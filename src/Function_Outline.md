# Function Breakdown
Here’s what each function does and how it should translate into an Airflow DAG:

## error_log_functions.py 

1. `read_data(file_path)`
   - **Purpose:** Reads the CSV file and returns a Pandas DataFrame.
   - **Airflow Consideration:**
     - This should be the first task in the `DAG`.
     - The function cannot return a `Pandas DataFrame` via `XCom` (due to size limits).
     - Instead, it should pass the file path through `XCom`.
2. `validate_data(df)`
   - **Purpose:** Iterates through the dataset, checks for errors, and writes errors to a log file.
   - **Airflow Consideration:**
     - This should be the second task in the `DAG`.
     - It must retrieve the file path from `XCom`, then read and validate the file.
     - Errors must be written to a physical log file (`cleaning_errors.log`) for use in the next `DAG`.
     - In addition to writing errors to `cleaning_errors.log`, use Airflow's logging system (`logging.info()`) to log error messages for easy debugging.
3. `summarize_logs()`
   - **Purpose:** Reads the error log and prints a summary of errors found to terminal.
   - **Airflow Consideration:**
     - This should be the final task in the DAG.
     - It should retrieve the error count from XCom instead of reading a log file.
     - Log the final summary in Airflow UI logs.


### Key Concepts to Keep in Mind

**Airflow Task Order:**
1. The DAG must follow the sequence:
    - `read_data` → `validate_data` → `summarize_logs`

2. Passing Data Between Tasks:
    - `XCom` should be used to pass file paths and error counts between tasks.
    - More information on `XComs` found [here](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html)


3. **No Large Object Passing** in `XCom`:
    - Pass the file path, not the DataFrame itself.

4.  Use `PythonOperator` to Create Tasks:
    - Each function should be used as a `PythonOperator` task inside the `DAG`. 



## dashboard_functions.py

1. `summarize_errors()`
   - **Purpose:** Reads cleaning_errors.log and counts the number of errors per category.
   - **Airflow Consideration:**
     - This should be the first task in the `DAG`.
     - The function must retrieve and process `cleaning_errors.log`.
     - Instead of returning a `dictionary`, **push the error summary to XCom** so the next task can use it.
2. `visualize_error_logs(error_summary)`
   - **Purpose:** Uses the error summary to generate a pie chart as an HTML file.
   - **Airflow Consideration:**
     - This should be the second task in the `DAG`.
     - It must retrieve the error summary from `XCom`, then generate the dashboard.
     - Ensure that the HTML file (`error_summary.html`) is properly saved and log its location for debugging.
     - Push the final file path to `XCom` in case another `DAG` needs to use it.


### Key Concepts to Keep in Mind
**Airflow Task Order:**
1. The DAG must follow the sequence:
   - `summarize_errors` → `visualize_error_logs`
2. Passing Data Between Tasks:
   - Use `XCom` to pass error summary data between tasks.
   - Use `XCom` to store the file path of the visualization.
3. Airflow Logging + Physical Log File:
   - Use `logging.info()` so errors appear in Airflow UI logs.
   - Still read from `cleaning_errors.log`, since it was generated in the previous `DAG`.
4. Use `PythonOperator` to Create Tasks:
   - Each function should be used as a `PythonOperator` task inside the `DAG`.
