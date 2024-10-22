import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

data = pd.read_csv('hitting_stats.csv')

# Define the weights for each offensive stat, now including Stolen Bases and Walks
weights = {
    'BA': 0.25,   # 25% weight
    'HR': 0.2,    # 20% weight
    'RBI': 0.15,  # 15% weight
    'OBP': 0.1,   # 10% weight
    'SLG': 0.1,   # 10% weight
    'SB': 0.1,    # 10% weight
    'BB': 0.1     # 10% weight
}

# Filter out players who don't qualify for league stats (e.g., based on minimum plate appearances) 
data = data[data['PA'] >= 502]

# Calculate the weighted total for each player
data['WeightedTotal'] = (
    data['BA'] * weights['BA'] +
    data['HR'] * weights['HR'] +
    data['RBI'] * weights['RBI'] +
    data['OBP'] * weights['OBP'] +
    data['SLG'] * weights['SLG'] +
    data['SB'] * weights['SB'] +
    data['BB'] * weights['BB']
)

# Sort players by their weighted total score
data_sorted = data.sort_values(by='WeightedTotal', ascending=False)

# Display the top 10 players with their original column names, including 'Name'
selected_columns = ['Player', 'WeightedTotal', 'BA', 'HR', 'RBI', 'OBP', 'SLG', 'OPS', 'SB', 'TB', 'R', 'BB']

# Print top 25 players without the index
print(data_sorted[selected_columns].head(10).to_string(index=False))

# Save the top 25 players to a new CSV file
data_sorted[selected_columns].head(25).to_csv('top_players.csv', index=False)

# Create a correlation matrix using only numeric columns
numeric_columns = ['WeightedTotal', 'BA', 'HR', 'RBI', 'OBP', 'SLG', 'OPS', 'SB', 'TB', 'R', 'BB',]
correlation_matrix = data_sorted[numeric_columns].corr()

# Plot the heatmap with a smaller figure size
plt.figure(figsize=(10, 5))  # Smaller figure size
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Offensive Stats')
plt.show()

# Top 10 Players Bar Chart
fig = px.bar(data_sorted.head(15), x='Player', y='WeightedTotal',
             title='Top 10 Players by Weighted Total',
             labels={'WeightedTotal':'Weighted Total Score'})
fig.show()