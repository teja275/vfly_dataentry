import numpy as np
import pandas as pd


def generate_df_from_response(response, header_present=False):
    if response.status_code == 200:
        response = response.json()
        # Extract the table data from the response
        data = response["result"][0]["prediction"][0]["cells"]
        # Determine the number of rows and columns
        num_rows = max(cell["row"] for cell in data)
        num_cols = max(cell["col"] for cell in data)
        # Appending data to a numpy array
        table_data = [cell["text"] for cell in data]
        table_data = np.array(table_data)
        # Reshaping the numpy array
        table_data = table_data.reshape(num_rows, num_cols)
        if header_present:
            df_table = pd.DataFrame(table_data[1:], columns=table_data[0], dtype=str)
        else:
            df_table = pd.DataFrame(table_data)
        return df_table
    else:
        print("HTTP request failed with status code:", response.status_code)
