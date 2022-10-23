# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from pprint import PrettyPrinter
pp = PrettyPrinter()

import pandas as pd
import ast
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer



movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.merge(left = movies, right = credits, on = 'title')
movies = movies[['id','title','overview','genres','cast','keywords','crew']]
movies.dropna(inplace=True)
def func(obj):
    List = []
    for i in ast.literal_eval(obj):
        List.append(i['name'])
    return List
movies['genres'] = movies['genres'].apply(func)
movies['keywords'] = movies['keywords'].apply(func)

def func1(obj):
    List = []
    counter = 0
    for i in ast.literal_eval(obj):
        if counter !=3:
            List.append(i['name'])
            counter+=1
        else:
            break
    return List
movies['cast'] = movies['cast'].apply(func1)

def func2(obj):
    List = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            List.append(i['name'])
            break
    return List
movies['crew'] = movies['crew'].apply(func2)
movies['overview'] = movies['overview'].apply(lambda x:x.split())
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
movies2 = movies[['id','title','tags']]
pd.options.mode.chained_assignment = None
movies2['tags'] = movies2['tags'].apply(lambda x:" ".join(x))
movies2['tags'] = movies2['tags'].apply(lambda x:x.lower())
cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(movies2['tags']).toarray()
#Stemming Process
ps = PorterStemmer()
#defining the stemming function
def stem(text):
    a=[]
    for i in text.split():
        a.append(ps.stem(i))
    return " ".join(a)
movies2['tags'] = movies2['tags'].apply(stem)
# Measuring similarity between Movies using cosine distance

similarity = cosine_similarity(vectors)


def recommend_me(movie):
    movie_index = movies2[movies2['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    for i in movies_list:
        print(movies2.iloc[i[0]].title)

recommend_me('Batman')


apiKey = '9b7dbe9c'
#Fetch Movie Data
data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
year = ''
movieTitle = 'Me Before You'
params = {
    's':movieTitle,
    'type':'movie',
    'y':year
}

response = requests.get(data_URL, params=params).json()
dict_items = response.items()
first_item = list(dict_items)[:1]
first_item = first_item[0][1]
print(first_item[0])

#pp.pprint(response)