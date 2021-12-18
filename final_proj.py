import requests
import json
import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import csv
import sqlite3
import pandas as pd


cid = 'c2a9185f37f1466e8c7e8112f553413c'
secret = '6c475ef6cfe543d9a1015830e1e881d6'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



CACHE_FILE_NAME = 'data.json'
CACHE_DICT = {}

# Code to scrape data from Spotify Charts website for United States Top 200 List
# https://spotifycharts.com/regional/us/daily/






hits_list = pd.read_csv('spotifytop200.csv').to_dict('records')
print(hits_list)
song_artist_list= [hits_list[i]['artist_name'] for i in range(10)]



def load_cache(): 
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache): 
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): 
        print("Using cache")
        return cache[url]     
    else:
        print("Fetching")
        response = requests.get(url) 
        cache[url] = response.text 
        save_cache(cache)          
        return cache[url]          

CACHE_DICT = load_cache()





def get_tracks_csv():
    # create empty lists where the results are going to be stored
    artist_name = []
    track_name = []
    popularity = []
    track_id = []

    # create csv file to store top 10 songs for each artist by using Spotify API
    for i in range(0,10):
        for name in song_artist_list:
            track_results = sp.search(name)
            # print(result['tracks']['items'][0]['artists'])
            for i, t in enumerate(track_results['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])
                popularity.append(t['popularity'])
        # print(track_name)

    df_tracks = pd.DataFrame({'artist_name':artist_name,'track_name':track_name,'track_id':track_id,'popularity':popularity})
    df_tracks.to_csv('artists.csv') 

get_tracks_csv()
#since creating the csv file cost a lot of time everytime so for the next steps I just utilize the former createdcsv file.



#write the pandas dataframe to a sqlite table
def create_tracks():
    conn= sqlite3.connect("songs.sqlite")
    cur = conn.cursor()
    df = pd.read_csv('artists.csv',index_col=0)
    df.drop_duplicates(subset=['track_id'],keep = False,inplace=True)
    drop_tracks_sql = 'DROP TABLE IF EXISTS "Track"'
    cur.execute(drop_tracks_sql)
    df.to_sql('Track', conn, if_exists='append', index=False)
    conn.close()

create_tracks()


#create hits table 
def create_hits():
    conn = sqlite3.connect("songs.sqlite")
    cur = conn.cursor()
    drop_hits_sql = 'DROP TABLE IF EXISTS "Hits"'
    
    create_hits_sql = '''
        CREATE TABLE IF NOT EXISTS "Hits" (
            "Track_Name" TEXT NOT NULL, 
            "Artist_Name" TEXT NOT NULL,
            "Rank" INTEGER PRIMARY KEY NOT NULL
        )
    '''
    cur.execute(drop_hits_sql)
    cur.execute(create_hits_sql)
    conn.commit()
    conn.close()

create_hits()  


def load_hits():
    conn = sqlite3.connect("songs.sqlite")
    cur = conn.cursor()

    insert_hits_sql = '''
        INSERT INTO Hits
        VALUES (?, ?, ?)
    '''
    
    for item in hits_list:
        cur.execute(insert_hits_sql,
        [
            item['track_name'],
            item['artist_name'],
            item['rank']
        ]
        )
    conn.commit()
    conn.close()

load_hits()  


# since there is no way right now to set a primary key in the pandas df.to_sql() method
# I need to create a duplicate table and set primary key followed by copying data over, then drop old table to clean up.
def edit_tracks():
    conn = sqlite3.connect("songs.sqlite")
    cur = conn.cursor()
    cur.executescript('''

    BEGIN TRANSACTION;
    ALTER TABLE Track RENAME TO old_table;

    /*create a new table with the same column names and types while
    defining a primary key for the desired column*/

    DROP TABLE IF EXISTS "Tracks";

    CREATE TABLE Tracks (
                            artist_name TEXT,
                            track_name TEXT,
                            track_id TEXT PRIMARY KEY NOT NULL,
                            popularity INTEGER
                            );

    INSERT INTO Tracks SELECT * FROM old_table;

    DROP TABLE old_table;
    COMMIT TRANSACTION;
    ''')

    conn.close()

edit_tracks()