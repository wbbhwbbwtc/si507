# Name: Leyi Wang
# UMID: 27515989

"""
This script is used to get the data from Spotify API and Billboard for final project
"""
from spotipy.oauth2 import SpotifyClientCredentials


def get_billboard():
    song_name_list, song_artist_list, song_rank_list = [], [], []
    hits_list = []
    url = "https://www.billboard.com/charts/hot-100"
    html_text = make_url_request_using_cache(url, CACHE_DICT)
    soup = BeautifulSoup(html_text, 'html.parser')
    all_list_name = soup.find_all('span',class_="chart-element__information__song text--truncate color--primary")
    all_list_artist = soup.find_all('span',class_="chart-element__information__artist text--truncate color--secondary")
    all_list_rank = soup.find_all('span',class_="chart-element__rank__number")

    for i in all_list_name:
        name = i.text
        song_name_list.append(name)
    for i in all_list_artist:
        artist = i.text
        song_artist_list.append(artist)
    for i in all_list_rank:
        rank = i.text
        song_rank_list.append(rank)
    for x in range(0,100):
        item={}
        item['track_name']= song_name_list[x]
        item['artist_name'] = song_artist_list[x]
        item['rank'] = x + 1
        hits_list.append(item)
    return hits_list


def get_spotify_csv(number):
    cid = secrets.CLIENT_ID
    secret = secrets.CLIENT_SECRET

    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    artist_name = []
    track_name = []
    popularity = []
    track_id = []

    for i in range(0,number):
        for name in song_artist_list:
            track_results = sp.search(name)
            for i, t in enumerate(track_results['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
                track_name.append(t['name'])
                track_id.append(t['id'])
                popularity.append(t['popularity'])

    df_tracks = pd.DataFrame({'artist_name':artist_name,'track_name':track_name,'track_id':track_id,'popularity':popularity})
    df_tracks.to_csv('artists.csv')
    return df_tracks

