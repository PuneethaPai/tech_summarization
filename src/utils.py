import csv


def read_csv(path: str) -> iter:
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def write_csv(path: str, data: iter, header: list = None) -> None:
    if not header:
        header = data[0].keys()
    with open(path, "w+", newline="") as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(data)
