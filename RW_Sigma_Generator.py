import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



def nonlinear_mapping(x):
    sigmoid_value = 1 / (1 + np.exp(-x))

    if (x >= -1 and x <= -0.8) or (x <= 1 and x >= 0.8):
        return sigmoid_value
    elif x > -0.8 and x < 0.8:
        return -sigmoid_value
    return 0



# Load the data with 'Day', 'I_r', and 'I_n' columns
df = pd.read_csv('RW_I_values.csv')
df['Day'] = pd.to_datetime(df['Day'])
# Define the proportionality constants for each group
K_sigma_p = 1
K_sigma_n = 1

# Lists to store sigma values for each group
sigma_p_values = [-1]
sigma_n_values = [-1]

# Perform Euler integration to obtain sigma values for each group
for i in range(1, len(df)):
    dsigma_p = K_sigma_p * nonlinear_mapping(df['I_p'][i])
    dsigma_n = K_sigma_n * nonlinear_mapping(df['I_n'][i])

    new_sigma_p = sigma_p_values[-1] + dsigma_p
    new_sigma_n = sigma_n_values[-1] + dsigma_n

    #sigma_p_values.append(new_sigma_p)
    #sigma_n_values.append(new_sigma_n)

    sigma_p_values.append(min(1, max(-1, new_sigma_p)))
    sigma_n_values.append(min(1, max(-1, new_sigma_n)))

output_df = pd.DataFrame({
    'Day': df['Day'],
    'sigma_p': sigma_p_values,
    'sigma_n': sigma_n_values
})

output_df.to_csv('RW_sigma_values.csv')
# Plot the results directly
plt.figure(figsize=(10, 5))

# Plotting sigma_p in blue
plt.plot(pd.to_datetime(output_df['Day']), output_df['sigma_p'], '-o', label=r'$\sigma_p$', color='blue')

# Plotting sigma_n in red
plt.plot(pd.to_datetime(output_df['Day']), output_df['sigma_n'], '-o', label=r'$\sigma_n$', color='red')

plt.xticks(rotation=45)

plt.legend()
plt.ylabel('$\sigma$ Values')
plt.grid(True)
plt.tight_layout()
plt.show()
