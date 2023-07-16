import pandas as pd
from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pd.read_pickle(open('popular.pkl','rb'))
pt = pd.read_pickle(open('pt.pkl','rb'))
books = pd.read_pickle(open('books.pkl','rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl','rb'))

app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['num_ratings'].values),
                           rating = list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    book_index = np.where(pt.index == user_input)[0][0]  # ------------>returning a 2-D array
    distances = similarity_scores[book_index]
    similar_books = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Image-URL-M"].values))

        data.append(item)

    #print(data)
    return render_template('recommend.html',data=data)


if __name__=='__main__':
    app.run(debug=True)
