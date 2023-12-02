# import code into Gephi
# dataset found here: https://www.kaggle.com/datasets/goyaladi/twitter-dataset/data
# don't forget to update your filepath accordingly

import pandas as pd
import networkx as nx
import community
from sklearn.ensemble import IsolationForest

# Step 1: Data Collection
dataset_path = 'C:\\Users\\Colin\\Desktop\\GSN\\twitter_dataset.csv'
data = pd.read_csv(dataset_path)

# Step 2: Data Cleaning and Preprocessing
data.drop_duplicates(subset=['Tweet_ID'], inplace=True)
data = data[data['Retweets'] != 0]  # Adjust the condition as needed
relevant_features = ['Username', 'Tweet_ID', 'Retweets', 'Likes', 'Timestamp']
cleaned_data = data[relevant_features]

# Step 3: Data Analysis
num_tweets = len(cleaned_data)
num_users = cleaned_data['Username'].nunique()
num_retweets = cleaned_data['Retweets'].sum()
num_likes = cleaned_data['Likes'].sum()

print(f"Number of Tweets: {num_tweets}")
print(f"Number of Users: {num_users}")
print(f"Total Retweets: {num_retweets}")
print(f"Total Likes: {num_likes}")

# Step 4: Identifying Communities
G = nx.from_pandas_edgelist(cleaned_data, 'Username', 'Tweet_ID')
communities = community.best_partition(G)

# Step 5: Export the Graph in GraphML Format
nx.write_graphml(G, 'twitter_network.graphml')

# Step 6: Anomaly Detection
features_for_anomaly_detection = ['Retweets', 'Likes']
model = IsolationForest()
model.fit(cleaned_data[features_for_anomaly_detection])
cleaned_data['is_anomaly'] = model.predict(cleaned_data[features_for_anomaly_detection])
