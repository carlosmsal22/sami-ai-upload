import pandas as pd
from scipy import stats

def run_group_comparison(df, group1, group2):
    """Compare two groups statistically"""
    result = pd.DataFrame({
        'Metric': ['Mean', 'Std Dev', 'Count'],
        group1: [df[group1].mean(), df[group1].std(), len(df[group1])],
        group2: [df[group2].mean(), df[group2].std(), len(df[group2])],
        'Difference': [
            df[group1].mean() - df[group2].mean(),
            df[group1].std() - df[group2].std(),
            len(df[group1]) - len(df[group2])
        ]
    })
    return result

def run_z_chi_tests(df):
    """Run statistical tests on dataframe"""
    results = []
    for col in df.select_dtypes(include=['number']).columns:
        if df[col].nunique() > 1:  # Only run if there's variation
            z_score = stats.zscore(df[col])
            results.append({
                'Column': col,
                'Test': 'Z-score',
                'Mean': z_score.mean(),
                'Std Dev': z_score.std()
            })
    return pd.DataFrame(results)

def get_descriptive_stats(df):
    """Get enhanced descriptive statistics"""
    return df.describe(include='all')
