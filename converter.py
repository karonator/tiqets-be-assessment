import csv
import heapq
from collections import defaultdict


def read_orders(file_path: str) -> list | None:
    orders = []
    try:
        with open(file_path) as orders_file:
            reader = csv.reader(orders_file)
            next(reader, None)
            for row in reader:
                if len(row) != 2:
                    continue
                orders.append(row)
        orders.sort()
        return orders
    except Exception as e:
        print(f"Error reading orders file: {e}")
    return None


def read_barcodes(file_path: str) -> list | None:
    barcodes = []
    unique_barcodes = set()
    unused_barcodes = 0
    try:
        with open("barcodes.csv") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for row in reader:
                if len(row) != 2:
                    continue

                barcode = row[0]
                order = row[1]

                if barcode in unique_barcodes:
                    print(f"Duplicate barcode {barcode}")
                    continue
                else:
                    unique_barcodes.add(barcode)

                if order:
                    barcodes.append(list(reversed(row)))
                else:
                    unused_barcodes += 1
        barcodes.sort()
        return barcodes, unused_barcodes
    except Exception as e:
        print(f"Error reading barcodes file: {e}")
    return None


def __main__() -> None:
    orders = read_orders("orderws.csv")
    if orders is None:
        return

    barcodes, unused_barcodes = read_barcodes("barcodes.csv")
    if barcodes is None:
        return

    print(f"Unused barcodes: {unused_barcodes}")

    # merge sorted orders and barcodes

    i = 0
    j = 0

    current_order = []
    customers = defaultdict(int)

    while i < len(orders) and j < len(barcodes):
        if orders[i][0] == barcodes[j][0]:
            current_order.append(barcodes[j][1])
            j += 1
        elif orders[i][0] < barcodes[j][0]:
            if not current_order:
                print(
                    "Order {} is missing barcodes".format(
                        orders[i][0]
                    )
                )
            else:
                print(orders[i], current_order)
                customers[orders[i][1]] += len(current_order)
                current_order = []
            i += 1
        else:
            print(
                "Order {} is missing customer".format(barcodes[j][0])
            )
            j += 1

    top_5_customers = heapq.nlargest(
        5, customers.items(), key=lambda x: x[1]
    )
    print(top_5_customers)


if __name__ == "__main__":
    __main__()
