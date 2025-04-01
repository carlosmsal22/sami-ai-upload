import matplotlib.pyplot as plt

def plot_group_bars(df):
    try:
        cols = df.columns[1:]
        x = df.iloc[:, 0]
        fig, ax = plt.subplots(figsize=(10, 5))
        for col in cols:
            ax.plot(x, df[col], marker='o', label=col)
        ax.set_title("Group Differences")
        ax.set_xlabel("Questions")
        ax.set_ylabel("Values")
        ax.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    except Exception as e:
        raise RuntimeError(f"Error generating chart: {str(e)}")