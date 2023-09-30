# NLP
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# courseCatalog variables
from courseCatalog import ordered_keys
from courseCatalog import matched_course_descriptions as course_desciptions
# graphing, plotting
from tabulate import tabulate
import networkx as nx
import matplotlib.pyplot as plt
# regex, json
import re
import json

# convert course descriptions into TF-IDF vectors/ tokenization
# tfidf_matrix will be a sparse matrix where each row corresponds to a course description 
# and each column corresponds to a unique term in the corpus.
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(course_desciptions)

#Calculate cosine similarity between all pairs of course descriptions
# cosine_similarities will be a square matrix where cosine_similarities[i][j]
#  represents the cosine similarity between course description i & description j.
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

cosine_similarity_df = pd.DataFrame(cosine_similarities, columns=course_desciptions.keys(), index=course_desciptions.keys())
#print(cosine_similarity_df)

# Write formatted similarity matrix to file 
cosine_similarity_df.to_csv('cosSim_matrix.csv')
table_string = cosine_similarity_df.to_string()

table = tabulate(cosine_similarity_df, headers='keys', tablefmt='fancy_grid')
with open('cosSim_table.txt', 'a', encoding='utf-8') as file:
	file.write(table_string)
	file.write(table)

'''
Represent cosine similarity between pairs of courses
where courses are nodes and 
where cosine similarity are edge weights
'''
#Graph creation
G = nx.Graph()
for course_title in ordered_keys:
    G.add_node(course_title)	

# Compute cosine similarity between course descriptions and assign it as edge weights
for i, course1 in enumerate(ordered_keys):
	for j, course2 in enumerate(ordered_keys):
		# only calculate cosine similarty of the 'upper' triangle of matrix
		#  due to symmetry of cosine_similarities matrix 
		# also i == j is not included since it is always 1, not interesting  
		if i < j:
			# Retreive cosine similarity between specific course descriptions
			similarity = cosine_similarities[i][j]

			# Assign cosine similarity as edge weight
			G.add_edge(course1, course2, weight=similarity)

# Adjust the figure size based on the number of nodes
fig = plt.figure(figsize=(10, 10))
# force-directed layout for the graph
pos = nx.spring_layout(G, k=1, iterations=100)  

#scale the graph while perserving proportionality
# scaling_factor = 5.0
# scaled_pos = {node: (x * scaling_factor, y * scaling_factor) for node, (x, y) in pos.items()}
# for u, v in G.edges():
#     G[u][v]['weight'] = G[u][v]['weight'] * scaling_factor

# helper function to extract titles only from course signatures
def extract_titles(input_string):
	#whitespace between metacharacters matter
    pattern = r'\w+\s\d+[A-Z]?\.\s(.*?)\s\(\d+\)'
    titles = re.findall(pattern, input_string)
    return ', '.join(titles)

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='skyblue')
titles_list = [extract_titles(key) for key in ordered_keys]

#debug: missing node labels (course titles)
# with open('tempLog.txt', 'w', encoding='utf-8') as file:
# 	file.write("[" + ", \n".join(map(str, ordered_keys)) + "]")
# 	file.write("[" + ", \n".join(map(str, titles_list)) + "]")
	
node_labels = {node: title for node, title in zip(G.nodes(), titles_list)}
nx.draw_networkx_labels(G, pos, font_size=8, labels=node_labels, font_family="Arial")

# Draw edges
edges = G.edges()
weights = [G[u][v]['weight'] for u, v in edges]
nx.draw_networkx_edges(G, pos, edgelist=edges, width=weights, edge_color='gray')
#nx.draw_networkx_edges(G, pos, width=weights, edge_color='gray')

# Add edge labels with weight numbers
#edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in edges}
#nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

plt.axis("off")
plt.title("Cosine Similarity Graph based on Course Descriptions")
plt.show()


'''
Reformat Graph to JSON representation (as input for D3.js)
'''
# Extract nodes and edges
nodes = list(G.nodes(data=True))
edges = list(G.edges(data=True))

# Create nodes, links data
# **node_attrs auto-unpack and add other attributes as key:value pairs
nodes_data = [{"id": node_id, **node_attrs} for node_id, node_attrs in nodes]
links_data = [{"source": source, "target": target, **edge_attrs} for source, target, edge_attrs in edges]

# Create a dictionary to hold the nodes and links data
# Remember that links independently define the edges, 
#  not indexed/paired with nodes 
graph_data = {"nodes": nodes_data, "links": links_data}

# Save graph to JSON conversion
graph_json = json.dumps(graph_data, indent=2)
with open('graph2json.txt', 'w', encoding='utf-8') as file:
	file.write(graph_json)





