import pandas as pd
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(
    filename='error_logs/cleaning_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_customer_id(row):
    if pd.isna(row['Customer ID']):
        return False
    return True

def validate_total_amount(row):
    try:
        expected_total = row['Quantity'] * float(row['Price per Unit'])
        return abs(expected_total - float(row['Total Amount'])) < 1e-3  # Allow for floating-point precision
    except (ValueError, TypeError):
        return False

def validate_date_format(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_data_types(row):
    try:
        float(row['Price per Unit'])
        int(row['Quantity'])
        float(row['Total Amount'])
        return True
    except (ValueError, TypeError):
        return False

def clean_and_log_errors(file_path):
    # Read the corrupted data
    data = pd.read_csv(file_path)

    # Iterate over the data and check for issues
    for index, row in data.iterrows():
        if not validate_customer_id(row):
            logging.error(f"Row {index}: Missing Customer ID")
        if not validate_data_types(row):
            logging.error(f"Row {index}: Data type mismatch in Quantity, Price, or Total Amount")
        if not validate_total_amount(row):
            logging.error(f"Row {index}: Incorrect Total Amount (doesn't match Quantity * Price per Unit)")
        if not validate_date_format(row['Date']):
            logging.error(f"Row {index}: Invalid Date format ({row['Date']})")

if __name__ == '__main__':
    # Input file path for the corrupted data
    cwd = os.getcwd()
    file_path = 'cwd'+'/data/corrupted_retail_sales_dataset.csv'
    clean_and_log_errors(file_path)
