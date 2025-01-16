import pandas as pd
import plotly.express as px
#from google.colab import files
#import os
import re
from collections import Counter

def source_data_length(file_path = 'data/raw/corrupted_retail_sales_dataset.csv'):
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
    
    valid_rows = source_data_length()
    error_counts['Valid Data'] = valid_rows
    
    return error_counts

def visualize_error_logs(log_file_path='logs/cleaning_errors.log', save_path='dashboard/error_summary.html'):
    # Summarize the errors using the summarize_errors function
    error_summary = summarize_errors(log_file_path)
    
    # Convert the summary to a DataFrame
    error_summary_df = pd.DataFrame(error_summary.items(), columns=['Error Type', 'Count'])
    
    # Create an interactive pie chart
    fig = px.pie(error_summary_df, names='Error Type', values='Count', title='Error Summary')
    
    # Save the interactive chart to an HTML file
    fig.write_html(save_path)
    fig.show()

# Run the visualization
if __name__ == "__main__":
    visualize_error_logs()
