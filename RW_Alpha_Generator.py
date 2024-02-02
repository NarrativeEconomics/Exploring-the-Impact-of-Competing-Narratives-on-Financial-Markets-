import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Load the I values from the CSV
df = pd.read_csv('RW_I_values.csv')
df['Day'] = pd.to_datetime(df['Day'])

# Parameter for alpha computation
k_alpha_p = 0.6 # proportionality constant
k_alpha_n = 0.6
# Compute the alpha dynamics
# As we're using discrete data, we'll compute the differences
df['dalpha_p'] = k_alpha_p * df['I_p'].diff().fillna(0)
df['dalpha_n'] = k_alpha_n * df['I_n'].diff().fillna(0)

# Integrate to get alpha values with an initial value of 0.68
initial_value = 0.9
df['alpha_p'] = df['dalpha_p'].cumsum() + initial_value
df['alpha_n'] = df['dalpha_n'].cumsum() + initial_value

# Save the alpha values to a CSV
alpha_df = df[['Day', 'alpha_p', 'alpha_n']]
alpha_df.to_csv('RW_alpha_values.csv', index=False)


plt.figure(figsize=(10, 6))

# Plotting Bullish Alpha Dynamics in blue
plt.plot(df['Day'], df['alpha_p'], label=r'$\alpha_p$ - Bullish Alpha Dynamics', color='blue')

# Plotting Bearish Alpha Dynamics in red
plt.plot(df['Day'], df['alpha_n'], label=r'$\alpha_n$ - Bearish Alpha Dynamics', color='red')

plt.title('Alpha Dynamics over Time')
plt.xlabel('Day')
plt.ylabel('Alpha Value')

# Set major locator to year and formatter to just show the year
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()  # This ensures the figure layout fits well
plt.show()
