import pandas as pd

def parse_crosstab_file(uploaded_file):
    return pd.read_excel(uploaded_file)
