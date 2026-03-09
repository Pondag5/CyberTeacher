"""
Аудит базы знаний
Проверяет PDF на качество
"""
import os

KB_DIR = "knowledge_base"

def audit_knowledge_base():
    """Аудит PDF файлов"""
    issues = []
    good = []
    small = []
    
    for f in os.listdir(KB_DIR):
        if not f.endswith('.pdf'):
            continue
        
        path = os.path.join(KB_DIR, f)
        size = os.path.getsize(path)
        
        if size < 10000:  # Менее 10KB - подозрительно
            small.append((f, size))
        elif size < 50000:  # Менее 50KB - маловато
            issues.append((f, size, "Маленький файл"))
        else:
            good.append((f, size))
    
    report = f"""
=== АУДИТ БАЗЫ ЗНАНИЙ ===

Всего PDF: {len(good) + len(issues) + len(small)}

✅ Хорошие ({len(good)}):
"""
    for f, s in good[:10]:
        report += f"  - {f[:50]} ({s/1024:.0f}KB)\n"
    if len(good) > 10:
        report += f"  ... и ещё {len(good)-10}\n"
    
    if issues:
        report += f"\n⚠️ Под вопросом ({len(issues)}):\n"
        for f, s, msg in issues:
            report += f"  - {f[:50]} ({s/1024:.0f}KB) - {msg}\n"
    
    if small:
        report += f"\n❌ Слишком маленькие ({len(small)}):\n"
        for f, s in small:
            report += f"  - {f[:50]} ({s} bytes)\n"
    
    return report

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(audit_knowledge_base())
