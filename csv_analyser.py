import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('Ethics.csv')
df.rename(columns={'As someone who is observing the scene from the sidewalk, what should the driver do?' : 'cow_p', 'What is your home country?':'country', 'For self-driving vehicles, do you believe the rules for the car deciding what action to take should be set by the government ? Or would you prefer  the car to take action based of how you think? ' : 'gove', 'You are driving this truck and suddenly a cow appears in front of you, what should you do?':'animal', 'As someone observing from the bushes, if you see the combi has lost control, what do you think the combi should do?':'pedestrian', 'You are one of the passengers of the combi, it has lost control and can perform the following actions? What is your preference?':'passenger', 'You are driving the car with your friends, which has lost control and can perform one of the following actions, which one would you prefer?': 'bicycle'}, inplace=True)
column_names = df.columns
df = df[~df['country'].isin(['u.s.', 'united states', 'united states of america', 'usa'])]

df_sorted = df.sort_values(by='country')
df_sorted.to_csv('ethics.csv', index=False)
df = df_sorted

df['country'] = df['country'].str.strip()
df['country'] = df['country'].str.lower()
df['country'] = df['country'].str.replace('usa', 'botswana')

country_counts = df['country'].value_counts()
india_count = country_counts.get('india', 0)
botswana_count = country_counts.get('botswana', 0)
print(f"Number of people from India: {india_count}")
print(f"Number of people from Botswana: {botswana_count}")

counts_2 = df['Whats your normal mode of transportation?  [Row 1]'].value_counts()
percentages = df['Whats your normal mode of transportation?  [Row 1]'].value_counts(normalize=True) * 100
all_options = []
# Iterate over each row in the 'transportation' column
for options in df['Whats your normal mode of transportation?  [Row 1]']:
    # Split the options by ';' and extend the list
    all_options.extend(options.split(';'))

# Step 3: Count each unique option across all rows
counts = pd.Series(all_options).value_counts()

# Step 4: Calculate the percentages
percentages = counts / counts.sum() * 100

# Print counts and percentages
print("Counts of each transportation mode:")
print(counts)
print("\nPercentages of each transportation mode:")
print(percentages)

# Print counts and percentages


def bicycle_problem():
    df['bicycle'] = df['bicycle'].str.replace('The ', 'Your ')
    df['bicycle'] = df['bicycle'].str.replace('Car ', 'car ')
    df['bicycle'] = df['bicycle'].str.replace('No preference as long as (you and your friends) are safe', 'No preference')
    df['bicycle'] = df['bicycle'].str.replace('Your car hits the man on the motorcycle with a helmet', 'Hit man on bike with helmet')
    df['bicycle'] = df['bicycle'].str.replace('Your car hits the woman walking', 'Hit the woman walking')


def perspective_analysis_text_match():
    df['passenger'] = df['passenger'].replace({'The combi hits the policemen, saving the passengers in the combi': 'injure pedestrians', 'The combi hits the policemen, saving the passengers ( you) in the combi': 'injure pedestrians', 'The combi hits the policemen, saving the passengers (i.e. you) in the combi': 'injure pedestrians'})
    df['passenger'] = df['passenger'].replace({'The combi hits the bus, saving the police but putting the people in the combi( you)  @ risk': 'injure occupants of AV' , "You don't care":  "No preference"})
    df['pedestrian'] = df['pedestrian'].replace({'Hit the police, saving the people in the combi': 'save occupants of AV', 'Hit the bus, potentially harming the people in the combi': 'save pedestrains'})

def government_choice():
    df['gove'] = df['gove'].str.replace('Yes', 'Government')
    counts_passenger = df.groupby(['country', 'passenger']).size().unstack(fill_value=0)
    counts_pedestrain = df.groupby(['country', 'pedestrian']).size().unstack(fill_value=0)
    return (counts_passenger, counts_pedestrain)


def government_choice_plot():
    bicycle_problem()
    df['gove'] = df['gove'].str.replace('Yes', 'Government')
    df['animal'] = df['animal'].str.replace('Hit the cow, and save yourself', 'Hit cow, save yourself')
    df['animal'] = df['animal'].str.replace('Go of the road, potentially injuring yourself', 'Save cow, injure yourself')
    counts = df.groupby(['country', 'animal']).size().unstack(fill_value=0)

    # Remove 'No preference' if it exists
    #counts_filtered = counts
    counts_filtered = counts.drop(columns=['No preference'], errors='ignore')

    # Get the maximum count value for y-axis scaling
    count_max = counts.values.max()

    # Define colors for the bar plot
    colors = ['darkblue', 'plum', 'red']

    # Plot the bar graph using the filtered counts
    counts_filtered.plot(kind='bar', figsize=(7, 6), color=colors)

    # Labeling the axes
    plt.xlabel('Country')
    plt.ylabel('Count')

    # Rotate x-axis labels if they are longer
    plt.xticks(rotation=0)

    # Adjust y-axis ticks
    plt.yticks(range(int(count_max) + 1))

    # Add legend with title
    plt.legend(title='Options')
    # Display the plot
    plt.show()

def plot_graph(counts, plot_title=""):

    count_max = counts.values.max()
    colors = ['darkblue', 'plum']

    counts_filtered = counts.drop(columns=['No preference'], errors='ignore')
    counts_filtered.plot(kind='bar', figsize=(7,6), color = colors)
 
    plt.xlabel('Country')
    plt.ylabel('Count')
    #if the x axis label names were longer we coudl rotate them to show it
    plt.xticks(rotation=0)
    plt.yticks(range(int( count_max) + 1))

    plt.legend( title='Options')

    plt.show()



perspective_analysis_text_match()
government_choice_plot()
count_dict = government_choice()
#plot_graph(count_dict[0], plot_title='Perspective from vehicle occupant')
#plot_graph(count_dict[1], plot_title='Perspective from non-occupant')




