import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the I values from the CSV
df = pd.read_csv('RW_I_values.csv')
df['Day'] = pd.to_datetime(df['Day'])
# Parameter for b computation
k_b_p = 1.0 # proportionality constant, can be adjusted
k_b_n = 1.0
# Compute the b dynamics using discrete differences
df['db_p'] = k_b_p * df['I_p'].diff().fillna(0)
df['db_n'] = k_b_n * df['I_n'].diff().fillna(0)


# Integrate (cumulative sum) to get b values with initial values
initial_value_b_p = 1.0 # adjust based on your needs
initial_value_b_n = 1.0  # adjust based on your needs
df['b_n'] = df['db_n'].cumsum() + initial_value_b_n
df['b_p'] = df['db_p'].cumsum() + initial_value_b_p

# Save the b values to a CSV
b_df = df[['Day', 'b_n', 'b_p']]
b_df.to_csv('RW_b_values_Positive_1.0_1.0_.csv', index=False)

# Plotting the b dynamics



plt.figure(figsize=(10, 6))

# Plotting b_n Dynamics in red
plt.plot(df['Day'], df['b_n'], label=r'$b_n$ - Dynamics', color='red')

# Plotting b_p Dynamics in blue
plt.plot(df['Day'], df['b_p'], label=r'$b_p$ - Dynamics', color='blue')

plt.title('b Dynamics over Time')
plt.xlabel('Day')
plt.ylabel('b Value')

# Set major locator to year and formatter to just show the year
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()  # This ensures the figure layout fits well
plt.show()
