import pandas as pd

def parse_crosstab_file(file):
    df = pd.read_excel(file)
    df = df.dropna(how="all")
    df.columns = [str(col).strip() for col in df.columns]
    row_headers = df.columns[0]
    col_headers = df.columns[1:]
    return df, row_headers, col_headers