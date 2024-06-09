import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer #pip install scikit-learn
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

filename = 'games.csv'

games = pd.read_csv(filename) #doc file csv

games = games[['app_id', 'title', 'rating', 'price_final']] #lay chi 3 cot trong file csv

word = "Very Positive"
very_positive_game = games[games['rating'].str.contains(word, na=False)] # tim cac game co danh gia very positive

titles = pd.DataFrame.from_dict(very_positive_game)

titles["mod_title"] = titles["title"].str.replace("[^a-zA-Z0-9 ]", "", regex=True) #sua title game xoa het ki tu k can thiet va cho vao cot mod_titles
titles["mod_title"] = titles["mod_title"].str.lower() # sua title cho viet thuong het
titles["mod_title"] = titles["mod_title"].str.replace("\s+", " ", regex=True) #sua title cho nhieu space = 1 space
titles = titles[titles["mod_title"].str.len()>0] #neu mod title k co gi thi xoa luon( vd: ten game toan ki tu)

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(titles["mod_title"]) # phuong phap tim kiem k hieu lam???

def search(query, vectorizer):
    processed = re.sub("^a-zA-Z0-9 ", "", query.lower()) # van la phuong phap tim kiem k hieu lam
    query_vec = vectorizer.transform([processed])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -10)[-10:] # lay 5 ket qua gan voi ten tim kiem nhat
    result = titles.iloc[indices]
    result = result.sort_values("price_final", ascending=False) # sap xep theo gia tien
    result = result[['app_id', 'title', 'rating', 'price_final']] # loai bo cot mod_title
    result = result.loc[similarity[indices]>= 0.1] # loai bo cac ket qua voi diem tuong dong qua thap
    return result

game_name = input("Điền vào tên game muốn tìm: ")
search_result = search(game_name, vectorizer)

if not search_result.empty:
    print(search_result)
else:
    print("Không tìm thấy kết quả phù hợp.")