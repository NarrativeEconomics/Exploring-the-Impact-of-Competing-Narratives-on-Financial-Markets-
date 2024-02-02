import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the I values from the CSV
df = pd.read_csv('I_values.csv')

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
b_df.to_csv('b_values_Positive.csv', index=False)

# Plotting the b dynamics
import matplotlib.pyplot as plt
import numpy as np



plt.figure(figsize=(10, 6))

# Plotting b_n Dynamics in red
plt.plot(df['Day'], df['b_n'], label=r'$b_n$ - Dynamics', color='red')

# Plotting b_p Dynamics in blue
plt.plot(df['Day'], df['b_p'], label=r'$b_p$ - Dynamics', color='blue')

plt.title('b Dynamics over Time')
plt.xlabel('Day')
plt.ylabel('b Value')
plt.xticks(np.arange(0, len(df['Day']), step=24), [f'Day {i+1}' for i in range(len(df['Day'])//24)], rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()  # This ensures the figure layout fits well
plt.show()
