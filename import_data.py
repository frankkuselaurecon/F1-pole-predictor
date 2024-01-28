import pandas as pd
import os
import matplotlib.pyplot as plt

current_directory = os.path.dirname(__file__)
file_name = 'F1_data.xlsm'
file_path = os.path.join(current_directory, file_name)
df = pd.read_excel(file_path, sheet_name='Results', index_col=0)
print(df)

# Transpose the DataFrame to have race names as columns
df = df.T
print(df)

# Calculate cumulative points for each user
cumulative_points = df.cumsum()
print(cumulative_points)


# Plot cumulative points for each user
for user in cumulative_points.columns:
    final_points = cumulative_points[user].iloc[-1]  # Get the final points for the user
    if final_points >= 180:  # Grey out users with less than 150 points
        if cumulative_points[user].max() == cumulative_points.max().max():  # Check if this user has the highest points
            plt.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=3, color='black')  # Make line bold
        else:
            plt.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=2)
    else:
        plt.plot(cumulative_points.index, cumulative_points[user], color='grey', alpha=0.3)

    # Initialize previous leader
    prev_leader = None
    leader_count = {user: 1 for user in cumulative_points.columns}

    # Annotate the plot with the name of the leader for each race
    for i, race in enumerate(cumulative_points.index):
        leader = cumulative_points.loc[race].idxmax()  # Get the user with the highest points for this race
        leader_points = cumulative_points.loc[race, leader]  # Get the points of the leader for this race

        # Check if the leader has changed
        if leader != prev_leader:
            # Position the label higher above the plotting point
            plt.text(i, leader_points + 15, leader, ha='center', va='bottom', fontsize=8, color='black', rotation=0, alpha=0.1)

            # Add a leader line pointing down to the plotting point
            plt.plot([i, i], [leader_points, leader_points + 10], color='black', linestyle='-', linewidth=0.1)

            # Update the previous leader
            prev_leader = leader


# Set labels and title
plt.xlabel('Race')
plt.ylabel('Cumulative Points')
plt.title('Cumulative Points by Race for Each User')
num_races = 22
plt.xticks(range(num_races), [])
plt.ylim(0, cumulative_points.max().max()+50)
plt.xticks(rotation=90)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 8}, frameon=False)  # Adjust font size as needed
plt.tight_layout()
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.show()