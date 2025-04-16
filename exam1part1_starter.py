# Create bin edges using linspace
bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
print("Bins:", bins)

# Define the group names
group_names = ['Low', 'Medium', 'High']

# Apply the binning using `cut()`
df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True)

# Show first few rows
df[['horsepower', 'horsepower-binned']].head(10)

import seaborn as sns

sns.countplot(x="horsepower-binned", data=df)
plt.pyplot.xlabel("horsepower")
plt.pyplot.ylabel("count")
plt.pyplot.title("Horsepower Bins Distribution")
plt.pyplot.show()
