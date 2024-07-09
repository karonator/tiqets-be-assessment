import argparse
import csv
import heapq
import sys
from collections import defaultdict


def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


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
        error_print(f"Error reading orders file: {e}")
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
                order_id = row[1]

                if barcode in unique_barcodes:
                    error_print(f"Duplicate barcode {barcode}")
                    continue
                else:
                    unique_barcodes.add(barcode)

                if order_id:
                    barcodes.append(list(reversed(row)))
                else:
                    unused_barcodes += 1
        barcodes.sort()
        return barcodes, unused_barcodes
    except Exception as e:
        error_print(f"Error reading barcodes file: {e}")
    return None


def __main__() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Merge orders and barcodes CSV files"
            " by order_id and write to output CSV file"
        )
    )
    parser.add_argument(
        "--orders",
        type=str,
        default="orders.csv",
        help="Path to orders CSV file",
    )
    parser.add_argument(
        "--barcodes",
        type=str,
        default="barcodes.csv",
        help="Path to barcodes CSV file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.csv",
        help="Path to output CSV file",
    )
    args = parser.parse_args()

    orders = read_orders(args.orders)
    if orders is None:
        return

    barcodes, unused_barcodes = read_barcodes(args.barcodes)
    if barcodes is None:
        return

    print(f"Unused barcodes: {unused_barcodes}")

    # merge sorted orders and sorted by order barcodes

    i = 0
    j = 0

    current_order = []
    customers = defaultdict(int)

    try:
        with open(args.output, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["order_id", "customer_id", "barcodes"])
            while i < len(orders) and j < len(barcodes):
                order_id = orders[i][0]
                customer_id = orders[i][1]

                barcode_order_id = barcodes[j][0]
                barcode = barcodes[j][1]

                if order_id == barcode_order_id:
                    current_order.append(barcode)
                    j += 1
                elif order_id < barcode_order_id:
                    if not current_order:
                        error_print(f"Order {order_id} is missing barcodes")
                    else:
                        writer.writerow(
                            [order_id, customer_id] + current_order
                        )
                        customers[customer_id] += len(current_order)
                        current_order = []
                    i += 1
                else:
                    error_print(
                        f"Order {barcode_order_id} is missing customer"
                    )
                    j += 1
    except Exception as e:
        error_print(f"Error writing output file: {e}")
        return

    top_5_customers = heapq.nlargest(5, customers.items(), key=lambda x: x[1])

    print("Top 5 customers:")
    for customer_data in top_5_customers:
        print(f"{customer_data[0]}, {customer_data[1]}")


if __name__ == "__main__":
    __main__()
