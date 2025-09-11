import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("iris")

print("First 5 rows of the dataset:")
print(df.head())

print("\nData types of each column:")
print(df.dtypes)

print("\nCheck for missing values:")
print(df.isnull().sum())

df_cleaned = df.dropna()
print("\nAfter cleaning, first 5 rows:")
print(df_cleaned.head())

print("\nBasic statistics of numerical columns:")
print(df.describe())

# Line chart
plt.figure(figsize=(8,5))
plt.plot(df.index, df["sepal_length"], label="Sepal Length", color="blue")
plt.title("Line Chart: Sepal Length over Index (as Time)")
plt.xlabel("Index (as Time)")
plt.ylabel("Sepal Length (cm)")
plt.legend()
plt.show()

# Bar chart
avg_petal = df.groupby("species")["petal_length"].mean()
plt.figure(figsize=(8,5))
avg_petal.plot(kind="bar", color=["skyblue","lightgreen","salmon"])
plt.title("Bar Chart: Average Petal Length per Species")
plt.xlabel("Species")
plt.ylabel("Average Petal Length (cm)")
plt.show()

# Histogram
plt.figure(figsize=(8,5))
plt.hist(df["sepal_width"], bins=15, color="purple", alpha=0.7, edgecolor="black")
plt.title("Histogram: Distribution of Sepal Width")
plt.xlabel("Sepal Width (cm)")
plt.ylabel("Frequency")
plt.show()

# Scatter plot
plt.figure(figsize=(8,5))
for species in df["species"].unique():
    subset = df[df["species"] == species]
    plt.scatter(subset["sepal_length"], subset["petal_length"], label=species, alpha=0.7)
plt.title("Scatter Plot: Sepal Length vs Petal Length")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Petal Length (cm)")
plt.legend(title="Species")
plt.show()
