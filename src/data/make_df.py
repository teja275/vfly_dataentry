import pandas as pd
import numpy as np


def generate_df_from_response(response, header_present=False, header=[]):
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
            header = remove_empty_elements(header)
            table_data = remove_empty_elements(table_data)
            # Converting the numpy array to dataframe
            if table_data.shape[1] > len(header):
                header = np.append(header, (table_data.shape[1]-len(header)))
            df_table = pd.DataFrame(table_data, columns=header, dtype=str)
        return df_table
    else:
        print("HTTP request failed with status code:", response.status_code)


def rename_dob_columns(df_table):
    df_table.columns = [
        f"{col}_{i}" if col == "DOB" else col for i, col in enumerate(df_table.columns)
    ]
    return df_table


def clean_dob_columns(df_table):
    # Format 'DOB' columns as 'MM/DD/YYYY' and output as string
    for col in df_table.columns:
        # if col.startswith('DOB'):
        #     df_table[col] = pd.to_datetime(df_table[col], format='%d/%m/%Y').dt.strftime('%-d/%-m/%Y')
        if col == "DOB_5":
            df_table[col] = pd.to_datetime(
                df_table[col], format="%d/%m/%Y", errors="ignore"
            ).dt.strftime("%-d/%-m/%Y")
        if col == "DOB_21":
            df_table[col] = pd.to_datetime(
                df_table[col], format="%m/%d/%Y", errors="ignore"
            ).dt.strftime("%-m/%-d/%Y")
    return df_table


def revert_dob_column_names(df_table):
    df_table.columns = [
        "DOB" if col.startswith("DOB") else col for col in df_table.columns
    ]
    return df_table


def remove_empty_elements(array, axis=0):
    if array.ndim == 1:
        return array[array != '']
    elif array.ndim == 2:
        if axis == 0:
            return array[:, ~np.all(array == '', axis=axis)]
        elif axis == 1:
            return array[~np.all(array == '', axis=axis), :]
    else:
        raise ValueError("Input array must be 1-D or 2-D.")


def get_cleaned_df(response, header_present, header):
    df_table = generate_df_from_response(response, header_present, header)
    # df_table = rename_dob_columns(df_table)
    # df_table = clean_dob_columns(df_table)
    # df_table = revert_dob_column_names(df_table)
    return df_table


if __name__ == '__main__':
    # Test with a 1-D array
    arr_1d = np.array(["a", "b", "", "d", "e"])
    result_1d = remove_empty_elements(arr_1d)
    print(result_1d)  # Output: ['a' 'b' 'd' 'e']

    # Test with a 2-D array
    arr_2d = np.array([["a", "b", ""],
                       ["d", "e", ""]])
    result_2d = remove_empty_elements(arr_2d, axis=0)
    print(result_2d)
    # Output:
    # [['a' 'b']
    #  ['d' 'e']]
