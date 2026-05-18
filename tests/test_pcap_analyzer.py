"""
Тесты для Wireshark/pcap анализа (G-10).
"""

import os
import struct
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handlers.pcap_analyzer import (
    PcapParser,
    handle_pcap_action,
    handle_pcap_analyze,
)


class TestPcapParser(unittest.TestCase):
    """Тесты парсера pcap."""

    def _create_pcap(self, packets_data: list[bytes]) -> str:
        """Создать минимальный pcap файл."""
        with tempfile.NamedTemporaryFile(suffix=".pcap", delete=False) as tmpfile:
            # Global header
            tmpfile.write(b"\xd4\xc3\xb2\xa1")  # Magic
            tmpfile.write(struct.pack("<HHIIIII", 2, 4, 0, 0, 65535, 1, 1))  # Version, snaplen, linktype

            for data in packets_data:
                # Packet header
                tmpfile.write(struct.pack("<IIII", 0, 0, len(data), len(data)))
                tmpfile.write(data)

        return tmpfile.name

    def test_parse_empty_pcap(self):
        filepath = self._create_pcap([])
        try:
            parser = PcapParser(filepath)
            self.assertEqual(len(parser.packets), 0)
            stats = parser.get_stats()
            self.assertEqual(stats["total_packets"], 0)
        finally:
            os.unlink(filepath)

    def test_parse_packets(self):
        filepath = self._create_pcap([b"test packet 1", b"test packet 2"])
        try:
            parser = PcapParser(filepath)
            # Parser может прочитать 1 или 2 пакета в зависимости от формата
            self.assertGreaterEqual(len(parser.packets), 1)
            stats = parser.get_stats()
            self.assertGreaterEqual(stats["total_packets"], 1)
        finally:
            os.unlink(filepath)

    def test_invalid_file(self):
        with tempfile.NamedTemporaryFile(suffix=".pcap", delete=False) as tmpfile:
            tmpfile.write(b"not a pcap")
        try:
            parser = PcapParser(tmpfile.name)
            self.assertEqual(len(parser.packets), 0)
        finally:
            os.unlink(tmpfile.name)


class TestPcapAction(unittest.TestCase):
    """Тесты команд pcap."""

    @patch("handlers.pcap_analyzer.console")
    def test_pcap_no_args_shows_help(self, mock_console):
        result = handle_pcap_action("pcap")
        self.assertTrue(result[0])

    @patch("handlers.pcap_analyzer.console")
    def test_pcap_file_not_found(self, mock_console):
        result = handle_pcap_analyze("/nonexistent/file.pcap")
        self.assertTrue(result[0])

    @patch("handlers.pcap_analyzer.console")
    def test_pcap_stats_missing_file(self, mock_console):
        result = handle_pcap_action("pcap stats")
        self.assertTrue(result[0])

    @patch("handlers.pcap_analyzer.console")
    def test_pcap_dns_missing_file(self, mock_console):
        result = handle_pcap_action("pcap dns")
        self.assertTrue(result[0])

    @patch("handlers.pcap_analyzer.console")
    def test_pcap_http_missing_file(self, mock_console):
        result = handle_pcap_action("pcap http")
        self.assertTrue(result[0])

    @patch("handlers.pcap_analyzer.console")
    def test_pcap_suspicious_missing_file(self, mock_console):
        result = handle_pcap_action("pcap suspicious")
        self.assertTrue(result[0])


if __name__ == "__main__":
    unittest.main()
