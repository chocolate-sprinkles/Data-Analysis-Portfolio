import requests
import pandas as pd
from bs4 import BeautifulSoup

class BasketBallReferenceConnection:

    # Solve getting the correct URL first
    def __init__(self,league,season_type,data_type,year):
        
        if not isinstance(league,str):
            raise TypeError("league must be a string")
        elif league not in ["NBA","WNBA"]:
            raise ValueError("league must be either 'NBA' or 'WNBA'")
        else:
            self.league = league

        if not isinstance(season_type,str):
            raise TypeError("season_type must be a string")
        elif season_type not in ["regular","playoff"]:
            raise ValueError ("season_type must be either 'regular' or 'playoff")
        else:
            self.season_type = season_type

        if not isinstance(data_type,str):
            raise TypeError("data_type must be a string")
        elif data_type not in ["team","player"]:
            raise ValueError("data_type must be either 'team' or 'player'")
        else:
            self.data_type = data_type

        if not isinstance(year,str):
            raise TypeError("year must be a string")
        elif "-" not in year:
            raise ValueError("year must be in YYYY-YY format")
        elif not year.replace("-","").isdigit():
            raise ValueError("year must be in YYYY-YY format")
        elif int(year.split("-")[0][-2:]) - int(year.split("-")[1]) != -1:
            raise ValueError("year must be in YYYY-YY format")
        elif int(year.split("-")[0]) < 1946 or int(year.split("-")[0]) > 2023:
            raise ValueError("year not within allowable values")
        else:
            self.year = year

        # Generate URL
        # can probably use a dictionary
        base = "https://www.basketball-reference.com/"

        self.url = base + "leagues/NBA_20" + year.split("-")[1]

        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, "html.parser")

        #https://www.basketball-reference.com/leagues/NBA_2023.html
        def get_per_game_stats(self,stats_type):
            # stats_type -> one of team, opponent
            pass

        def get_total_stats(self,stats_type):
            pass

        def get_per_100_poss_stats(self,stats_type):
            pass

        def get_advanced_stats():
            pass

        def get_shooting_stats(self,stats_type):
            pass

        def get_league_awards(self):
            pass

        def get_players_of_the_week(self):
            pass

        def get_players_of_the_month(self):
            pass
        
        # https://www.basketball-reference.com/playoffs/NBA_2023.html
        

#x = BasketBallReferenceConnection()

        
        # league -> one of NBA, WNBA
        # season_type -> one of regular, playoffs
        # data_type -> one of team, player
        # year -> year in the format of 2022-23 (str)
        # what about defaults?
        # league -> NBA
        # season_type -> regular
        # data_type -> team
        # year -> current_year
        
        # Purpose
        # User fills in values for all the above
        # constructor generates the appropriate URL given the information
        # constructor pulls data and creates soup object based on the URL 

        # So, this one constructor should be able to generate all URLs. 
        # Issue -> since you've generalized at this stage, all your methods won't work. 
        # you'll need to validate that you have the right method for the data
        # ex. highest ppg player wont work on team data

        # other considerations
        # raise errors for anything that wont work -> bad user input 
        # validating connection -> what if user isn't connected on the internet? what is website is down?
        # what if the website url changed and the data you want isn't there anymore?
        # how can you ensure that you're getting the right data and formatting it correctly? (to the best of your abilities)

        # how can you distribute your data so that its easily accesible? pandas, dict, csv, etc.

        # URLs
        # https://www.basketball-reference.com/leagues/NBA_2023.html -> Team info regular season
        # https://www.basketball-reference.com/playoffs/NBA_2023.html -> team info playoffs
        # https://www.basketball-reference.com/leagues/NBA_2023_per_game.html -> player stats per game regular
        # https://www.basketball-reference.com/leagues/NBA_2023_per_minute.html -> player stats per minute regular

#         # create issues https://github.com/chocolate-sprinkles/Data-Analysis-Portfolio/issues/1 and track your work here


#         remote: Resolving deltas: 100% (3/3), completed with 1 local object.
# remote: warning: See https://gh.io/lfs for more information.
# remote: warning: File stratascratch/evolent health - beer data analysis/BeerDataScienceProject.tar.bz2 is 92.10 MB; this is larger than GitHub's recommended maximum file size of 50.00 MB
# remote: warning: GH001: Large files detected. You may want to try Git Large File Storage - https://git-lfs.github.com.
# To https://github.com/chocolate-sprinkles/Data-Analysis-Portfolio.git
#    6413077..a8b4ac6  main -> main

        # so, for any methods, you can check the URL you're working with. you'll know that for a URL of a certain type, you can 
        # do some stuff and for other ones, you cannot
