import pandas as pd

def parse_crosstab_file(file) -> pd.DataFrame:
    df = pd.read_excel(file, header=0)
    if df.columns.duplicated().any():
        df.columns = [f"{col}_{i}" if df.columns.duplicated()[i] else col
                      for i, col in enumerate(df.columns)]
    return df
