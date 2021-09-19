import pandas as pd
import psycopg2
import csv


class Database:
    def __init__(self):
        self.connection = None

    # connect to PostgreSQL DB server and print name and version
    # creating a new connections is tedious, keep open as long as needed
    def connect_db(self):
        print("\nConnecting to PostgreSQL database...")
        try:
            connection = psycopg2.connect(
                host="localhost",
                port=5432,
                database="postgres",
                user="postgres",
                password="postgres")

            # grant permission to write to db, and automatically commit changes
            connection.set_session(readonly=False, autocommit=True)

            cursor = connection.cursor()  # create cursor to use to retrieve db details

            print('PostgreSQL database version:')
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            print(db_version)

            print('PostgreSQL database name:')
            cursor.execute('SELECT current_database()')
            db_name = cursor.fetchone()
            print(db_name)

            cursor.close()  # close cursor to free cached data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                self.connection = connection

    def create_fraud_table(self):
        with self.connection as conn1:
            cursor = conn1.cursor()
            print("\nCreating new table Fraud...")

            # first, drop table if exists
            cursor.execute('DROP TABLE IF EXISTS Fraud')

            cursor.execute("CREATE TABLE Fraud (\
                                credit_card_number TEXT NOT NULL,\
                                ipv4 TEXT NOT NULL,\
                                state TEXT,\
                                CONSTRAINT PK_Fraud PRIMARY KEY(credit_card_number))")
            print("New table Fraud created successfully")
            print('Table row-count:')
            cursor.execute('SELECT count(*) AS row_count FROM Fraud;')
            fraud_count = cursor.fetchone()
            print(fraud_count)
            cursor.close()

    # get restructure fraud data set to load into db
    @staticmethod
    def get_structured_fraud_data():
        # read in data with 3 pre-determined columns (adds empty values for rows with no state-value)
        fraud = pd.read_csv(r'Data/fraud', names=['credit_card_number', 'ipv4', 'state'], skiprows=[0])
        # print(fraud.head(10))
        # load restructured fraud data into new csv
        fraud_structured_path = 'Data/fraud_structured'
        fraud.to_csv(fraud_structured_path, index=False)
        return fraud_structured_path

    def load_fraud_data(self, path_fraud):
        load_query = "INSERT INTO Fraud VALUES (%s, %s, %s)"  # 3 strings from columns of csv
        with self.connection as conn_load:
            cursor = conn_load.cursor()
            print("\nLoading restructured fraud data into Fraud table")
            with open(path_fraud, 'r') as data:
                data_reader = csv.reader(data)
                next(data_reader)  # skip header
                for row in data_reader:  # load data line by line from csv
                    cursor.execute(load_query, row)
            cursor.close()
        print("Inserted values successfully")

    def close_db_connection(self):
        if self.connection is not None:
            self.connection.commit()  # necessary?
            self.connection.close()
            print('\nDatabase connection closed.')

    def setup_db(self):
        self.connect_db()
        self.create_fraud_table()
        path = self.get_structured_fraud_data()
        self.load_fraud_data(path)
