import pandas as pd

# Load the Twitter data from the local file
csv_path = 'C:\\Users\\Colin\\Desktop\\TwitterThreads\\fifteen_twenty.csv'

# Try different encodings until you find the correct one
encodings_to_try = ['utf-8', 'ISO-8859-1', 'cp1252']
for encoding in encodings_to_try:
    try:
        data = pd.read_csv(csv_path, encoding=encoding)
        break  # Stop trying encodings if successful
    except UnicodeDecodeError:
        print(f"Failed to decode using {encoding} encoding. Trying another one.")

# Create a new DataFrame for nodes
nodes = data[['id', 'thread_number']].copy()
nodes.drop_duplicates(inplace=True)

# Save the nodes DataFrame to a CSV file
nodes.to_csv('C:\\Users\\Colin\\Desktop\\TwitterThreads\\nodes.csv', index=False)

# Create a new DataFrame for edges with additional columns for weights
edges = data[['id', 'thread_number', 'retweets', 'likes', 'replies']].copy()

# Calculate weights based on some metric (e.g., retweets, likes, replies)
edges['weight'] = edges['retweets'] + edges['likes'] + edges['replies']

# Save the edges DataFrame to a CSV file
edges.to_csv('C:\\Users\\Colin\\Desktop\\TwitterThreads\\edges.csv', index=False)

# Update the edges DataFrame to include source and target columns
edges['source'] = edges['id'].astype(str)  # Ensure source is in string format
edges['target'] = edges['thread_number'].astype(str)  # Ensure target is in string format

# Save the updated edges DataFrame to a CSV file
edges.to_csv('C:\\Users\\Colin\\Desktop\\TwitterThreads\\edges.csv', index=False)

# Display the first few rows of the loaded data
print(edges.head())
