# Error Log Analyzer
This repository contains the raw data files and scripts necessary to generate both an error log and dashboard on the `corrupted_retail_sales_dataset.csv` dataset. Below is the current file structure:
```
ErrorLogAnalyzer/
│
├── data/      
│   └── corrupted_retail_sales_dataset.csv       # Raw data files 
├── src/
│   ├── cleaning_script.py     # Script that logs errors
│   └── dashboard_colab.py     # Visualization script
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

This project is designed to read the data withing the `raw/` directory and record the type or error detected. Then based on the generated log report, a dashboard is created in order to display the frequency and type of errors detected in the dataset.

## Tasking
You will be required to automatate the creation of both the log file and dashboard file through a DAG and Apache Airflow. After getting a base file structure from the `!pip install airflowctl` command, you will combine it with your GitHub files so that it resembles below
```
.
└── my_airflow_project
  ├── \dags
  ├── \logs
  ├── \plugins
  ├── \data   
  |      └── corrupted_retail_sales_dataset.csv
  ├── \src   
  |      ├── cleaning_script.py
  |      └──dashboard_colab.py
  ├── airflow.cfg
  ├── airflow.db
  ├── requirements.txt
  ├── standalone_admin_password.txt
  ├── settings.yaml
  └── webserver_config.py
```

## Steps
1. Set your environment as described in the attatched notebook
    - link here: 
2. Use Generative AI to guide the creation of the DAG to automate
   - Calling and executing the `cleaning_script.py` to generate `cleaning_errors.log`
   - Calling and executing the `visualize_error_logs()` method from the `dashboard_colab.py` file to create the dashboard image
   - Sending an email with the summarized dashboard to a list of test users. 

## Goal
   This project helps you understand how to create and automate a data quality pipeline using Apache Airflow. You will use generative AI to build a DAG that logs errors in a retail sales dataset and visualizes the results in an interactive dashboard.
