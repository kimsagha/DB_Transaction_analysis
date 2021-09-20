# Coding Challenge

### Instructions
Perform data analysis on transaction data in Python with unit testing. Setup SQL database.

### Project Setup
- Python interpreter: conda-environment with Python 3.9
- Requirements: pandas, postgres, psycopg2, testing.postgresql
- Postgres container on Docker, hosting PostgreSQL db 
  - Database name: postgres, host: localhost, port: 5432, username: postgres, password: postgres
  - Server currently stopped
  - Database Management System used: DataGrip
- Output from terminal directed to output.txt
- To run code, run data_processor.py
- To run database unit tests, run test_database.py