# So, to strike an appropriate balance between these goals, and to protect our business, our technology infrastructure, and our ability to continue to provide interesting and robust sports statistics to our users, this section of our Agreement sets forth certain restrictions on permitted uses of this Site and its Content. Our guiding principles are that (1) sharing, using, modifying, repackaging, or publishing data found on individual SRL webpages is welcomed, whether for commercial or non-commercial purposes, but (2) any such sharing, use, modification, repackaging, or publication should explicitly credit SRL as the source of the data to the maximum extent possible and (3) any such sharing, use, modification, repackaging, or publication must not violate any express restrictions set forth in this Section 5, especially the restrictions set forth in subparts 5(i) and 5(j) below.

# Bot/Scraping/Crawler Traffic on Sports-Reference.com Sites

# October 26, 2022

# Sports Reference is primarily dependent on ad revenue, so we must ensure that actual people using web browsers have the best possible experience when using this site. Unfortunately, non-human traffic, ie bots, crawlers, scrapers, can overwhelm our servers with the number of requests they send us in a short amount of time. Therefore we are implementing rate limiting on the site. We will attempt to keep this page up to date with our current settings.

# Currently we will block users sending requests to:

#     our sites more often than twenty requests in a minute.
#     This is regardless of bot type and construction and pages accessed.
#     If you violate this rule your session will be in jail for an hour.

# Why Not Provide an API?

# Most of our data comes from third parties who sell the data to us. As part of our agreements with them we can not provide the data available as a download on our site. We are aware that an API would mitigate some issues, but it's not our business model. If you want to get data for a low price, we suggest NatStat.com. 


# What questions do people want to ask the data?
# https://www.basketball-reference.com//leagues/NBA_2023.html
# - 

# import requests
# import pandas as pd
# from bs4 import BeautifulSoup

# def main():

#     # URL to scrape
#     url = 'https://www.basketball-reference.com/leagues/NBA_2023.html'

#     # Send a GET request to the URL
#     response = requests.get(url)

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find the Per Game Stats table
#     table = soup.find('table', {'id': 'per_game_stats'})

#     # Convert the table to a pandas DataFrame
#     df = pd.read_html(str(table))[0]

#     # Print the DataFrame
#     print(df)

# if __name__ == "__main__":
#     main()

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# idea
# create your own class for your results
# you'll want to create a bbref object 
# bbref.data() -> gives you the pandas object
# bbref.data_dict() -> data dictionary for the values 

# is there a way to see if i already called a particular URL
# some URLs have lots of data, so i may not need to call it again in a second call. 
# it might already be in memory?? maybe not since its all contained in a function, but if its class, would it work??

def per_game_stats():
    # per_game_stats has team and opponent
    # team -> per_game-team
    # opponent -> per_game-opponent
    time.sleep(0.5)
    url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    bbref_html_table = soup.find('table', {"id": "per_game-team"})
    bbref_stats = pd.read_html(str(bbref_html_table))[0]
    bbref_stats["Team"] = bbref_stats["Team"].apply(lambda x: x.replace("*",""))
    bbref_stats = bbref_stats.iloc[:-1]
    return bbref_stats

def total_stats():
    # has team + opponent disctinctions
    time.sleep(0.5)
    url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    bbref_html_table = soup.find('table', {"id": "totals-team"})
    bbref_stats = pd.read_html(str(bbref_html_table))[0]
    bbref_stats["Team"] = bbref_stats["Team"].apply(lambda x: x.replace("*",""))
    bbref_stats = bbref_stats.iloc[:-1]
    return bbref_stats

# per_poss-team

def per_possession_stats():
    # has team + opponent disctinctions
    time.sleep(0.5)
    url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    bbref_html_table = soup.find('table', {"id": "per_poss-team"})
    bbref_stats = pd.read_html(str(bbref_html_table))[0]
    bbref_stats["Team"] = bbref_stats["Team"].apply(lambda x: x.replace("*",""))
    bbref_stats = bbref_stats.iloc[:-1]
    return bbref_stats

def advanced_stats():
    url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table', {"id": "advanced-team"})
    bbref_stats = pd.read_html(str(table))[0]
    new_cols = [x[1] for x in bbref_stats.columns]
    bbref_stats.columns = new_cols
    bbref_stats["Team"] = bbref_stats["Team"].apply(lambda x: x.replace("*",""))
    bbref_stats = bbref_stats.iloc[:-1]
    return bbref_stats

if __name__ == "__main__":
    print(per_game_stats()) 
