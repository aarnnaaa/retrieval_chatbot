import sqlite3

conn = sqlite3.connect('courier.db')
cursor = conn.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS parcels(
               id TEXT PRIMARY KEY,
               sender TEXT,
               recipient TEXT,
               status TEXT,
               eta TEXT,
               user_id TEXT)""")

sample_data = [
    ("P10002", "Flipkart", "Rahul Mehta", "Delivered", "2025-06-10", "user_002"),
    ("P10003", "Myntra", "Sneha Sharma", "Out for Delivery", "2025-06-12", "user_003"),
    ("P10004", "Nykaa", "Anjali Rao", "Delayed", "2025-06-18", "user_004"),
    ("P10005", "Ajio", "Karan Singh", "Shipped", "2025-06-14", "user_005"),
    ("P10006", "Apple", "Neha Patil", "Delivered", "2025-06-05", "user_006"),
    ("P10007", "Samsung", "Vikram Reddy", "Returned", "2025-06-01", "user_007"),
    ("P10008", "Dell", "Priya Verma", "Out for Delivery", "2025-06-12", "user_008"),
    ("P10009", "HP", "Arjun Malhotra", "In Transit", "2025-06-17", "user_009"),
    ("P10010", "Boat", "Isha Jain", "Shipped", "2025-06-13", "user_010")
]

cursor.executemany("INSERT OR REPLACE INTO parcels VALUES (?, ?, ?, ?, ?, ?)", sample_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("database created and sample data inserted.")