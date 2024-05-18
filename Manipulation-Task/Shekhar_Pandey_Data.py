# To execute this file, use Google Colab

import pandas as pd
from google.colab import files


csvdata = files.upload()


# Read CSV file into a DataFrame
df = pd.read_csv('test.csv')

# Calculate average salary
average_salary = df['Salary'].mean()
print(f"Average Salary: ${average_salary:.2f}")

# Find top 3 earners
top_earners = df.nlargest(3, 'Salary')[['Name', 'Salary']]
print("\nTop Earners:")
print(top_earners.to_string(index=False))
