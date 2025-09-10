import pandas as pd
import glob

# Step 1: Read all CSVs in data/ folder
csv_files = glob.glob("data/*.csv")
df = pd.concat([pd.read_csv(file) for file in csv_files])

# Step 2: Filter for only pink morsel
df = df[df["product"] == "pink morsel"]

# Step 3: Calculate sales
df["sales"] = df["quantity"] * df["price"]

# Step 4: Keep only required fields
output_df = df[["sales", "date", "region"]]

# Step 5: Save output
output_df.to_csv("formatted_output.csv", index=False)

print("The formatted_output.csv created successfully!")
