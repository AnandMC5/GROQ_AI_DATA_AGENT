# import csv
# import random
# import datetime

# # Define file name
# filename = "C:/PROJECTS/GROK_DATA_AGENT/data/input/orders.csv"

# # Define columns
# columns = ["OrderID", "CustomerName", "Product", "Quantity", "Price", "OrderDate"]

# # Sample data pools
# customers = ["John Doe", "Jane Smith", "Michael Lee", "Sara Khan", "David Brown", None]
# products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor", None]

# # Generate rows
# rows = []
# for i in range(10000):
#     order_id = random.randint(1000, 11000)  # some duplicates
#     customer = random.choice(customers)
#     product = random.choice(products)
#     quantity = random.randint(1, 10)
#     price = random.choice([1200, 800, 450, 300, 150, None])  # some nulls
#     order_date = datetime.date(2026, random.randint(1, 12), random.randint(1, 28))
    
#     rows.append([order_id, customer, product, quantity, price, order_date])

# # Write to CSV
# with open(filename, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(columns)
#     writer.writerows(rows)

# print(f"CSV file '{filename}' with 10,000 rows created successfully!")


# import csv
# import random
# import datetime

# # File name
# filename = "C:/PROJECTS/GROK_DATA_AGENT/data/input/sales.psv"

# # Define columns
# columns = ["SaleID", "CustomerName", "Product", "Quantity", "Price", "SaleDate"]

# # Sample data pools
# customers = ["John Doe", "Jane Smith", "Michael Lee", "Sara Khan", "David Brown", None]
# products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor", None]

# # Generate rows
# rows = []
# for i in range(20000):
#     sale_id = random.randint(1000, 25000)  # duplicates possible
#     customer = random.choice(customers)
#     product = random.choice(products)
#     quantity = random.randint(1, 10)
#     price = random.choice([1200, 800, 450, 300, 150, None])  # some nulls
#     sale_date = datetime.date(2026, random.randint(1, 12), random.randint(1, 28))
    
#     rows.append([sale_id, customer, product, quantity, price, sale_date])

# # Write to PSV (pipe-separated)
# with open(filename, "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f, delimiter="|")
#     writer.writerow(columns)
#     writer.writerows(rows)

# print(f"PSV file '{filename}' with 20,000 rows created successfully!")


import pandas as pd
import random
import datetime

# File name
filename = "C:/PROJECTS/GROK_DATA_AGENT/data/input/product.xlsx"

# Define columns
columns = ["ProductID", "ProductName", "Category", "Quantity", "Price", "AddedDate"]

# Sample data pools
products = ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor", "Keyboard", None]
categories = ["Electronics", "Accessories", "Office", "Gaming", None]

# Generate rows
rows = []
for i in range(30000):
    product_id = random.randint(1000, 35000)  # duplicates possible
    product_name = random.choice(products)
    category = random.choice(categories)
    quantity = random.randint(1, 50)
    price = random.choice([1200, 800, 450, 300, 150, None])  # some nulls
    added_date = datetime.date(2026, random.randint(1, 12), random.randint(1, 28))
    
    rows.append([product_id, product_name, category, quantity, price, added_date])

# Create DataFrame
df = pd.DataFrame(rows, columns=columns)

# Save to Excel
df.to_excel(filename, index=False)

print(f"Excel file '{filename}' with 30,000 rows created successfully!")
