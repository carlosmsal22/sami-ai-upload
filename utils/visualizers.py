import pandas as pd
import matplotlib.pyplot as plt

def plot_comparison_chart(df, question_col, group_col, value_col):
    try:
        df = df[[question_col, group_col, value_col]].dropna()
        df[group_col] = df[group_col].astype(str)
        df[question_col] = df[question_col].astype(str)
        df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
        pivot_df = df.pivot(index=question_col, columns=group_col, values=value_col)

        ax = pivot_df.plot(kind="bar", figsize=(10, 5))
        ax.set_ylabel("Value")
        ax.set_title("Group Comparison Chart")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        return ax.get_figure()
    except Exception as e:
        raise RuntimeError(f"Error generating chart: {e}")
