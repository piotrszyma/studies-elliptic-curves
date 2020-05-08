import argparse
import csv
import dataclasses
import matplotlib.pyplot as plt


@dataclasses.dataclass
class Row:
    x: int
    y: int
    type_: str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path")
    args = parser.parse_args()
    rows = []

    with open(args.input_path, newline="") as csvfile:
        raw_rows = csv.reader(csvfile, delimiter=";")

        for row in raw_rows:
            try:
                type_, x, y = row
            except ValueError:
                continue

            x = int(x)
            y = int(y)
            rows.append(Row(type_=type_, x=x, y=y))

    max_x = max(row.x for row in rows)
    max_y = max(row.y for row in rows)

    plt.plot([row.x for row in rows], [row.y for row in rows], markersize=3)
    plt.show()

    import pdb

    pdb.set_trace()


if __name__ == "__main__":
    main()
