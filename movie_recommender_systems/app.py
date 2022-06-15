from flask import Flask, render_template, request
from get_recommendation import random_recommender, nmf_recommender, cosim_recommender, most_popular_movie_recommender
import random
import pickle


app = Flask(import_name=__name__)

@app.route("/")
def homepage():

    #load the pickled movie_list
    file = open('data/movie_list.bin', mode='rb')
    binary = file.read()
    file.close()
    movie_list = pickle.loads(binary)
        
    movie_1 = random.choice(movie_list)
    movie_2 = random.choice(movie_list)
    movie_3 = random.choice(movie_list)
    movie_4 = random.choice(movie_list)
    movie_5 = random.choice(movie_list)

    return render_template("homepage.html", movie_1 = movie_1, movie_2 = movie_2, movie_3=movie_3, movie_4=movie_4, movie_5=movie_5)
   

@app.route("/recommendations")
def results():
        
    new_user_query = request.args.to_dict()
    new_user_query.pop('model')
    new_user_query = {key:int(value) for key, value in new_user_query.items()} #dictionary comprehension
   

    if request.args.to_dict()['model'] == 'NMF':
        result_list = nmf_recommender(new_user_query,k_top=5)

    if request.args.to_dict()['model'] == 'Cosim':
        result_list = cosim_recommender(new_user_query,k_top=5)
    
    if request.args.to_dict()['model'] == 'Random':
        result_list = random_recommender(new_user_query,k_top=5)

    if request.args.to_dict()['model'] == 'Most_Popular':
        result_list = most_popular_movie_recommender(new_user_query,k_top=5)
  
    
    return render_template(
        "results.html",
         recommend_movie_list=result_list 
    )

if __name__ == '__main__':
    app.run(debug=True)