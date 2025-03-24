import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI
import io

# ----------------------------
# Page config & branding
# ----------------------------
st.set_page_config(page_title="SAMI AI – Excel Analyzer", layout="wide")

# Sidebar: Branding + Prompt Templates
st.sidebar.image("https://nextaigeninsights.com/wp-content/uploads/2023/10/INSIGHTS-AI-LOGO-White-Transparent.png", use_column_width=True)
st.sidebar.title("💡 Prompt Templates")
st.sidebar.markdown("""
Try these to get started:
- 🔍 Find the top 5 categories by revenue
- 📊 Summarize data trends by region
- ⚖️ Compare performance across time
- 🧠 Show any outliers or unusual values
- 📈 Suggest possible correlations
""")

st.title("SAMI AI – Advanced Analytical Tool")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])
user_prompt = st.text_area("Ask a question about your uploaded file or type any data-related query:")

def parse_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        return None

def apply_filters(df):
    st.sidebar.subheader("🔍 Filter Your Data")
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    date_cols = df.select_dtypes(include="datetime").columns.tolist()

    filters = {}
    for col in cat_cols:
        options = df[col].dropna().unique().tolist()
        selected = st.sidebar.multiselect(f"{col}", options, default=options)
        if selected and set(selected) != set(options):
            filters[col] = selected

    # Optional date filtering
    if date_cols:
        for dcol in date_cols:
            date_range = pd.to_datetime(df[dcol], errors='coerce').dropna()
            if not date_range.empty:
                min_date = date_range.min()
                max_date = date_range.max()
                start, end = st.sidebar.date_input(f"Date range for {dcol}", [min_date, max_date])
                filters[dcol] = (start, end)

    filtered_df = df.copy()
    for col, val in filters.items():
        if isinstance(val, tuple):  # date
            filtered_df = filtered_df[
                (pd.to_datetime(filtered_df[col]) >= pd.to_datetime(val[0])) &
                (pd.to_datetime(filtered_df[col]) <= pd.to_datetime(val[1]))
            ]
        else:
            filtered_df = filtered_df[filtered_df[col].isin(val)]

    return filtered_df

def generate_basic_chart(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        st.subheader("📊 Auto-Generated Chart")
        fig, ax = plt.subplots()
        df[numeric_cols[:2]].plot(kind='bar', ax=ax)
        st.pyplot(fig)

def summarize_data(df):
    st.subheader("📈 Summary Statistics")
    summary = df.describe(include='all').transpose()
    st.dataframe(summary)
    csv = summary.to_csv().encode('utf-8')
    st.download_button("Download Summary CSV", data=csv, file_name="summary_stats.csv", mime='text/csv')
    return summary.to_string()

def show_grouped_insights(df):
    st.subheader("📊 Grouped Insights")
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    if not cat_cols or not num_cols:
        st.info("Grouped insights require at least one categorical and one numeric column.")
        return None, None, None, None

    cat_col = st.selectbox("Group by (categorical column):", cat_cols, key="cat_col")
    num_col = st.selectbox("Aggregate (numeric column):", num_cols, key="num_col")
    agg_func = st.selectbox("Aggregation method:", ["mean", "sum", "count"], key="agg_func")

    grouped_df = None
    if st.button("Generate Grouped Insights"):
        grouped_df = df.groupby(cat_col)[num_col].agg(agg_func).reset_index()
        st.dataframe(grouped_df)

        fig, ax = plt.subplots()
        grouped_df.plot(x=cat_col, y=num_col, kind="bar", ax=ax, legend=False)
        plt.ylabel(f"{agg_func} of {num_col}")
        st.pyplot(fig)

        csv = grouped_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Grouped Data CSV", data=csv, file_name="grouped_data.csv", mime='text/csv')

    return grouped_df.to_string(index=False) if grouped_df is not None else "", cat_col, num_col

if st.button("Analyze"):
    if uploaded_file:
        try:
            df = parse_file(uploaded_file)
            file_info = f"The uploaded file contains {df.shape[0]} rows and {df.shape[1]} columns."
            df_filtered = apply_filters(df)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()
    else:
        st.warning("Please upload a file to begin.")
        st.stop()

    summary_text = summarize_data(df_filtered)
    keywords = ['chart', 'graph', 'visual', 'compare', 'trend']
    if any(kw in user_prompt.lower() for kw in keywords):
        try:
            generate_basic_chart(df_filtered)
        except Exception as e:
            st.warning("Chart generation failed.")

    grouped_str, cat_col, num_col = show_grouped_insights(df_filtered)
    insight_output = ""

    if df_filtered is not None:
        system_parts = [
            f"You are SAMI AI, an advanced analytics assistant.",
            file_info,
            f"Filtered data has {df_filtered.shape[0]} rows.",
            f"Summary statistics:\n{summary_text}"
        ]
        if grouped_str:
            system_parts.append(f"Grouped result for {cat_col} vs {num_col}:\n{grouped_str}")
        system_prompt = "\n\n".join(system_parts)

        try:
            with st.spinner("Generating GPT insight..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                insight_output = response.choices[0].message.content
                st.markdown(insight_output)

                # Offer download
                txt_bytes = insight_output.encode('utf-8')
                st.download_button("Download GPT Insight", txt_bytes, file_name="gpt_insight.txt", mime='text/plain')
        except Exception as e:
            st.error(f"API error: {e}")

# ----------------------------
# Correlation Matrix Section
# ----------------------------
def show_correlation_matrix(df):
    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.shape[1] < 2:
        st.info("Need at least 2 numeric columns to compute correlation.")
        return None

    st.subheader("📊 Correlation Matrix")
    corr = numeric_cols.corr()
    st.dataframe(corr.round(2))

    import seaborn as sns
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    return corr.to_string()

# ----------------------------
# PCA Visualization Section
# ----------------------------
def run_pca(df):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    numeric_cols = df.select_dtypes(include='number')
    if numeric_cols.shape[1] < 2:
        st.info("Need at least 2 numeric columns for PCA.")
        return None

    st.subheader("🔎 Principal Component Analysis (PCA)")

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    color_by = st.selectbox("Color PCA points by (optional category):", ["None"] + cat_cols)

    df_clean = numeric_cols.dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df_clean)

    pca = PCA(n_components=2)
    pcs = pca.fit_transform(scaled)
    pca_df = pd.DataFrame(pcs, columns=["PC1", "PC2"])
    if color_by != "None" and color_by in df.columns:
        pca_df[color_by] = df.loc[df_clean.index, color_by].values

    fig, ax = plt.subplots()
    if color_by != "None" and color_by in pca_df.columns:
        for grp in pca_df[color_by].unique():
            subset = pca_df[pca_df[color_by] == grp]
            ax.scatter(subset["PC1"], subset["PC2"], label=grp, alpha=0.6)
        ax.legend()
    else:
        ax.scatter(pca_df["PC1"], pca_df["PC2"], alpha=0.6)

    ax.set_xlabel("Principal Component 1")
    ax.set_ylabel("Principal Component 2")
    st.pyplot(fig)

    explained_var = pca.explained_variance_ratio_
    st.markdown(f"**Explained Variance:** PC1: {explained_var[0]:.2%}, PC2: {explained_var[1]:.2%}")

    return f"PCA explained variance: PC1={explained_var[0]:.2%}, PC2={explained_var[1]:.2%}"

# Extend Analyze block
if uploaded_file:
    if st.button("Analyze"):
        try:
            df = parse_file(uploaded_file)
            file_info = f"The uploaded file contains {df.shape[0]} rows and {df.shape[1]} columns."
            df_filtered = apply_filters(df)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()

        summary_text = summarize_data(df_filtered)
        if any(kw in user_prompt.lower() for kw in ['chart', 'graph', 'visual', 'compare', 'trend']):
            try:
                generate_basic_chart(df_filtered)
            except Exception:
                st.warning("Chart generation failed.")

        grouped_str, cat_col, num_col = show_grouped_insights(df_filtered)

        corr_text = show_correlation_matrix(df_filtered)
        pca_text = run_pca(df_filtered)

        # GPT context building
        if df_filtered is not None:
            system_parts = [
                "You are SAMI AI, an advanced analytics assistant.",
                file_info,
                f"Filtered data has {df_filtered.shape[0]} rows.",
                f"Summary statistics:\n{summary_text}"
            ]
            if grouped_str:
                system_parts.append(f"Grouped result for {cat_col} vs {num_col}:\n{grouped_str}")
            if corr_text:
                system_parts.append(f"Correlation matrix:\n{corr_text}")
            if pca_text:
                system_parts.append(f"PCA Summary:\n{pca_text}")
            system_prompt = "\n\n".join(system_parts)

            try:
                with st.spinner("Generating GPT insight..."):
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    )
                    insight_output = response.choices[0].message.content
                    st.markdown(insight_output)
                    txt_bytes = insight_output.encode('utf-8')
                    st.download_button("Download GPT Insight", txt_bytes, file_name="gpt_insight.txt", mime='text/plain')
            except Exception as e:
                st.error(f"API error: {e}")
