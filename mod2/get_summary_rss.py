from pathlib import Path
import sys

UNITS = ["B", "KiB", "MiB", "GiB", "TiB"]


def convert_bytes(size: int) -> str:
    unit_index = 0
    while size >= 1024 and unit_index < len(UNITS) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {UNITS[unit_index]}"


def get_summary_rss(file_path: str) -> str:
    total_rss = 0

    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()[1:]  # пропускаем заголовок

    for line in lines:
        columns = line.split()
        if len(columns) < 6:
            continue
        try:
            total_rss += int(columns[5])  # RSS — 6-й столбец
        except ValueError:
            continue

    return convert_bytes(total_rss)


if __name__ == "__main__":
    OUTPUT_FILE = "output_file.txt"
    print(get_summary_rss(OUTPUT_FILE))