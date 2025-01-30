import pandas as pd
import logging
import os
from datetime import datetime

# Setup Logging
cwd = os.getcwd()
LOG_PATH = os.path.join(cwd, "tmp/airflow_logs")
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOG_PATH, "cleaning_errors.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Validation functions
def validate_customer_id(row):
    return not pd.isna(row['Customer ID'])

def validate_total_amount(row):
    try:
        expected_total = row['Quantity'] * float(row['Price per Unit'])
        return abs(expected_total - float(row['Total Amount'])) < 1e-3
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

# Step 1: Read Data
def read_data(file_path):
    """Reads a CSV file and returns a Pandas DataFrame."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Data file not found: {file_path}")

    logging.info(f"✅ Reading data from: {file_path}")
    return pd.read_csv(file_path)

# Step 2: Validate Data
def validate_data(df):
    """Validates the dataset and logs errors to a log file."""
    error_logs = []

    for index, row in df.iterrows():
        if not validate_customer_id(row):
            error_logs.append(f"Row {index}: Missing Customer ID")
        if not validate_data_types(row):
            error_logs.append(f"Row {index}: Data type mismatch in Quantity, Price, or Total Amount")
        if not validate_total_amount(row):
            error_logs.append(f"Row {index}: Incorrect Total Amount")
        if not validate_date_format(row['Date']):
            error_logs.append(f"Row {index}: Invalid Date format ({row['Date']})")

    # Write errors to log file
    with open(LOG_FILE, "a") as log_f:
        for error in error_logs:
            log_f.write(error + "\n")
            logging.info(error)

    logging.info("✅ Data validation completed. Errors logged.")

# Step 3: Summarize Logs
def summarize_logs():
    """Reads the error log file and prints a summary."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.readlines()
            logging.info(f"📝 Summary of errors: {len(logs)} issues found.")
    else:
        logging.info("✅ No errors found during validation.")

# Main Execution
if __name__ == "__main__":
    FILE_PATH = os.path.join(cwd, "my_airflow_project/data/corrupted_retail_sales_dataset.csv")

    # Run the sequence of functions
    data = read_data(FILE_PATH)
    validate_data(data)
    summarize_logs()

    print("✅ Data validation completed. Check logs for details.")
