import threading
import time
import random
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def connect_to_db():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as err:
        print(f"❌ Simulator Connection Error: {err}")
        return None

# --- 1. תעבורה לגיטימית ---
def simulate_legitimate_traffic(num_events):
    db = connect_to_db()
    if not db: return
    cursor = db.cursor()
    print(f">>> [THREAD] Legitimate traffic started...")
    for i in range(num_events):
        source_ip = f"192.168.1.{random.randint(1, 254)}"
        cursor.execute("INSERT INTO Network_Traffic (source_ip, dest_asset_id, port_number, packet_size_kb) VALUES (%s, %s, %s, %s)",
                       (source_ip, random.randint(1, 4), 80, random.randint(20, 1500)))
    db.commit()
    db.close()

# --- 2. תקיפת DDoS ---
def attack_ddos(total_requests=1000):
    db = connect_to_db()
    if not db: return
    cursor = db.cursor()
    # רעש רקע לסטיית תקן
    for i in range(10):
        cursor.execute("INSERT INTO Network_Traffic (source_ip, dest_asset_id, port_number, packet_size_kb) VALUES (%s, %s, %s, %s)",
                       (f"192.168.1.{i}", 1, 443, 50))
    # התקפה
    botnet = [f"10.50.1.{i}" for i in range(1, 6)]
    for _ in range(total_requests):
        cursor.execute("INSERT INTO Network_Traffic (source_ip, dest_asset_id, port_number, packet_size_kb) VALUES (%s, %s, %s, %s)",
                       (random.choice(botnet), random.randint(1, 4), 443, random.randint(7000, 9000)))
    db.commit()
    db.close()

# --- 3. תקיפת Brute Force ---
def attack_brute_force(num_attempts=500):
    db = connect_to_db()
    if not db: return
    cursor = db.cursor()
    # רעש רקע
    for i in range(10):
        cursor.execute("INSERT INTO Network_Traffic (source_ip, dest_asset_id, port_number, packet_size_kb) VALUES (%s, %s, %s, %s)",
                       (f"10.0.0.{i}", 1, 22, 2))
    # התקפה
    attacker_ip = f"172.16.10.{random.randint(1, 254)}"
    for _ in range(num_attempts):
        cursor.execute("INSERT INTO Network_Traffic (source_ip, dest_asset_id, port_number, packet_size_kb) VALUES (%s, %s, %s, %s)",
                       (attacker_ip, random.randint(1, 4), 22, 2))
    db.commit()
    db.close()

# --- 4. תקיפת Port Scanning ---
def attack_port_scan():
    db = connect_to_db()
    if not db: return
    cursor = db.cursor()
    attacker_ip = f"192.168.9.{random.randint(1, 254)}"
    for port in range(1, 101):
        cursor.execute("INSERT INTO Network_Traffic (source_ip, dest_asset_id, port_number, packet_size_kb) VALUES (%s, %s, %s, %s)",
                       (attacker_ip, random.randint(1, 4), port, 1))
    db.commit()
    db.close()

def run_multi_attack_simulation():
    print("\n--- [SIMULATOR] Starting Integrated Attack Wave ---")
    threads = [
        threading.Thread(target=simulate_legitimate_traffic, args=(50,)),
        threading.Thread(target=attack_ddos, args=(1000,)),
        threading.Thread(target=attack_brute_force, args=(500,)),
        threading.Thread(target=attack_port_scan)
    ]
    for t in threads: t.start()
    for t in threads: t.join()
    print("--- [SIMULATOR] Wave Completed ---")

if __name__ == "__main__":
    run_multi_attack_simulation()