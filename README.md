# Automated Open-Meteo Weather Data Collector

An automated data engineering pipeline in Python that fetches live weather metrics from the Open-Meteo REST API, stores them in a local PostgreSQL database, and runs automatically via Windows Task Scheduler.

## Tech Stack
* **Language:** Python 3.13 (`requests`, `psycopg2`, `python-dotenv`)
* **Database:** PostgreSQL (`data_collector_db`)
* **Automation:** Windows Task Scheduler (`run_collector.bat`)
* **Version Control:** Git & GitHub (`V-SURVE`)

## Setup & Execution
1. Clone the repository: