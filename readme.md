# Orders and Barcodes Merger

This program reads two CSV files (`orders.csv` and `barcodes.csv`), merges them based on `order_id`, and writes the merged data to an output CSV file. 

## Usage

### Command Line Interface

To run the program from the command line, use the short command:

```
python converter.py
```

Or the full command:

```sh
python converter.py --orders path/to/orders.csv --barcodes path/to/barcodes.csv --output path/to/output.csv
```

### Arguments

- `--orders`: Path to the orders CSV file (default: `orders.csv`).
- `--barcodes`: Path to the barcodes CSV file (default: `barcodes.csv`).
- `--output`: Path to the output CSV file (default: `output.csv`).
- `--help -h`: Prints help to the command line.

## Files Format

### orders.csv

The `orders.csv` file should have the following structure:

```csv
order_id,customer_id
1,1001
2,1002
3,1003
...
```

The first line of the file will be interpreted as a header.
No any other additional requirements, order_id and customer_id can have any format, int not necessary.

### barcodes.csv

The `barcodes.csv` file should have the following structure:

```csv
barcode,order_id
ABC123,1
DEF456,2
GHI789,3
...
```

The first line of the file will be interpreted as a header.
No any other additional requirements, order_id and barcode can have any format.

## Output

The output CSV file will have the following structure:

```csv
order_id,customer_id,barcodes
1,1001,ABC123
2,1002,DEF456, GHI789
...
```

## Additional Information

- The program prints the number of unused barcodes.
- The program prints the top 5 customers based on the number of barcodes.

## Error Handling

- If there is an error reading any of the CSV files, an appropriate error message will be printed to the standard error.
- Also the programm will write a message to standard error if:
- - There is order without a barcode
- - There is a duplicating barcode
- - There is the barcode without a customer (not necessary but was added because it's easy to check)


## Example Output

After running the program, you might see an output similar to the following in your console:

```sh
Unused barcodes: 2
Top 5 customers:
1001, 5
1002, 3
1003, 2
...
```

## Comments

The program works by iterating over two sorted lists. When reading the barcodes, we invert the barcode row so that both files are read into lists of tuples with order_id at index 0. Then we use a simple sort. The format of order_id (whether it's an int, string, or UUID) doesn't matter, as long as both lists are sorted using the same algorithm.

Unfortunately, this approach requires reading both files into program memory. While we could sort the files externally and then process them line by line, similar to how we iterate through the lists, this would introduce significant overhead.

In a real-world scenario, if we're using something like Django I'll organize DB like this:

```
CREATE TABLE orders (
    order_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL
);

CREATE TABLE barcodes (
    barcode VARCHAR(255) PRIMARY KEY,
    order_id VARCHAR(255),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE INDEX idx_order_id ON barcodes(order_id);
```

...but really I'll use Django and do something like this:

```
from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=255, primary_key=True)
    customer_id = models.CharField(max_length=255)

    def __str__(self):
        return self.order_id

class Barcode(models.Model):
    barcode = models.CharField(max_length=255, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.barcode
```

Thank you for your time.