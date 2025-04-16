import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Page configuration
st.set_page_config(page_title="Automobile Data Cleaning", layout="wide")

st.title("🚗 Automobile Dataset - Data Cleaning and Preprocessing")
st.markdown("By **MD ARSHAD KHAN** | Banner ID: 001413634")

# Load data
st.subheader("🔗 Load Data from URL")
url = "https://raw.githubusercontent.com/klamsal/Fall2024Exam/refs/heads/main/auto.csv"
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
           "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
           "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
           "peak-rpm","city-mpg","highway-mpg","price"]

df = pd.read_csv(url, names=headers)

st.dataframe(df.head(), use_container_width=True)

# Replace "?" with NaN
df.replace("?", np.nan, inplace=True)

# Count missing values
st.subheader("🔍 Missing Values Count")
missing_counts = df.isnull().sum()
st.write(missing_counts[missing_counts > 0])

# Replace by mean
for col in ["normalized-losses", "bore", "stroke", "horsepower", "peak-rpm"]:
    df[col] = df[col].astype(float)
    mean_val = df[col].mean()
    df[col].replace(np.nan, mean_val, inplace=True)

# Replace by frequency
df["num-of-doors"].replace(np.nan, df["num-of-doors"].value_counts().idxmax(), inplace=True)

# Drop rows with missing price
df.dropna(subset=["price"], axis=0, inplace=True)
df["price"] = df["price"].astype(float)

# Reset index
df.reset_index(drop=True, inplace=True)

# Convert data types
df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df["normalized-losses"] = df["normalized-losses"].astype("int")
df["peak-rpm"] = df["peak-rpm"].astype("float")

st.subheader("✅ Data After Cleaning")
st.dataframe(df.head(), use_container_width=True)

# Standardization
st.subheader("🔄 Convert MPG to L/100km")
df["city-L/100km"] = 235 / df["city-mpg"]
df["highway-L/100km"] = 235 / df["highway-mpg"]
st.dataframe(df[["city-mpg", "city-L/100km", "highway-mpg", "highway-L/100km"]].head(), use_container_width=True)

# Normalization
st.subheader("📊 Normalize 'length', 'width', 'height'")
for col in ["length", "width", "height"]:
    df[col] = df[col].astype(float)
    df[col] /= df[col].max()

st.dataframe(df[["length", "width", "height"]].head(), use_container_width=True)

# Binning Horsepower
st.subheader("🧱 Binning Horsepower into 3 categories")
df["horsepower"] = df["horsepower"].astype(int)
bins = np.linspace(df["horsepower"].min(), df["horsepower"].max(), 4)
group_names = ["Low", "Medium", "High"]
df["horsepower-binned"] = pd.cut(df["horsepower"], bins, labels=group_names, include_lowest=True)

# Histogram of horsepower
fig, ax = plt.subplots()
ax.hist(df["horsepower"], bins=10, color="skyblue", edgecolor="black")
ax.set_xlabel("Horsepower")
ax.set_ylabel("Count")
ax.set_title("Horsepower Distribution")
st.pyplot(fig)

st.subheader("🎯 Horsepower Binned Sample")
st.dataframe(df[["horsepower", "horsepower-binned"]].head(), use_container_width=True)

st.success("✅ Data Cleaning and Preprocessing Completed!")
