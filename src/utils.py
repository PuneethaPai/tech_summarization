import csv
from typing import Dict, Iterable, Any


def read_csv(path: str) -> Iterable[Dict[str, Any]]:
    """Reads csv and yeilds row as dict"""
    csv.field_size_limit(int(1e7))
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def write_csv(
    path: str, data: Iterable[Dict[str, Any]], header: Iterable[str] = None
) -> None:
    """Writes data into csv"""
    if not header:
        header = data[0].keys()
    with open(path, "w+", newline="") as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(data)
