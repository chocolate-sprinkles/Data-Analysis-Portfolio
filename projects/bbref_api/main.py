import requests
import pandas as pd
from bs4 import BeautifulSoup

class BasketBallReferenceConnection:

    # Solve getting the correct URL first
    def __init__(self,league,season_type,data_type,year):
        pass
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