import requests
import random

TMDB_APIKEY = "6310fba08f1872dc0567d5f6d52ec77f"
TMDB_READ_ACCESS = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MzEwZmJhMDhmMTg3MmRjMDU2N2Q1ZjZkNTJlYzc3ZiIsIm5iZiI6MTczNDc1MjU0My44MzksInN1YiI6IjY3NjYzOTFmNzE2ODBiODJhZTkwZTc3YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mX9zcL1p6apu7cyHunumY5gZQuT0HeG7AGtJ2uYkfj4"
TMDB_URL = 'https://api.themoviedb.org/3/discover/movie'


OMDB_API_KEY = "31453b08"
OMDB_URL = "http://www.omdbapi.com/"

PERAMS = {
    "apikey": OMDB_API_KEY,
    "s": "John Wick",
    "type": "Movie",
}

genre_dict = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}





class Movies:
    def __init__(self):
        self.movies = []





    def movie(self, option, *args):
        movie_dict = {}


        if option.title() == "Genre":

            PERAMS = {
                "api_key": TMDB_APIKEY,
                'with_genres': genre_dict[args[0].title()],
                "page": "1",
            }

            response = requests.get(TMDB_URL, params= PERAMS)
            data = response.json()

            movie_list = data

            for i, movie in enumerate(data["results"]):
                movie_dict[i] = {
                    "Movie": movie["original_title"],
                    "Image": movie["backdrop_path"]
                }


            return movie_dict

        if option.title() == "Search":
            URL = "https://api.themoviedb.org/3/search/movie"

            PERAMS = {
                "api_key": TMDB_APIKEY,
                "query": args[0],
            }

            response = requests.get(URL, params=PERAMS)
            data = response.json()

            if data["results"]:


                for i, movie in enumerate(data["results"]):
                    movie_dict[i] = {
                        "title": movie["original_title"],
                        "poster_path": f"https://image.tmdb.org/t/p/w500{movie["backdrop_path"]}",
                        "overview": movie["overview"],
                        "id": movie["id"],
                        "vote_average": round(movie["vote_average"], 1),
                        "release_date": movie["release_date"][:4],
                    }
                return movie_dict[0]

    def random_movie_genre(self):
        movie_dict = {}
        random_key = random.choice(list(genre_dict.keys()))

        PERAMS = {
            "api_key": TMDB_APIKEY,
            'with_genres': genre_dict[random_key],
            "page": "1",
        }

        response = requests.get(TMDB_URL, params=PERAMS)
        data = response.json()

        movie_list = data
        print(movie_list)

        for i, movie in enumerate(data["results"]):
            movie_dict[i] = {
                "title": movie["original_title"],
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie["backdrop_path"]}",
                "overview": movie["overview"],
                "id": movie["id"],
                "vote_average": round(movie["vote_average"], 1),
                "release_date": movie["release_date"][:4],


            }


        return movie_dict


# one = Movies()
# print(one.movie("search", "john wick"))








