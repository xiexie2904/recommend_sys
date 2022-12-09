from django.shortcuts import render
from django.http import HttpResponse
# importing the required libraries and functions
import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# def home(request):
#     return render(request, 'home.html')
def main(request):
    return render(request, 'films/main.html')
def user_info(request):
    return render(request, 'films/user_info.html')
def user_form(request):
    return render(request, 'films/user_form.html')
def user_recommend(request):
    # importing the datasets
    # movies_df = pd.read_csv('./data/movies.csv')
    # rating_df = pd.read_csv('./data/ratings.csv')
    movies_df = pd.read_csv('./data/movies.csv',usecols=['movieId','title'],dtype={'movieId': 'int32', 'title': 'str'})
    rating_df=pd.read_csv('./data/ratings.csv',usecols=['userId', 'movieId', 'rating'],
    dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
    print(movies_df.head())
    df = pd.merge(rating_df,movies_df,on='movieId')
    combine_movie_rating = df.dropna(axis = 0, subset = ['title'])
    movie_ratingCount = (combine_movie_rating.
     groupby(by = ['title'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'totalRatingCount'})
     [['title', 'totalRatingCount']]
    )
    rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on = 'title', right_on = 'title', how = 'left')

    popularity_threshold = 50
    rating_popular_movie= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')

    movie_features_df=rating_popular_movie.pivot_table(index='title',columns='userId',values='rating').fillna(0)

    movie_features_df_matrix = csr_matrix(movie_features_df.values)

    
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(movie_features_df_matrix)

    query_index = np.random.choice(movie_features_df.shape[0])

    distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)

    list_recommend = []

    for i in range(0, len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:\n'.format(movie_features_df.index[query_index]))
        else:
            list_recommend.append(movie_features_df.index[indices.flatten()[i]])
            print('{0}: {1}, with distance of {2}:'.format(i, movie_features_df.index[indices.flatten()[i]], distances.flatten()[i]))


    print(list_recommend)

    prod_name = request.POST.get('product')
    submitbutton =  request.POST.get('submit')
    context = {'prod_name': prod_name, 'submitbutton': submitbutton, 'recommendation':list_recommend}
    return render(request, 'films/user_form.html', context)
