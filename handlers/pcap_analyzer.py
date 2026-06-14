"""
🔍 Анализ pcap файлов (G-10)

Команды:
- /pcap <file> — общий анализ pcap файла
- /pcap stats <file> — статистика пакетов
- /pcap protocols <file> — распределение протоколов
- /pcap ips <file> — топ IP-адресов
- /pcap dns <file> — DNS запросы
- /pcap http <file> — HTTP запросы
- /pcap suspicious <file> — поиск подозрительной активности
- /pcap extract <file> <type> — извлечение данных (files, passwords, emails)
"""

import logging
import os
import re
import struct
from collections import Counter, defaultdict
from typing import Any, List, Dict, Optional, Tuple, Union

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from handlers.types import HandlerResult


console = Console()
logger = logging.getLogger(__name__)

# Попытка импорта scapy
try:
    from scapy.all import DNS, DNSQR, HTTP, IP, TCP, UDP, Raw, rdpcap

    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False


class PcapParser:
    """Минимальный парсер pcap без scapy."""

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.packets: List[Dict[str, Any]] = []
        self._parse()

    def _parse(self) -> None:
        """Парсинг pcap файла (формат libpcap)."""
        try:
            with open(self.filepath, "rb") as f:
                # Global header (24 bytes)
                magic = f.read(4)
                if magic not in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
                    raise ValueError("Not a valid pcap file")

                f.read(20)  # Skip rest of global header

                while True:
                    # Packet header (16 bytes)
                    pkt_header = f.read(16)
                    if len(pkt_header) < 16:
                        break

                    if magic == b"\xd4\xc3\xb2\xa1":
                        ts_sec, ts_usec, incl_len, orig_len = struct.unpack(
                            "<IIII", pkt_header
                        )
                    else:
                        ts_sec, ts_usec, incl_len, orig_len = struct.unpack(
                            ">IIII", pkt_header
                        )

                    data = f.read(incl_len)
                    if len(data) < incl_len:
                        break

                    self.packets.append(
                        {
                            "timestamp": ts_sec + ts_usec / 1_000_000,
                            "length": orig_len,
                            "captured_len": incl_len,
                            "data": data,
                        }
                    )
        except Exception as e:
            logger.error(f"Error parsing pcap: {e}")

    def get_stats(self) -> dict:
        """Базовая статистика."""
        if not self.packets:
            return {"total_packets": 0, "total_bytes": 0}

        total_bytes = sum(p["length"] for p in self.packets)
        durations = [p["timestamp"] for p in self.packets]
        duration = max(durations) - min(durations) if len(durations) > 1 else 0

        return {
            "total_packets": len(self.packets),
            "total_bytes": total_bytes,
            "duration_sec": round(duration, 2),
            "avg_packet_size": round(total_bytes / len(self.packets), 1)
            if self.packets
            else 0,
            "packets_per_sec": round(len(self.packets) / duration, 1)
            if duration > 0
            else 0,
        }


def analyze_pcap_scapy(filepath: str) -> Dict[str, Any]:
    """Анализ pcap с помощью scapy."""
    packets = rdpcap(filepath)
    results: Dict[str, Any] = {
        "total_packets": len(packets),
        "total_bytes": sum(len(p) for p in packets),
        "protocols": Counter(),
        "ip_pairs": Counter(),
        "dns_queries": [],
        "http_requests": [],
        "suspicious": [],
        "top_src_ips": Counter(),
        "top_dst_ips": Counter(),
        "top_ports": Counter(),
    }

    for pkt in packets:
        # Протоколы
        if pkt.haslayer(IP):
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            results["ip_pairs"][f"{src_ip} → {dst_ip}"] += 1
            results["top_src_ips"][src_ip] += 1
            results["top_dst_ips"][dst_ip] += 1

            if pkt.haslayer(TCP):
                results["protocols"]["TCP"] += 1
                results["top_ports"][f"TCP:{pkt[TCP].dport}"] += 1

                # HTTP detection
                if (pkt[TCP].dport == 80 or pkt[TCP].sport == 80) and pkt.haslayer(Raw):
                    payload = pkt[Raw].load.decode("utf-8", errors="ignore")
                    if payload.startswith(
                        ("GET ", "POST ", "PUT ", "DELETE ", "HEAD ")
                    ):
                        results["http_requests"].append(payload.split("\r\n")[0])

                # Suspicious: common attack ports
                if pkt[TCP].dport in (4444, 5555, 1337, 31337, 1234, 6667):
                    results["suspicious"].append(
                        {
                            "type": "suspicious_port",
                            "detail": f"{src_ip} → {dst_ip}:{pkt[TCP].dport}",
                        }
                    )

            elif pkt.haslayer(UDP):
                results["protocols"]["UDP"] += 1
                results["top_ports"][f"UDP:{pkt[UDP].dport}"] += 1

            # DNS
            if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
                qname = pkt[DNSQR].qname.decode("utf-8", errors="ignore")
                results["dns_queries"].append(qname)

                # Suspicious DNS
                if len(qname) > 50:
                    results["suspicious"].append(
                        {
                            "type": "long_dns_query",
                            "detail": qname[:80],
                        }
                    )

        elif pkt.haslayer("ARP"):
            results["protocols"]["ARP"] += 1

    return results


def analyze_pcap_basic(filepath: str) -> dict:
    """Базовый анализ без scapy."""
    parser = PcapParser(filepath)
    stats = parser.get_stats()

    # Поиск паттернов в raw data
    dns_queries = []
    http_requests = []
    suspicious = []

    for pkt in parser.packets:
        data = pkt["data"]
        try:
            text = data.decode("utf-8", errors="ignore")

            # DNS queries (look for common patterns)
            dns_match = re.search(r"([a-zA-Z0-9.-]+\.(com|net|org|io|ru|local))", text)
            if dns_match:
                dns_queries.append(dns_match.group(1))

            # HTTP requests
            http_match = re.search(r"(GET|POST|PUT|DELETE|HEAD) ([^\s]+) HTTP", text)
            if http_match:
                http_requests.append(f"{http_match.group(1)} {http_match.group(2)}")

            # Suspicious patterns
            if re.search(r"(password|passwd|pwd)\s*[:=]", text, re.IGNORECASE):
                suspicious.append({"type": "password_in_clear", "detail": text[:80]})
            if re.search(r"(4444|5555|1337|31337|6667)", text):
                suspicious.append(
                    {"type": "suspicious_port_pattern", "detail": text[:80]}
                )

        except (ValueError, IndexError, AttributeError, TypeError):
            continue

    return {
        **stats,
        "protocols": {"Unknown": len(parser.packets)},
        "dns_queries": dns_queries,
        "http_requests": http_requests,
        "suspicious": suspicious,
        "top_src_ips": Counter(),
        "top_dst_ips": Counter(),
        "top_ports": Counter(),
        "ip_pairs": Counter(),
    }


def handle_pcap_analyze(filepath: str) -> HandlerResult:
    """Общий анализ pcap файла."""
    if not os.path.exists(filepath):
        console.print(f"[red]Файл не найден: {filepath}[/red]")
        return True, None, None, True

    if not filepath.endswith((".pcap", ".pcapng", ".cap")):
        console.print("[yellow]⚠️ Файл может не быть pcap форматом[/yellow]")

    console.print(f"[bold]Анализирую: {filepath}[/bold]")

    try:
        if HAS_SCAPY:
            results = analyze_pcap_scapy(filepath)
        else:
            results = analyze_pcap_basic(filepath)

        # Summary panel
        summary = (
            f"📦 Пакетов: {results['total_packets']}\n"
            f"📊 Байт: {results.get('total_bytes', 0):,}\n"
            f"⏱️ Длительность: {results.get('duration_sec', 'N/A')} сек\n"
            f"📈 Пакетов/сек: {results.get('packets_per_sec', 'N/A')}\n"
            f"📐 Средний размер: {results.get('avg_packet_size', 'N/A')} байт"
        )

        console.print(Panel(summary, title="🔍 PCAP Analysis", border_style="cyan"))

        # Protocols
        protocols = results.get("protocols", {})
        if protocols:
            table = Table(title="Протоколы")
            table.add_column("Protocol", style="cyan")
            table.add_column("Count", justify="right")
            for proto, count in protocols.most_common(10):
                table.add_row(proto, str(count))
            console.print(table)

        # Suspicious
        suspicious = results.get("suspicious", [])
        if suspicious:
            console.print(
                f"[yellow]⚠️ Подозрительная активность ({len(suspicious)}):[/yellow]"
            )
            for s in suspicious[:10]:
                console.print(f"  • [{s['type']}] {s['detail']}")

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка анализа: {e}[/red]")
        return True, None, None, True


def handle_pcap_stats(filepath: str) -> HandlerResult:
    """Статистика пакетов."""
    if not os.path.exists(filepath):
        console.print(f"[red]Файл не найден: {filepath}[/red]")
        return True, None, None, True

    try:
        if HAS_SCAPY:
            results = analyze_pcap_scapy(filepath)
        else:
            results = analyze_pcap_basic(filepath)

        # Top IPs
        src_ips = results.get("top_src_ips", {})
        dst_ips = results.get("top_dst_ips", {})

        if src_ips:
            table = Table(title="Топ IP-адресов (источники)")
            table.add_column("IP", style="cyan")
            table.add_column("Packets", justify="right")
            for ip, count in src_ips.most_common(10):
                table.add_row(ip, str(count))
            console.print(table)

        if dst_ips:
            table = Table(title="Топ IP-адресов (назначения)")
            table.add_column("IP", style="cyan")
            table.add_column("Packets", justify="right")
            for ip, count in dst_ips.most_common(10):
                table.add_row(ip, str(count))
            console.print(table)

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_pcap_dns(filepath: str) -> HandlerResult:
    """DNS запросы из pcap."""
    if not os.path.exists(filepath):
        console.print(f"[red]Файл не найден: {filepath}[/red]")
        return True, None, None, True

    try:
        if HAS_SCAPY:
            results = analyze_pcap_scapy(filepath)
        else:
            results = analyze_pcap_basic(filepath)

        dns_queries = results.get("dns_queries", [])
        if dns_queries:
            console.print(f"[bold]DNS запросы ({len(dns_queries)}):[/bold]")
            dns_counter = Counter(dns_queries)
            for domain, count in dns_counter.most_common(30):
                console.print(f"  {domain} ({count})")
        else:
            console.print("[yellow]DNS запросы не найдены[/yellow]")

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_pcap_http(filepath: str) -> HandlerResult:
    """HTTP запросы из pcap."""
    if not os.path.exists(filepath):
        console.print(f"[red]Файл не найден: {filepath}[/red]")
        return True, None, None, True

    try:
        if HAS_SCAPY:
            results = analyze_pcap_scapy(filepath)
        else:
            results = analyze_pcap_basic(filepath)

        http_requests = results.get("http_requests", [])
        if http_requests:
            console.print(f"[bold]HTTP запросы ({len(http_requests)}):[/bold]")
            for req in http_requests[:30]:
                console.print(f"  {req}")
            if len(http_requests) > 30:
                console.print(f"  [dim]...и ещё {len(http_requests) - 30}[/dim]")
        else:
            console.print("[yellow]HTTP запросы не найдены[/yellow]")

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_pcap_suspicious(filepath: str) -> HandlerResult:
    """Поиск подозрительной активности."""
    if not os.path.exists(filepath):
        console.print(f"[red]Файл не найден: {filepath}[/red]")
        return True, None, None, True

    try:
        if HAS_SCAPY:
            results = analyze_pcap_scapy(filepath)
        else:
            results = analyze_pcap_basic(filepath)

        suspicious = results.get("suspicious", [])
        if suspicious:
            console.print(
                Panel(
                    f"Найдено {len(suspicious)} подозрительных событий:\n\n"
                    + "\n".join(
                        f"• [{s['type']}] {s['detail']}" for s in suspicious[:20]
                    ),
                    title="🚨 Suspicious Activity",
                    border_style="red",
                )
            )
        else:
            console.print("[green]✅ Подозрительная активность не обнаружена[/green]")

        return True, None, None, True

    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")
        return True, None, None, True


def handle_pcap_action(action: str) -> HandlerResult:
    """Обработка /pcap <subcommand>."""
    parts = action.split()

    if len(parts) < 2:
        console.print("[cyan]Использование:[/cyan]")
        console.print("  /pcap <file>              — общий анализ")
        console.print("  /pcap stats <file>        — статистика")
        console.print("  /pcap protocols <file>    — протоколы")
        console.print("  /pcap ips <file>          — топ IP-адресов")
        console.print("  /pcap dns <file>          — DNS запросы")
        console.print("  /pcap http <file>         — HTTP запросы")
        console.print("  /pcap suspicious <file>   — подозрительная активность")
        console.print("\n[dim]Пример: /pcap capture.pcap[/dim]")
        return True, None, None, True

    subcmd = parts[1]

    if subcmd in ("stats", "protocols", "ips"):
        if len(parts) < 3:
            console.print("[red]Укажите файл: /pcap stats <file>[/red]")
            return True, None, None, True
        return handle_pcap_stats(parts[2])
    elif subcmd == "dns":
        if len(parts) < 3:
            console.print("[red]Укажите файл: /pcap dns <file>[/red]")
            return True, None, None, True
        return handle_pcap_dns(parts[2])
    elif subcmd == "http":
        if len(parts) < 3:
            console.print("[red]Укажите файл: /pcap http <file>[/red]")
            return True, None, None, True
        return handle_pcap_http(parts[2])
    elif subcmd == "suspicious":
        if len(parts) < 3:
            console.print("[red]Укажите файл: /pcap suspicious <file>[/red]")
            return True, None, None, True
        return handle_pcap_suspicious(parts[2])
    else:
        # Treat as file path
        return handle_pcap_analyze(subcmd)
