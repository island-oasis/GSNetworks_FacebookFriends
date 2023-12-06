import pandas as pd
import networkx as nx
import io

print("Starting...")

# Step 1: Load the Data
# Adjust delimiter if needed (e.g., delimiter='\t' for tab-separated)
data = []
with open('C:\\Users\\Colin\\Desktop\\GSN\\data.csv', 'r', encoding='utf-8', errors='replace') as file:
    for line in file:
        try:
            data.append(pd.read_csv(io.StringIO(line), header=None))
        except pd.errors.ParserError:
            pass

df = pd.concat(data)

# Step 2: Data Cleaning
# Remove rows where the 'tags' column has more than one element
df = df[df.iloc[:, 2].apply(lambda x: len(eval(x)) == 1)]

# Remove unnecessary columns
columns_to_keep = [0, 1, 2, 3, 4, 5, 6]  # Adjust column indices based on your data
df = df.iloc[:, columns_to_keep]

# Rename columns
df.columns = ['id', 'screenName', 'tags', 'avatar', 'followersCount', 'friendsCount', 'friends']

# Drop rows with missing values
df = df.dropna()

# Ensure data types are appropriate (e.g., convert IDs to integers)
df['id'] = df['id'].astype(int)
df['friends'] = df['friends'].astype(int)

# Remove entries in the 'avatar' column that start with the " character
df = df[~df['avatar'].str.startswith('"')]

# Step 3: Graph Creation
# Create a directed graph
G = nx.from_pandas_edgelist(df, 'id', 'friends', create_using=nx.DiGraph())

# Step 4: Export to Gephi
# Save the graph in GraphML format
nx.write_graphml(G, 'twitter_friends_graph.graphml')

# Print "Done" statement
print("Done")
