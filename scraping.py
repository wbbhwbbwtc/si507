# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Get list of dates to use in url strings
dates = []
start = datetime.date(2021, 12, 10)
end = datetime.date(2021, 12, 10)
delta = end - start
for i in range(int(delta.days + 1)):
    day = start + datetime.timedelta(days=i)
    url_string = day.strftime("%Y-%m-%d")
    dates.append(url_string)

# Get list of full urls for each date
date_urls = []
for date in dates:
    url = "https://spotifycharts.com/regional/us/daily/"
    date_url = url + date
    date_urls.append(date_url)


# Define function to run scraping process
def scrape(date_urls):
    data = []

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Run scraping function
    for url in date_urls:
        # Visit URL
        browser.visit(url)

        # Set up HTML parser
        html = browser.html
        song_soup = soup(html, 'html.parser')
        playlist = song_soup.find('table', class_='chart-table')
        rank = 1
        for i in playlist.find('tbody').findAll('tr'):
            song = i.find('td', class_='chart-table-track').find('strong').get_text()

            artist = i.find('td', class_='chart-table-track').find('span').get_text()
            artist = artist.replace("by ", "").strip()

            songurl = i.find('td', class_='chart-table-image').find('a').get('href')
            songid = songurl.split("track/")[1]

            position = i.find('td', class_='chart-table-position').get_text()

            streams = i.find('td', class_='chart-table-streams').get_text()

            date = url.split("daily/")[1]
            data.append([songid, songurl, song, artist, date, position, streams, rank])
            rank += 1


    # Stop webdriver
    browser.quit()

    # Convert to pandas DataFrame
    spotify_df = pd.DataFrame(data, columns=["song_id", "song_url", "track_name", "artist_name", "date", "position", "streams", "rank"])
    spotify_df = spotify_df.set_index("song_id")
    # Save as csv file in same folder
    with open('spotifytop200.csv', 'w') as x:
        spotify_df.to_csv(x, header=True, index=False)
    return spotify_df