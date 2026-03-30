import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    if db.is_connected():
        print("✅ Success! Python is connected to the Database.")

    cursor = db.cursor()

    # שליפת נתוני הנכסים (Assets)
    cursor.execute("SELECT * FROM Assets")

    print("\n--- Registered Assets in System Memory ---")
    assets = cursor.fetchall()

    for row in assets:
        print(f"ID: {row[0]} | Name: {row[2]} | IP: {row[1]} | Status: {row[4]}")

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")

finally:
    # סגירה בטוחה של החיבור
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\n🔒 Connection closed safely.")