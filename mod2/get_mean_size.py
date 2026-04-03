import sys


def get_mean_size(lines) -> float:
    sizes = []

    for line in lines[1:]:
        columns = line.split()
        if len(columns) < 5:
            continue

        try:
            size = int(columns[4])
            sizes.append(size)
        except ValueError:
            continue

    if not sizes:
        return 0

    return sum(sizes) / len(sizes)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    mean_size = get_mean_size(lines)
    print(mean_size)