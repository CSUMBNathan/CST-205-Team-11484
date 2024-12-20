#https://github.com/CSUMBNathan/CST-205-Team-11484
#Authors: Nathaniel Trujillo, Joseph Ramer, Cooper Westervelt
#Date:12/18/2024
#Abstract: This program makes a flask web application that pull a random
#video from the youtube data API. Displays it on a flask webpage and 
#requests user input for a guess on the number of views.




import random
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from googleapiclient.discovery import build

API_KEY = 'AIzaSyCG-XNDsCYENMDhzhZsv9zArJVH-ZlYhvk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

#Function made by Nathaniel Trujillo and edited by Cooper Westervelt
#this function gets a 'random' videof using a random keyword and searching that query. 50 Results
def get_random_video():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    search_query = random.choice(['cool', 'random', 'awesome','cooking','sports', 'fortnite', 'music', 'computer science'])
    response = youtube.search().list(
        q=search_query,
        part='snippet',
        type='video',
        maxResults=50
    ).execute()

    num = random.randint(0, 49)
    #Get a random video from the list.
    video = random.choice(response['items'])

    #API to get the statistics based on the video chosen. Make variables to pass into routes.
    videoStats = youtube.videos().list(
        part = 'statistics',
        id = video['id']['videoId']
    ).execute()

    view_count = int(videoStats['items'][0]['statistics']['viewCount'])
    print(video['snippet']['title'])
    print(view_count)


    return {
        'title': video['snippet']['title'],
        'thumbnail': video['snippet']['thumbnails']['high']['url'],
        'video_id': video['id']['videoId'],
        'view_count': view_count
    }

#get_random_video()

app = Flask(__name__)
bootstrap = Bootstrap5(app)

#Routes made by Nathaniel Trujillo
@app.route('/')
def index():
    # Get random video and pass it to the template
    video = get_random_video()
    return render_template('index.html', video=video)

@app.route('/guess', methods=['POST'])
def guess():
    # Get the user's guess and video data from the form
    user_guess = int(request.form['view_count'])
    actual_views = int(request.form['actual_views'])  # Passed from the form

    # check if the guess is equal to a video's views
    is_equal = user_guess == actual_views

    # Check if the user's guess is within 10% of a video's views
    ten_percent = actual_views//10
    is_close = user_guess >= actual_views-ten_percent and user_guess <= actual_views - ten_percent 

    # Render results with actual views and whether the guess was close
    return render_template(
        'results.html',
        is_equal = is_equal,
        actual_views=actual_views,
        is_close=is_close,
        video_title=request.form['video_title'],
        video_thumbnail=request.form['video_thumbnail']
    )

if __name__ == '__main__':
    app.run(debug=True)