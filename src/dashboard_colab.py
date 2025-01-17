import pandas as pd
import plotly.express as px
import re
from collections import Counter
import os

def source_data_length(file_path):
    data = pd.read_csv(file_path)
    return len(data)


def summarize_errors(log_file_path):
    error_patterns = {
        'Missing Customer ID': re.compile(r'Missing Customer ID'),
        'Invalid Date format': re.compile(r'Invalid Date format'),
        'Incorrect Total Amount': re.compile(r'Incorrect Total Amount')
    }
    
    error_counts = Counter()
    
    with open(log_file_path, 'r') as file:
        for line in file:
            for error_type, pattern in error_patterns.items():
                if pattern.search(line):
                    error_counts[error_type] += 1
    cwd = os.getcwd()
    file_path = 'cwd'+'/data/corrupted_retail_sales_dataset.csv'
    valid_rows = source_data_length(file_path)
    error_counts['Valid Data'] = valid_rows
    
    return error_counts

def visualize_error_logs(log_file_path):
    # Summarize the errors using the summarize_errors function
    error_summary = summarize_errors(log_file_path)
    
    # Convert the summary to a DataFrame
    error_summary_df = pd.DataFrame(error_summary.items(), columns=['Error Type', 'Count'])
    
    # Create an interactive pie chart
    fig = px.pie(error_summary_df, names='Error Type', values='Count', title='Error Summary')
    
    # Save the interactive chart to an HTML file
    cwd = os.getcwd()
    save_path = 'cwd'+'dashboard/error_summary.html'
    fig.write_html(save_path)

# Run the visualization
if __name__ == "__main__":
    cwd = os.getcwd()
    file_path = 'cwd'+'logs/cleaning_errors.log'
    visualize_error_logs(file_path)
