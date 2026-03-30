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
        print(f"❌ Database Connection Error: {err}")
        return None


def print_mitigation_header(title):
    print("\n" + "#" * 60)
    print(f" {title.center(58)} ")
    print("#" * 60)


def run_full_mitigation():
    db = connect_to_db()
    if not db:
        return

    cursor = db.cursor()

    print_mitigation_header("🛡️  ACTIVE RESPONSE ENGINE - ENGAGED")

    # --- 1. ניתוח סיכונים לפי חשיבות הנכס (Assets) ---
    risk_query = """
                 SELECT a.asset_name, a.importance_score, COUNT(*) as attack_count
                 FROM Network_Traffic nt
                          JOIN assets a ON nt.dest_asset_id = a.id
                 WHERE nt.is_anomaly = 1
                 GROUP BY a.asset_name, a.importance_score
                 ORDER BY a.importance_score DESC;
                 """
    cursor.execute(risk_query)
    high_risks = cursor.fetchall()

    print("[📊 RISK STATUS]")
    if high_risks:
        for (name, score, count) in high_risks:
            priority = "🔴 CRITICAL" if score >= 8 else "🟡 MEDIUM"
            print(f"   [{priority}] {name} (Importance: {score}) under attack! Count: {count}")

    # --- 2. חסימה חכמה עם סיווג סיבה ---
    print("\n[*] Enforcement: Updating Blacklist with Specific Reasons...")

    cursor.execute("""
                   SELECT source_ip, MAX(port_number), MAX(packet_size_kb)
                   FROM Network_Traffic
                   WHERE is_anomaly = 1
                     AND source_ip NOT IN (SELECT blocked_ip FROM Blacklist)
                   GROUP BY source_ip
                   """)
    new_threats = cursor.fetchall()

    for (ip, port, size) in new_threats:
        # לוגיקה לסיווג סוג התקיפה
        if port == 22:
            reason = "Brute Force Attack (SSH)"
        elif size > 3000:
            reason = "DDoS Attack (High Volume)"
        else:
            reason = "Port Scanning Activity"

        insert_sql = "INSERT IGNORE INTO Blacklist (blocked_ip, reason) VALUES (%s, %s)"
        cursor.execute(insert_sql, (ip, reason))
        print(f"   🚫 IP {ip} --> Blocked for: {reason}")

    # --- 3. ניהול עומסים (Load Management) ---
    print("\n[*] Traffic Management: Calculating Optimal Route...")
    load_query = "SELECT dest_asset_id, COUNT(*) as traffic_load FROM Network_Traffic GROUP BY dest_asset_id ORDER BY traffic_load ASC LIMIT 1"
    cursor.execute(load_query)
    best_server = cursor.fetchone()

    if best_server:
        print(f"   ⚖️  Greedy Decision: Redirecting traffic to Asset ID: {best_server[0]}")

    db.commit()
    print("\n" + "#" * 60)
    print("✅ RESPONSE CYCLE COMPLETE.")
    print("#" * 60 + "\n")
    db.close()


if __name__ == "__main__":
    run_full_mitigation()