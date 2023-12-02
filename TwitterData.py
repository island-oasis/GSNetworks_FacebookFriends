
import pandas as pd
import networkx as nx
import community
from sklearn.ensemble import IsolationForest

# Step 1: Data Collection
dataset_path = 'C:\\Users\\Colin\\Desktop\\GSN\\twitter_dataset.csv'
data = pd.read_csv(dataset_path)

# Step 2: Data Cleaning and Preprocessing
data.drop_duplicates(subset=['Tweet_ID'], inplace=True)
data = data[~data['Retweets'] != 0]
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
nx.write_gexf(G, 'twitter_network.gephi')

# Step 5: Anomaly Detection
features_for_anomaly_detection = ['Retweets', 'Likes']
model = IsolationForest()
model.fit(cleaned_data[features_for_anomaly_detection])
cleaned_data['is_anomaly'] = model.predict(cleaned_data[features_for_anomaly_detection])

# Step 6: Documentation and Reporting
# Ensure to document and comment your code appropriately