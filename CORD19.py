import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import streamlit as st

df = pd.read_csv("metadata.csv")

print("First 5 rows:")
print(df.head())

print("\nDataFrame dimensions:", df.shape)
print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum().head(20))

print("\nBasic statistics (numerical):")
print(df.describe())

missing_summary = df.isnull().mean().sort_values(ascending=False)
print("\nMissing value ratio per column:")
print(missing_summary.head(20))

important_cols = ["title", "abstract", "publish_time", "journal", "source_x"]
df_cleaned = df[important_cols].dropna(subset=["title", "publish_time"])

df_cleaned["publish_time"] = pd.to_datetime(df_cleaned["publish_time"], errors="coerce")
df_cleaned = df_cleaned.dropna(subset=["publish_time"])

df_cleaned["year"] = df_cleaned["publish_time"].dt.year

df_cleaned["abstract_word_count"] = df_cleaned["abstract"].fillna("").apply(lambda x: len(x.split()))

papers_by_year = df_cleaned["year"].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.lineplot(x=papers_by_year.index, y=papers_by_year.values)
plt.title("Number of Publications Over Time")
plt.xlabel("Year")
plt.ylabel("Paper Count")
plt.show()

top_journals = df_cleaned["journal"].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top Journals Publishing COVID-19 Research")
plt.xlabel("Paper Count")
plt.ylabel("Journal")
plt.show()

titles = " ".join(df_cleaned["title"].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)

plt.figure(figsize=(12,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

plt.figure(figsize=(10,5))
sns.countplot(y="source_x", data=df_cleaned, order=df_cleaned["source_x"].value_counts().head(10).index)
plt.title("Top Sources of Papers")
plt.xlabel("Paper Count")
plt.ylabel("Source")
plt.show()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv", low_memory=False)
    df = df[["title", "abstract", "publish_time", "journal", "source_x"]].dropna(subset=["title", "publish_time"])
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df = df.dropna(subset=["publish_time"])
    df["year"] = df["publish_time"].dt.year
    df["abstract_word_count"] = df["abstract"].fillna("").apply(lambda x: len(x.split()))
    return df

df = load_data()

st.title("CORD-19 Metadata Explorer")
st.write("Explore COVID-19 research metadata interactively.")

st.subheader("Sample Data")
st.write(df.head())

year_range = st.slider("Select publication year range", int(df["year"].min()), int(df["year"].max()), (2019, 2021))
filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

st.subheader("Publications Over Time")
papers_by_year = filtered["year"].value_counts().sort_index()
st.line_chart(papers_by_year)

st.subheader("Top Journals")
top_journals = filtered["journal"].value_counts().head(10)
st.bar_chart(top_journals)

st.subheader("Word Cloud of Titles")
titles = " ".join(filtered["title"].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)
