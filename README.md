# 🛡️ AutoShield: Autonomous Cyber War Room

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**AutoShield** is a real-time network security monitoring and automated response engine. The system is designed to simulate cyber attacks, identify behavioral deviations using statistical analysis, and execute mitigation protocols autonomously.

---

## 🚀 Key Features

* **Multi-threaded Attack Simulator:** Simulates various threat vectors including **DDoS (High Volume)**, **Brute Force (SSH)**, and **Port Scanning** simultaneously.
* **Intelligent Threat Detection:** Utilizes **Z-Score statistical analysis** to identify significant traffic deviations from the established baseline.
* **Active Response Engine:**
    * **Dynamic Blacklisting:** Automatically blocks malicious IPs with specific reasoning (e.g., "Brute Force Attack").
    * **Traffic Management:** Redirects traffic to optimal assets based on current server load and asset importance scores.
* **Secure Configuration:** Fully integrated with environment variables (`.env`) to ensure sensitive credentials remain protected.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Database:** MySQL (Relational Data Modeling)
* **Concurrency:** Python `threading` for simultaneous simulation and analysis.
* **Security:** `python-dotenv` for environment isolation.

---

## 🏗️ System Architecture



The system operates in three main layers:
1.  **Simulation Layer:** Generates both legitimate and malicious traffic.
2.  **Analysis Layer:** Queries the traffic database and identifies threats based on statistical thresholds.
3.  **Mitigation Layer:** Executes SQL-based enforcement rules to block threats and balance the network load.

---

## ⚙️ Installation & Setup

To get AutoShield running on your machine, clone the repository with git clone https://github.com/danielrotman/AutoShield.git, install all required dependencies by running pip install -r requirements.txt, and ensure your MySQL server is active with the CyberWarRoom schema initialized before finally creating a .env file in the root directory to define your DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME credentials.
