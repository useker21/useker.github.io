"""Here implement the movie-recommender functions"""

##import the relevant packages and libraries
import random
import pandas as pd
import numpy as np

from sklearn.decomposition import NMF 
from sklearn.impute import KNNImputer

import pickle

from sklearn.metrics.pairwise import cosine_similarity

#load and create the dataframes
def create_dataframe_list():
    movies = pd.read_csv('data/movies.csv')
    ratings = pd.read_csv('data/ratings.csv')
    ratings_movies = pd.merge(ratings,movies, how='left',on='movieId')
    ratings_movies_pivot = pd.pivot_table(data = ratings_movies, 
                                      index='userId', 
                                      columns='title', 
                                      values='rating'
                                     )

    #create user and movie lists
    user_list  = ratings_movies_pivot.index.to_list()
    movie_list = ratings_movies_pivot.columns.to_list()
    return movie_list, user_list, ratings_movies_pivot, ratings_movies

movie_list, user_list, ratings_movies_pivot, ratings_movies = create_dataframe_list()

#fill the missing values
knn_imputer = KNNImputer(n_neighbors=2)
knn_imputer.fit_transform(ratings_movies_pivot)


def nmf_recommender(new_user_query, k_top=5):
    '''The function gets k-top movie recommadations for a given user matrix based on nmf model
    '''
    #get new_user-item dataframe with the previous dictionary
    new_user_ratings = pd.DataFrame(
                                    data=new_user_query,
                                    columns=movie_list, 
                                    index=['new_user']
                                   )
    #fill the missing value
    new_user_ratings_imputed = pd.DataFrame(
                                            data=knn_imputer.transform(new_user_ratings), 
                                            columns=movie_list, 
                                            index=['new_user']
                                           )
    #load the pickled model
    file = open('model/nmf_model.bin', mode='rb')
    binary = file.read()
    file.close()
    nmf_model = pickle.loads(binary)
    
    #create movie feature matrix Q
    Q_matrix = nmf_model.components_
    
    
    #create user feature matrix P
    P_new_user_matrix = nmf_model.transform(new_user_ratings_imputed)
    
    ##get the ratings reconstructed dataframe
    new_user_ratings_rec = pd.DataFrame(data=np.dot(P_new_user_matrix,Q_matrix),
                                    columns=new_user_ratings.columns,
                                    index=new_user_ratings.index.to_list()
                                       )
    #exclude the rated movies
    mask = new_user_ratings.T.isna()
    new_user_ratings_rec_2 = new_user_ratings_rec.T[mask].T
   
    #get top k rated movies
    recommend_list = new_user_ratings_rec_2.sort_values(new_user_ratings.index.to_list(), axis=1, ascending=False).T.index.to_list()[:k_top]
        
    return recommend_list

def cosim_recommender(new_user_query, k_top=5):
    '''The function gets k-top movie recommadations for a given user based on cosine similarity matrix
    '''
   
    #get new_user-item dataframe with the previous dictionary
    new_user_ratings = pd.DataFrame(
                                    data=new_user_query,
                                    columns=movie_list, 
                                    index=['new_user']
                                   )

    #add new user to user_based dataframe
    ratings_movies_pivot_2 = ratings_movies_pivot.append(new_user_ratings, ignore_index=False)

    #transpose the pivot table
    user_based = ratings_movies_pivot_2.T

    #assign to 0 for unrated movies  
    user_based_imputed = user_based.fillna(value=0)

    #apply cosine similarity to create a similarity matrix
    user_based_similarity_matrix = pd.DataFrame(cosine_similarity(user_based_imputed.T))
      
    #create a list of unseen movies for new user
    unseen_mask = user_based['new_user'].isna()
    unseen_movies = user_based[unseen_mask].index
    
    #create a list of top n=20 similar users
    similar_top_n_users = user_based_similarity_matrix[610].sort_values(ascending=False).index[1:21]
   
    #create ratings for the active user
    #predict the rating based on the (weighted) average ratings of the other user
    #sum(ratings*similarity)/sum(similarities)

    pred_ratings_list = []

    for movie in unseen_movies:
        others_user = user_based.columns[~user_based.loc[movie].isna()]
        others_user = set(others_user)
        num = 0
        den = 0
        pred_ratings = 0
        for user in set(similar_top_n_users).intersection(others_user):
            rating = user_based[user][movie]    
            sim = user_based_similarity_matrix[610][user]
              
            num = num + (rating*sim)
            den = den + sim + 0.000001
        
            pred_ratings = round(num/den)
        
        
        pred_ratings_list.append((movie, pred_ratings))
        pred_ratings = 0
          
    #look at the rating and choose n of them
    recommend_list = sorted(pred_ratings_list, key=lambda tup: tup[1], reverse=True)[0:k_top]

    result_list = []
    for item in recommend_list:
        result_list.append(item[0])
           
    return result_list


def most_popular_movie_recommender(new_user_query,k_top=5):
    '''The function gets k-top most popular movie recommadations 
    '''
    #get new_user-item dataframe with the previous dictionary
    new_user_ratings = pd.DataFrame(
                                    data=new_user_query,
                                    columns=movie_list, 
                                    index=['new_user']
                                   )

    #add new user to user_based dataframe
    ratings_movies_pivot_2 = ratings_movies_pivot.append(new_user_ratings, ignore_index=False)

    #transpose the pivot table
    user_based = ratings_movies_pivot_2.T

    #create a list of unseen movies for new user
    unseen_mask = user_based['new_user'].isna()
    unseen_movies = user_based[unseen_mask].index

    # filter out movies that have been watched by less than 100 users
    ratings = ratings_movies.groupby('title')[['rating']].count()
    ratings = ratings[ratings['rating'] >=100]
    movies_more_than_100 = ratings.index.to_list()
    
    #create a best movie list which have not seen before and watched by more than 100 users
    best_movie_list = []
    for i in movies_more_than_100:
        if i in unseen_movies:
            best_movie_list.append(i)
        else:
            continue
            
    ratings_2 = ratings_movies.set_index('title').loc[best_movie_list,:]
    
    # 2. scoring
    # calculate the average rating and wachted by users for each movie
    ratings_3 = ratings_2.reset_index()
    # merge them to a new dataframe
    ratings_4 = pd.DataFrame(ratings_3.groupby('title')[['rating']].mean().round(2))
    ratings_4['count_rating'] = ratings_3.groupby('title')[['rating']].count()
    ratings_4.rename(columns={'rating':'mean_rating'}, inplace=True)
    
    # 3. ranking
    recommend_list = ratings_4.sort_values(['mean_rating','count_rating'], ascending=False).index.to_list()[:5]
   
    return recommend_list
  


def random_recommender(new_user_query,k_top=5):
    '''The function gets k-top random movie recommadations
    '''
    #get new_user-item dataframe with the previous dictionary
    new_user_ratings = pd.DataFrame(
                                    data=new_user_query,
                                    columns=movie_list, 
                                    index=['new_user']
                                   )

    #add new user to user_based dataframe
    ratings_movies_pivot_2 = ratings_movies_pivot.append(new_user_ratings, ignore_index=False)


    #transpose the pivot table
    user_based = ratings_movies_pivot_2.T

    #create a list of unseen movies for new user
    unseen_mask = user_based['new_user'].isna()
    unseen_movies = user_based[unseen_mask].index

    result_list = []
    
    for i in range(5):

        movie = random.choice(unseen_movies)
        result_list.append(movie)

    return result_list
