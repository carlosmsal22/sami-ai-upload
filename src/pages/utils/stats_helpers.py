
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind

def run_group_comparison(df, col1, col2):
    try:
        return df[[col1, col2]]
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

def run_z_chi_tests(df):
    try:
        table = df.select_dtypes(include=[np.number])
        chi2, p, dof, expected = chi2_contingency(table.values)
        return pd.DataFrame({
            "Chi2 Statistic": [chi2],
            "p-value": [p],
            "Degrees of Freedom": [dof]
        })
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})

def get_descriptive_stats(df):
    try:
        numeric = df.select_dtypes(include=[np.number])
        desc = numeric.describe().T
        desc["median"] = numeric.median()
        return desc
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})
