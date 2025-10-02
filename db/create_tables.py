import sqlite3
import os
from datetime import datetime, timedelta
import random

# Ensure "data" directory exists
os.makedirs("data", exist_ok=True)

# Connect to database
conn = sqlite3.connect("data/apps.db")
c = conn.cursor()

RESET_DATABASE = True 

if RESET_DATABASE:
    print("Resetting database...")
    c.execute("DROP TABLE IF EXISTS orders")
    c.execute("DROP TABLE IF EXISTS products") 
    c.execute("DROP TABLE IF EXISTS users")

# --- Create Tables ---
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    is_active INTEGER NOT NULL,
    created_at TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    order_status TEXT NOT NULL,
    order_date TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

def random_past_date(days_back=365):
    days_ago = random.randint(1, days_back)
    return (datetime.now() - timedelta(days=days_ago)).isoformat()

# Inserting sample data 

# 12 Users
users = [
    ("Sarah Johnson", "sarah.johnson@gmail.com", 1, random_past_date(180)),
    ("Michael Chen", "m.chen@outlook.com", 1, random_past_date(240)),
    ("Emily Rodriguez", "emily.r.2024@yahoo.com", 1, random_past_date(90)),
    ("James Wilson", "james.wilson@company.com", 0, random_past_date(300)),  # Inactive
    ("Priya Patel", "priya.patel@tech.io", 1, random_past_date(45)),
    ("David Thompson", "d.thompson@university.edu", 1, random_past_date(120)),
    ("Maria Garcia", "maria.garcia@startup.com", 1, random_past_date(60)),
    ("Robert Kim", "robert.kim@freelancer.net", 0, random_past_date(400)),  # Inactive
    ("Jessica Brown", "jess.brown.writer@gmail.com", 1, random_past_date(15)),
    ("Ahmed Hassan", "a.hassan@consulting.biz", 1, random_past_date(200)),
    ("Lisa Anderson", "lisa.and@photographer.pro", 1, random_past_date(30)),
    ("Chris Martinez", "chris.m.dev@github.io", 1, random_past_date(75))
]
c.executemany("INSERT OR IGNORE INTO users (name, email, is_active, created_at) VALUES (?, ?, ?, ?)", users)

# 25 Products across different categories
products = [
    # Electronics
    ("MacBook Pro 16-inch", "Electronics", 2499.99, 8),
    ("iPhone 15 Pro", "Electronics", 1199.00, 15),
    ("Samsung Galaxy S24", "Electronics", 899.99, 22),
    ("Sony WH-1000XM5 Headphones", "Electronics", 399.99, 35),
    ("iPad Air 11-inch", "Electronics", 699.00, 12),
    ("Dell XPS 13 Laptop", "Electronics", 1399.99, 6),
    ("AirPods Pro (2nd Gen)", "Electronics", 249.99, 45),
    
    # Home & Kitchen
    ("Ninja Foodi Air Fryer", "Home & Kitchen", 159.99, 28),
    ("Dyson V15 Vacuum Cleaner", "Home & Kitchen", 749.99, 5),
    ("KitchenAid Stand Mixer", "Home & Kitchen", 449.99, 14),
    ("Yeti Rambler Tumbler", "Home & Kitchen", 39.99, 120),
    ("Instant Pot Duo 7-in-1", "Home & Kitchen", 99.99, 32),
    
    # Books
    ("The Psychology of Money", "Books", 16.99, 85),
    ("Atomic Habits", "Books", 18.99, 67),
    ("The Midnight Library", "Books", 14.99, 42),
    ("Educated: A Memoir", "Books", 17.99, 38),
    
    # Clothing
    ("Levi's 501 Original Jeans", "Clothing", 89.99, 55),
    ("Nike Air Max 270", "Clothing", 149.99, 33),
    ("Patagonia Houdini Jacket", "Clothing", 129.99, 18),
    ("Uniqlo Merino Wool Sweater", "Clothing", 59.99, 41),
    
    # Sports & Outdoors
    ("Hydro Flask Water Bottle", "Sports & Outdoors", 44.99, 78),
    ("Yoga Mat Premium", "Sports & Outdoors", 89.99, 29),
    ("Resistance Bands Set", "Sports & Outdoors", 24.99, 95),
    
    # Office Supplies
    ("Ergonomic Office Chair", "Office Supplies", 299.99, 11),
    ("Moleskine Notebook Set", "Office Supplies", 34.99, 156)
]
c.executemany("INSERT OR IGNORE INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)", products)

# 35 Orders by users for various products
orders = [
    # Recent orders (last 30 days)
    (9, 1, 1, "Delivered", (datetime.now() - timedelta(days=5)).isoformat()),   # Jessica bought MacBook
    (11, 7, 2, "Shipped", (datetime.now() - timedelta(days=3)).isoformat()),   # Lisa bought 2 AirPods
    (5, 13, 1, "Pending", (datetime.now() - timedelta(days=1)).isoformat()),   # Priya bought book
    (12, 21, 1, "Processing", (datetime.now() - timedelta(days=2)).isoformat()), # Chris bought water bottle
    
    # This month
    (1, 4, 1, "Delivered", (datetime.now() - timedelta(days=12)).isoformat()),  # Sarah bought headphones
    (3, 17, 2, "Delivered", (datetime.now() - timedelta(days=18)).isoformat()),  # Emily bought 2 jeans
    (7, 8, 1, "Delivered", (datetime.now() - timedelta(days=25)).isoformat()),  # Maria bought air fryer
    (10, 22, 1, "Shipped", (datetime.now() - timedelta(days=8)).isoformat()),   # Ahmed bought yoga mat
    (6, 14, 3, "Delivered", (datetime.now() - timedelta(days=15)).isoformat()), # David bought 3 books
    
    # Last month
    (1, 2, 1, "Delivered", (datetime.now() - timedelta(days=45)).isoformat()),  # Sarah bought iPhone
    (5, 11, 2, "Delivered", (datetime.now() - timedelta(days=38)).isoformat()), # Priya bought 2 tumblers
    (9, 18, 1, "Delivered", (datetime.now() - timedelta(days=52)).isoformat()), # Jessica bought Nike shoes
    (11, 24, 1, "Delivered", (datetime.now() - timedelta(days=41)).isoformat()), # Lisa bought office chair
    
    # 2-3 months ago
    (3, 12, 1, "Delivered", (datetime.now() - timedelta(days=78)).isoformat()), # Emily bought Instant Pot
    (7, 19, 1, "Delivered", (datetime.now() - timedelta(days=85)).isoformat()), # Maria bought jacket
    (12, 6, 1, "Delivered", (datetime.now() - timedelta(days=92)).isoformat()), # Chris bought Dell laptop
    (10, 23, 2, "Delivered", (datetime.now() - timedelta(days=67)).isoformat()), # Ahmed bought resistance bands
    
    # Older orders (3-6 months ago)
    (1, 9, 1, "Delivered", (datetime.now() - timedelta(days=125)).isoformat()), # Sarah bought Dyson vacuum
    (5, 3, 1, "Delivered", (datetime.now() - timedelta(days=134)).isoformat()), # Priya bought Samsung phone
    (6, 16, 2, "Delivered", (datetime.now() - timedelta(days=156)).isoformat()), # David bought 2 memoirs
    (9, 20, 1, "Delivered", (datetime.now() - timedelta(days=143)).isoformat()), # Jessica bought sweater
    
    # Multiple orders from same users (showing customer loyalty)
    (1, 25, 3, "Delivered", (datetime.now() - timedelta(days=167)).isoformat()), # Sarah bought notebooks
    (1, 15, 2, "Delivered", (datetime.now() - timedelta(days=189)).isoformat()), # Sarah bought books
    (5, 21, 1, "Delivered", (datetime.now() - timedelta(days=201)).isoformat()), # Priya bought water bottle
    (9, 13, 1, "Delivered", (datetime.now() - timedelta(days=178)).isoformat()), # Jessica bought psychology book
    
    # Some cancelled/returned orders (realistic scenario)
    (3, 1, 1, "Cancelled", (datetime.now() - timedelta(days=95)).isoformat()),  # Emily cancelled MacBook
    (7, 5, 1, "Returned", (datetime.now() - timedelta(days=110)).isoformat()),  # Maria returned iPad
    (12, 24, 1, "Cancelled", (datetime.now() - timedelta(days=88)).isoformat()), # Chris cancelled chair
    
    # High-value orders
    (10, 1, 2, "Delivered", (datetime.now() - timedelta(days=234)).isoformat()), # Ahmed bought 2 MacBooks (business)
    (6, 6, 3, "Delivered", (datetime.now() - timedelta(days=198)).isoformat()), # David bought 3 Dell laptops (university)
    
    # Recent bulk orders
    (11, 25, 5, "Delivered", (datetime.now() - timedelta(days=21)).isoformat()), # Lisa bought 5 notebooks
    (5, 23, 3, "Shipped", (datetime.now() - timedelta(days=6)).isoformat()),   # Priya bought resistance bands
    
    # Mixed category orders
    (7, 14, 1, "Delivered", (datetime.now() - timedelta(days=72)).isoformat()), # Maria bought Atomic Habits
    (10, 10, 1, "Delivered", (datetime.now() - timedelta(days=145)).isoformat()), # Ahmed bought KitchenAid
    (12, 4, 1, "Processing", (datetime.now() - timedelta(days=4)).isoformat()), # Chris bought Sony headphones
    
    # Edge cases - inactive users with old orders (they became inactive later)
    (4, 17, 1, "Delivered", (datetime.now() - timedelta(days=320)).isoformat()), # James (now inactive)
    (8, 11, 2, "Delivered", (datetime.now() - timedelta(days=380)).isoformat())  # Robert (now inactive)
]

c.executemany("INSERT OR IGNORE INTO orders (user_id, product_id, quantity, order_status, order_date) VALUES (?, ?, ?, ?, ?)", orders)

conn.commit()
conn.close()