import pandas as pd


def clean_states(df_table, state_replacements_all=None, state_replacements_col=None):
    if state_replacements_all is None:
        state_replacements_all = {"N / A": "N/A", "DK": "OK", "DH": "OH"}
    if state_replacements_col is None:
        state_replacements_col = {"L": "IL", "I": "IL", "1": "IL", "W": "WI", "A": "FL"}
    df_table = df_table.replace(state_replacements_all)
    if df_table.shape[1] == 23:
        state_columns = [7, 14, 19]
        df_table.iloc[:, state_columns] = df_table.iloc[:, state_columns].replace(
            state_replacements_col
        )
    return df_table


def clean_address(df_table, address_replacements=None):
    if address_replacements is None:
        address_replacements = {" \.": "."}
    if df_table.shape[1] == 23:
        address_columns = [3, 12, 18]
        df_table.iloc[:, address_columns] = df_table.iloc[:, address_columns].replace(
            address_replacements, regex=True
        )
    return df_table


def clean_mediclaim_number(df_table):
    if df_table.shape[1] == 23:
        mediclaim_number_column = 9
        df_table.iloc[:, mediclaim_number_column] = df_table.iloc[
            :, mediclaim_number_column
        ].apply(lambda x: x if not str(x).endswith("4") else str(x)[:-1] + "A")
    return df_table


def clean_dot_space(df_table):
    df_table = df_table.replace(" \.", ".", regex=True)
    return df_table


def clean_df(
    df_table,
    state_replacements_all=None,
    state_replacements_col=None,
    address_replacements=None,
):
    df_table = clean_states(df_table, state_replacements_all, state_replacements_col)
    df_table = clean_address(df_table, address_replacements)
    df_table = clean_mediclaim_number(df_table)
    df_table = clean_dot_space(df_table)
    return df_table


if __name__ == '__main__':
    df = pd.DataFrame({'a': ['a .', 'b .', 'c .'], 'b': ['d .', 'e .', 'f .']})
    print(df)
    df = clean_dot_space(df)
    print(df)
