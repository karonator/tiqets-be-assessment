import csv
import heapq
from collections import defaultdict


def __main__():
    orders = []
    with open("orders.csv") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if len(row) != 2:
                continue
            orders.append(row)
    orders.sort()

    barcodes = []
    with open("barcodes.csv") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if len(row) != 2:
                continue
            if row[1]:
                barcodes.append([row[1], row[0]])
    barcodes.sort()

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
