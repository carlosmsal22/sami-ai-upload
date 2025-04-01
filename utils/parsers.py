import pandas as pd

def parse_crosstab_file(uploaded_file):
    df = pd.read_excel(uploaded_file, header=None)

    # Automatically detect header row
    header_row_index = df[df.apply(lambda row: row.astype(str).str.contains("Total", case=False).any(), axis=1)].index.min()

    if pd.isna(header_row_index):
        raise ValueError("Could not locate header row with 'Total' in it.")

    df.columns = df.iloc[header_row_index]
    df = df.drop(index=range(0, header_row_index + 1)).reset_index(drop=True)

    # Drop empty rows/columns
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    # Rename first column to "Question" for clarity
    df.rename(columns={df.columns[0]: "Question"}, inplace=True)

    return df
