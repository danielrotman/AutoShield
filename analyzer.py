import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title.center(58)} ")
    print("=" * 60)


def run_advanced_security_analysis():
    db = connect_to_db()
    cursor = db.cursor()

    print_header("🧠 SECURITY ANALYZER v2.0 - STARTING CYCLE")

    # הגדרת השאילתות לכל סוגי התקיפות
    threat_queries = {
        "DDoS (Volume)": """
                         SELECT source_ip, COUNT(*)
                         FROM Network_Traffic
                         GROUP BY source_ip
                         HAVING (COUNT(*) - (SELECT AVG(c)
                                             FROM (SELECT COUNT(*) as c FROM Network_Traffic GROUP BY source_ip) as s))
                                    / (SELECT STD(c)
                                       FROM (SELECT COUNT(*) as c FROM Network_Traffic GROUP BY source_ip) as s2) > 2;
                         """,
        "Port Scan (Breadth)": """
                               SELECT source_ip, COUNT(DISTINCT port_number)
                               FROM Network_Traffic
                               GROUP BY source_ip
                               HAVING (COUNT(DISTINCT port_number) - (SELECT AVG(c)
                                                                      FROM (SELECT COUNT(DISTINCT port_number) as c
                                                                            FROM Network_Traffic
                                                                            GROUP BY source_ip) as s))
                                          / (SELECT STD(c)
                                             FROM (SELECT COUNT(DISTINCT port_number) as c
                                                   FROM Network_Traffic
                                                   GROUP BY source_ip) as s2) > 3;
                               """,
        "Brute Force (Depth)": """
                               SELECT source_ip, COUNT(*)
                               FROM Network_Traffic
                               WHERE port_number = 22
                               GROUP BY source_ip
                               HAVING (COUNT(*) - (SELECT AVG(c)
                                                   FROM (SELECT COUNT(*) as c
                                                         FROM Network_Traffic
                                                         WHERE port_number = 22
                                                         GROUP BY source_ip) as s))
                                          / (SELECT STD(c)
                                             FROM (SELECT COUNT(*) as c
                                                   FROM Network_Traffic
                                                   WHERE port_number = 22
                                                   GROUP BY source_ip) as s2) > 2;
                               """
    }

    anomalies_found = 0

    for threat_name, query in threat_queries.items():
        print(f"[*] Checking for {threat_name}...")
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for (ip, score) in results:
                anomalies_found += 1
                print(f"   🚨 ALERT: {threat_name} detected! Source IP: {ip} | Score: {score}")
                # תיוג האנומליה ב-DB
                cursor.execute("UPDATE Network_Traffic SET is_anomaly = 1 WHERE source_ip = %s", (ip,))
        else:
            print(f"   ✅ {threat_name}: Status Normal.")

    db.commit()

    print("-" * 60)
    if anomalies_found > 0:
        print(f"🚩 SUMMARY: Analysis complete. {anomalies_found} threats identified and tagged.")
    else:
        print("🟢 SUMMARY: Analysis complete. No threats detected.")
    print("=" * 60 + "\n")

    db.close()


if __name__ == "__main__":
    run_advanced_security_analysis()