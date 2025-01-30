import pandas as pd
import plotly.express as px
import re
import os
import logging
from collections import Counter
from datetime import datetime

# Setup Logging
cwd = os.getcwd()
LOG_PATH = os.path.join(cwd, "tmp/airflow_logs")
LOG_FILE = os.path.join(LOG_PATH, "cleaning_errors.log")
DATA_FILE = os.path.join(cwd, "my_airflow_project/data/corrupted_retail_sales_dataset.csv")
DASHBOARD_FILE = os.path.join(cwd, "tmp/error_summary.html")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to count total rows in dataset
def source_data_length(file_path):
    """Returns the total number of rows in the dataset."""
    if not os.path.exists(file_path):
        logging.error(f"❌ Source data file not found: {file_path}")
        raise FileNotFoundError(f"Source data file not found: {file_path}")

    df = pd.read_csv(file_path)
    return len(df)

# Function to summarize errors
def summarize_errors():
    """Reads cleaning_errors.log and summarizes error counts."""
    
    if not os.path.exists(LOG_FILE):
        logging.error(f"❌ Log file not found: {LOG_FILE}")
        raise FileNotFoundError(f"Log file not found: {LOG_FILE}")

    logging.info(f"🔍 Processing log file: {LOG_FILE}")

    error_patterns = {
        'Missing Customer ID': re.compile(r'Missing Customer ID'),
        'Invalid Date format': re.compile(r'Invalid Date format'),
        'Incorrect Total Amount': re.compile(r'Incorrect Total Amount')
    }

    error_counts = Counter()
    
    with open(LOG_FILE, 'r') as file:
        for line in file:
            for error_type, pattern in error_patterns.items():
                if pattern.search(line):
                    error_counts[error_type] += 1

    total_rows = source_data_length(DATA_FILE)
    total_errors = sum(error_counts.values())
    error_counts['Valid Data'] = max(0, total_rows - total_errors)

    logging.info(f"✅ Error Summary Computed: {dict(error_counts)}")
    return dict(error_counts)

# Function to generate a pie chart
def visualize_error_logs(error_summary):
    """Generates an error summary dashboard (HTML Pie Chart)."""
    
    if not error_summary:
        logging.error("❌ No error summary available.")
        raise ValueError("Error summary not found.")

    error_summary_df = pd.DataFrame(error_summary.items(), columns=['Error Type', 'Count'])
    
    fig = px.pie(error_summary_df, names='Error Type', values='Count', title='Error Summary')
    fig.write_html(DASHBOARD_FILE)

    logging.info(f"✅ Dashboard saved at {DASHBOARD_FILE}")

# Main Execution
if __name__ == "__main__":
    # Run the sequence of functions
    error_summary = summarize_errors()
    visualize_error_logs(error_summary)

    print("✅ Error visualization completed. Check logs for details.")
