# si507
## Part 1: How to run this app


Firstly, please set up a virtual environment and install the python packages in requirement.txt

Secondly, run `python3 scraping.py` to scrape top songs from spotify website. You could change the start date and end date to scrape tracks from mutiple dates

Thirdly, run `python3 webapi_and_build_db.py` to get information using spotify's web API to retrive detailed information and popularity. It will also build a database and cache the data in data.json. Please change the secret and key if you want to use the code in other projects

Finally, you could run `flask run` to run the app

## Part 2: Data Sources

1. Scraping a new single page (Challenge score = 4, I managed to scraped multiple pages!!)

In this project, I scraped daily top songs in US from https://spotifycharts.com/regional/us/daily/ which including songs name, songs url, artist name, position, stream, and rank. The scraped data was stored as a csv file named “spotifytop200.csv”. the bs4 package was used to scrape the page. The most challenging part is to scrape multiple pages with different dates as top songs changes fast by days. Therefore, webdriver_manager package was used to scrape any given time period and the script will scrape them automatically. The default setting will scrape the data from today and it is all depends to future users of this application and could be easily extended to scrape top songs from any start date and end date.The records of each dates are 200 and all of them are retrieved and cache was used.

2. Web API (Challenge score = 4)

The second part of the project data is using spotify API to search the artist’s name from top songs and return detailed information. The spotify package and keys were used to retrieve the data and cache was used as well. For more details, please see webapi_and_build_db.py


## Part 3: Interaction and Presentation Options

In this project. I used Flask, Jinja2 and SQLite to build a web application that enable users to interact with the application. Firstly, user could view the top songs with different ranking algorithm including, rank, track name and artist name. Also, user could choose the number of top songs they want to view such as 20, 50, 100 etc. 

Once users found interesting songs or artist, they could use the second feature to find more information including other music by given artist and plotly package was used to view the popularity index from spotify. For more details, please see app.py and templates.

Finally, inspired by homework, I created a side project named guessing your favorite artist.


## Part 4: Demo Link
https://drive.google.com/file/d/14-LkMyiMp637TP-Ju6k9XHm6I96qrcKt/view?usp=sharing
![image](https://user-images.githubusercontent.com/39076514/146651479-0209c608-61e3-455a-93cc-7d25967cc2fc.png)
