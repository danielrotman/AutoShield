import threading
import time
import sys
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

try:
    import simulator as sim
    import analyzer as ana
    import mitigation as mit
except ImportError as e:
    print(f"❌ ERROR: Missing one of the project files! {e}")
    sys.exit(1)

def print_orchestrator_status(message):
    timestamp = time.strftime("%H:%M:%S")
    print(f"\n{'#'*70}\n[⚙️ ORCHESTRATOR - {timestamp}] {message}\n{'#'*70}")

def start_simulation():
    print("[🌱] Simulator Thread: Active. Injecting traffic and attacks...")
    while True:
        try:
            sim.run_multi_attack_simulation()
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Simulation Error: {e}")
            time.sleep(5)

def start_analysis():
    while True:
        try:
            time.sleep(10)
            ana.run_advanced_security_analysis()
        except Exception as e:
            print(f"⚠️ Analysis Error: {e}")

def start_mitigation():
    while True:
        try:
            time.sleep(15)
            mit.run_full_mitigation()
        except Exception as e:
            print(f"⚠️ Mitigation Error: {e}")

if __name__ == "__main__":
    print_orchestrator_status("INITIALIZING AUTONOMOUS WAR ROOM ENGINE")

    threads = [
        threading.Thread(target=start_simulation, name="Simulator-Thread"),
        threading.Thread(target=start_analysis, name="Analyzer-Thread"),
        threading.Thread(target=start_mitigation, name="Mitigation-Thread")
    ]

    for t in threads:
        t.daemon = True
        t.start()
        print(f"[*] Started {t.name}...")

    print_orchestrator_status("SYSTEM IS LIVE - MONITORING NETWORK TRAFFIC")

    try:
        while True:
            try:
                # שימוש במשתני סביבה במקום Hardcoded Credentials
                db = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME")
                )
                cursor = db.cursor()
                cursor.execute("DELETE FROM Network_Traffic WHERE timestamp < NOW() - INTERVAL 5 MINUTE")
                db.commit()
                db.close()
                print("[🧹] Cleanup: Old traffic data cleared to keep Z-Score accurate.")
            except Exception as e:
                print(f"⚠️ Cleanup Error: {e}")

            time.sleep(10)

    except KeyboardInterrupt:
        print("\n[🛑] Orchestrator stopped by user. Shutting down...")