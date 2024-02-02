import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Market Mood Data
df = pd.read_csv('RW_market_mood.csv')
df['Day'] = pd.to_datetime(df['Day'])

# Parameters
I_0 = 0.1  # basal opinion drive
U_r = 0.1  # sensitivity thresholds for bullish investors
L_r = 0.1
U_n = 0.1   # sensitivity thresholds for bearish investors
L_n = 0.1

def f(x, U, L):
    """Function to represent the 'dead zone' or threshold region"""
    if x >= U:
        return x - U
    elif -L < x < U:
        return 0
    else:
        return x + L

# Calculate I_r(t) and I_n(t) using the equations provided
df['I_p'] = df['Market_Mood'].apply(lambda x: f(x + I_0, U_r, L_r))
df['I_n'] = df['Market_Mood'].apply(lambda x: f(-x - I_0, U_n, L_n))

# Save I_r and I_n to a CSV
I_df = df[['Day', 'I_p', 'I_n']]
I_df.to_csv('RW_I_values.csv', index=False)


# Assuming df is already defined with your data

#plt.style.use('classic')
plt.figure(figsize=(10, 6))

# Plotting Bullish Investor Sentiment Influence in blue
plt.plot(df['Day'], df['I_p'], label=r'$I_p(t)$ ', color='blue')

# Plotting Bearish Investor Sentiment Influence in red
plt.plot(df['Day'], df['I_n'], label=r'$I_n(t)$', color='red')

plt.title('Investor Sentiment Influence over Time')
plt.xlabel('Day')
plt.ylabel('Sentiment Influence Value')



# Set major locator to year and formatter to just show the year
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()