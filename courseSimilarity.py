import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from courseCatalog import matched_course_descriptions as course_desciptions

from tabulate import tabulate

# convert course descriptions into TF-IDF vectors
# tfidf_matrix will be a sparse matrix where each row corresponds to a course description 
# and each column corresponds to a unique term in the corpus.
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(course_desciptions)

#Calculate cosine similarity between all pairs of course descriptions
# cosine_similarities will be a square matrix where cosine_similarities[i][j]
#  represents the cosine similarity between course description i & description j.
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

cosine_similarity_df = pd.DataFrame(cosine_similarities, columns=course_desciptions.keys(), index=course_desciptions.keys())
print(cosine_similarity_df)
cosine_similarity_df.to_csv('cosSim_matrix.csv')
table_string = cosine_similarity_df.to_string()

# Create nicely formatted table
table = tabulate(cosine_similarity_df, headers='keys', tablefmt='fancy_grid')
with open('cosSim_table.txt', 'a', encoding='utf-8') as file:
	file.write(table_string)
	file.write(table)


