import csv
import sqlite3

# Connect to the database
conn = sqlite3.connect("thuisbezongd.db")
cursor = conn.cursor()

# Create the new table
cursor.execute("CREATE TABLE netherlands_pc4 (X REAL, Y REAL, PC_4 INTEGER, Year INTEGER, Gemeente_code INTEGER, Provincie_code INTEGER, Provincie_name TEXT, Gemeente_name TEXT)")

# Open the CSV file
with open("netherlands-postcode-pc4.csv") as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    # Skip the first row (header)
    next(reader)
    # Iterate over the rows
    for row in reader:
        # Insert the data into the table
        cursor.execute("INSERT INTO netherlands_pc4 (X, Y, PC_4, Year, Gemeente_code, Provincie_code, Provincie_name, Gemeente_name) VALUES (?,?,?,?,?,?,?,?)", row)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
