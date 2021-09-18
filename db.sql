-- Check number of rows in Fraud table
SELECT count(*) AS row_count FROM "Fraud"; -- 1,011

-- Check number of rows in Transactions table
SELECT count(*) AS row_count FROM "Transactions"; -- 500,000

-- Check if any entries in the Transactions table contain a credit card number that starts with 98 (invalid)
SELECT count(*) AS row_count FROM "Transactions" WHERE "credit_card_number" LIKE '98%' -- 0

-- Check how many entries in the Transactions table contain a credit card number that is not in the Fraud table
SELECT count(*) AS row_count FROM "Transactions"
WHERE "credit_card_number" NOT IN (SELECT "credit_card_number" FROM "Fraud") -- 498,989

-- Delete entries from above statement
DELETE FROM "Transactions" WHERE "credit_card_number" NOT IN (SELECT "credit_card_number" FROM "Fraud")

-- Check if entries were deleted
SELECT count(*) AS row_count FROM "Transactions"
WHERE "credit_card_number" NOT IN (SELECT "credit_card_number" FROM "Fraud") -- 0