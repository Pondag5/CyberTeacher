import os

project_root = r"M:\Cyber_Teacher\Cyber_Teacher"
output_file = os.path.join(project_root, "project_dump.txt")
target_dirs = ["docs", "tracks", "missions", "hints", "book_new"]  # укажи нужные папки

with open(output_file, "w", encoding="utf-8") as out:
    for folder in target_dirs:
        dir_path = os.path.join(project_root, folder)
        if not os.path.exists(dir_path):
            continue
        for root, _, files in os.walk(dir_path):
            for fname in files:
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, project_root)
                out.write(f"\n{'='*60}\n")
                out.write(f"ФАЙЛ: {rel}\n")
                out.write(f"{'='*60}\n")
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    # Ограничим до 2000 строк на файл, если гигантский
                    lines = content.splitlines()
                    out.write("\n".join(lines[:2000]))
                    if len(lines) > 2000:
                        out.write(f"\n... [обрезано, всего строк: {len(lines)}]\n")
                except Exception as e:
                    out.write(f"[Ошибка чтения: {e}]\n")
                out.write("\n")
print(f"Дамп сохранён: {output_file}")