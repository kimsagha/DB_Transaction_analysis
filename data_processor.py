import pandas as pd
import database


class Processor:
    def __init__(self):
        self.transactions = None
        self.db = None
        self.iin_ranges = None
        self.fraud_transac = None

    def initialise_processor(self):
        self.load_transactions()
        self.get_db()
        self.get_vendor_info()

    def load_transactions(self):
        print('Loading transaction data...')
        transactions_1 = pd.read_csv(r'Data/transaction_001',
                                     names=['credit_card_number', 'ipv4', 'state'], skiprows=[0])
        transactions_2 = pd.read_csv(r'Data/transaction_002',
                                     names=['credit_card_number', 'ipv4', 'state'], skiprows=[0])
        transactions = transactions_1.append(transactions_2, ignore_index=True)
        self.transactions = transactions
        print(transactions.head(5))
        # print(transactions.tail(5))
        print(transactions.shape)

    def get_db(self):
        postgres_db = database.Database()
        postgres_db.setup_db()
        self.db = postgres_db

    def get_vendor_info(self):
        maestro = ['5018', '5020', '5038', '56##']
        mastercard = ['51', '52', '54', '55', '222%']
        visa = ['4']
        amex = ['34', '37']
        discover = ['6011', '65']
        diners = ['300', '301', '304', '305', '36', '38']
        jcb16 = ['35']
        jcb15 = ['2131', '1800']

        vendor_dict = {"vendor": [], "prefix": []}
        for i in maestro:
            vendor_dict["vendor"].append('maestro')
            vendor_dict["prefix"].append(i)
        for i in mastercard:
            vendor_dict["vendor"].append('mastercard')
            vendor_dict["prefix"].append(i)
        for i in visa:
            vendor_dict["vendor"].append('visa')
            vendor_dict["prefix"].append(i)
        for i in amex:
            vendor_dict["vendor"].append('amex')
            vendor_dict["prefix"].append(i)
        for i in discover:
            vendor_dict["vendor"].append('discover')
            vendor_dict["prefix"].append(i)
        for i in diners:
            vendor_dict["vendor"].append('diners')
            vendor_dict["prefix"].append(i)
        for i in jcb16:
            vendor_dict["vendor"].append('jcb16')
            vendor_dict["prefix"].append(i)
        for i in jcb15:
            vendor_dict["vendor"].append('jcb15')
            vendor_dict["prefix"].append(i)

        print('\nLoad vendor info with prefixes')
        iin_ranges = pd.DataFrame(data=vendor_dict)
        print(iin_ranges.head(10))
        self.iin_ranges = iin_ranges

    def sanitise_transactions(self):
        # validate transactions by dropping the rows where the credit_card_number
        # doesn't start with one of the prefixes in iin_ranges
        df_t = self.transactions
        prefixes = tuple(self.iin_ranges['prefix'].tolist())
        df_t = df_t[df_t['credit_card_number'].astype(str).str.startswith(prefixes)]
        self.transactions = df_t
        print('\nSanitised transactions successfully:')
        print(self.transactions.head(10))
        print('shape of new transactions dataframe:', self.transactions.shape)

    def get_num_fraud_transac(self):
        # find the number of rows in transaction data with credit card numbers corresponding to that of fraud data
        self.db.load_frauds()
        frauds = self.db.frauds
        # print("fraud-data shape:", frauds.shape)
        transactions = self.transactions
        fraudulent_transactions = transactions.astype(str).merge(frauds['credit_card_number'].astype(str),
                                                                 how='inner', on=['credit_card_number'])
        print('\nNumber of fraudulent transactions:', fraudulent_transactions.shape[0])
        # print(fraudulent_transactions.head(10))
        self.fraud_transac = fraudulent_transactions

        # get details on fraudulent transactions
        self.get_fraud_transac_state()
        self.get_fraud_transac_vendor()

    # Create a report of the number of fraudulent transactions per state
    def get_fraud_transac_state(self):
        fraudulent_transactions = self.fraud_transac
        state_counts = fraudulent_transactions['state'].value_counts()
        print('\nNumber of frauds per state:')
        print(state_counts)

    # Create a report of the number of fraudulent transactions per card vendor, eg: maestro => 45, amex => 78, etc...
    def get_fraud_transac_vendor(self):
        fraudulent_transactions = self.fraud_transac
        print('\nNumber of frauds per vendor:')
        ###########################

    def close_db_conn(self):
        self.db.close_db_connection()


processor = Processor()
processor.initialise_processor()
processor.sanitise_transactions()
processor.get_num_fraud_transac()
processor.close_db_conn()
