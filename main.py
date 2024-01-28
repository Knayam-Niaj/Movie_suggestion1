from flask import Flask, jsonify, request
import pandas as pd 

from demographic_filter import output
from content_filter import getRecs

app = Flask(__name__)
movies_data = pd.read_csv("final.csv")
movies_data["liked"] = "unwatched"

print(movies_data.head())
all_movies = movies_data("original_title", "poster", "weighted_rating")

# create function for generic popular movies
def assign_vals():
    m_data = {
        "original_title": all_movies.iloc[0, 0], 
        "poster": all_movies.iloc[0, 1],
        "rating":  all_movies.iloc[0, 4],
    }

    return m_data

# create API call for above function and combine them
@app.route("/movies")
def get_movies():
    movie_data = assign_vals()
    return jsonify({
        "data": movie_data,
        "status": "success"
    })


# create function and app route for likes, function of liked_movies -> append var to movie data of wether movie was liked or not
def liked_movies(title, liked):
    
    # liked, disliked, unwatched

    for titles in movies_data["original_title"]:
        if(titles.lower() == title.lower()):
            titles["liked"] = liked

@app.route("/liked")
def assign_liked():
    title = request.args.get("title")
    liked = request.args.get("liked")
    liked_movies(title, liked)

    return jsonify({
        "status": "success"
    })


if __name__ == '__main__':
    app.run()