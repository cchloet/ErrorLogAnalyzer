# Error Log Analyzer
This repository contains the raw data files and scripts necessary to generate both an error log and dashboard on the `corrupted_retail_sales_dataset.csv` dataset. Below is the current file structure:
```
ErrorLogAnalyzer/
│
├── \data      
│   └── corrupted_retail_sales_dataset.csv       # Raw data files 
├── \src   
│     ├── ReadMe.md        #Function Overview  
│     ├── dashboard_functions.py     # Visualization script
│     └── error_log_functions.py     # Script that logs errors
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

This project is designed to read the data withing the `data/` directory and record the type or error detected. Then based on the generated log report, a dashboard (HTML pie chart file) is created in order to display the frequency and type of errors detected in the dataset.

## Tasking
You will be required to automatate the creation of both the log file and dashboard file through a DAG and Apache Airflow. After getting a base file structure from the `!pip install airflowctl` command, you will combine it with your GitHub files so that it resembles below
```
.
└── my_airflow_project
  ├── \dags
  │     ├── example_dag_basic.py        #Example dag included in airflowctl
  │     ├── dashboardDAG.py     # Dashboard_functions file turned into a DAG
  │     └── error_logsDAG.py     # error_log_functions file turned into a DAG
  ├── \logs
  ├── \plugins
  ├── \data   
  |      └── corrupted_retail_sales_dataset.csv
  ├── airflow.cfg
  ├── airflow.db
  ├── requirements.txt
  ├── standalone_admin_password.txt
  ├── settings.yaml
  └── webserver_config.py
```

## Steps
1. Set your environment as described in the attatched notebook
2. Use Generative AI to guide the creation of the DAG to automate
   - Edit the `cleaning_script.py` to create a proper DAG which will generate `cleaning_errors.log`
   - Edit the `dashboard_colab.py` file to create a proper DAG which will create the dashboard image

## Goal
   This project helps you understand how to create and automate a data quality pipeline using Apache Airflow. You will use generative AI to build a DAG that logs errors in a retail sales dataset and visualizes the results in an interactive dashboard.
