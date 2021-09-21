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

### Process
1. Host a PostgreSQL database via Docker
2. Manipulate and interact with db via DataGrip to quickly try out SQL statements and check the connection
3. Connect to the db via PyCharm DB Browser
4. Create a class for the database in the program
5. Define instance variables for the database class: the connection (so it can be maintained) and the fraud data on the db
6. Create functions for specific db-related tasks, each with its own cursor to execute SQL statements
7. Create a database processor class, instantiated with variables to use in its functions, transactions, db and fraud data
8. Create functions to process the transaction data based on the fraud data in the db
9. Main functions include:
   - Sanitise data
   - Find fraudulent transactions
   - Mask transactions and save in new files (JSON and binary format)
  
10. Instantiate processor which uses db to process data
11. Send output from terminal to file

#### Questions
1. What would be best practice? Have an SQL file with all statements or divide them up into functions in a python file
2. Is DataGrip a good option for DB management or is it more efficient to just use PyCharm?
3. Should I have stored the transaction data in the db as well?
4. Is the Luhn algorithm a save and effective option for credit card number validation?
5. Is it best practice to stop docker image or keep running constantly?
6. In what format should the masked files have been stored?