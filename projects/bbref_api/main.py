import requests
import pandas as pd
from bs4 import BeautifulSoup

class BasketBallReferenceConnection:

    def __init__(self,league,season_type,data_type,year):
        
        # WNBA will be updated later
        if not isinstance(league,str):
            raise TypeError("league must be a string")
        elif league not in ["NBA","WNBA"]:
            raise ValueError("league must be either 'NBA' or 'WNBA'")
        else:
            self.league = league

        if not isinstance(season_type,str):
            raise TypeError("season_type must be a string")
        elif season_type not in ["regular","playoffs"]:
            raise ValueError ("season_type must be either 'regular' or 'playoffs")
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
        base = "https://www.basketball-reference.com/"
        end = ".html"
        url_mapping = {"NBA":"NBA_","WNBA":"wnba","regular":"leagues/","playoffs":"playoffs/","team":"","player":"_per_game"}

        self.url = base + url_mapping[self.season_type] + url_mapping[self.league] + self.year[:2] + self.year[-2:] + url_mapping[self.data_type] + end

        # Generate soup object
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, "html.parser")

        if [self.league,self.season_type,self.data_type] == ["NBA","regular","team"]:
            self.url_type = 1
        elif [self.league,self.season_type,self.data_type] == ["NBA","playoff","team"]:
            self.url_type = 2
        elif [self.league,self.season_type,self.data_type] == ["NBA","regular","player"]:
            self.url_type = 3
        elif [self.league,self.season_type,self.data_type] == ["NBA","playoff","player"]:
            self.url_type = 4

        #https://www.basketball-reference.com/leagues/NBA_2023.html
        # so get playoff stats has similar stats 
        # from a user experience, if you say get_stats(), you'll want to get them regardless of which url you have 
        # rename this to get team stats and have another called player stats. have this one handle playoff and regular season urls.
        def get_stats(self,stats_type,opponent):
            # stats_type one of "pg","total","per 100","adv","shooting"
            # css_ids
            # per_game-team
            # per_game-opponent
            # totals-team
            # totals-opponent
            # per_poss-team
            # per_poss-opponent
            # advanced-team
            # shooting-team
            # shooting-opponent

            if self.url_type == 1:

                css_id_mapping = {"pg":"per_game-","total":"totals-","per 100":"per_poss-","adv":"advanced-","shooting":"shooting-",False:"team",True:"opponent"}
                css_id = css_id_mapping[stats_type] + css_id_mapping[opponent]
                stats_df = pd.read_html(str(self.soup.find('table', {"id": css_id})))[0]

                advanced_cols = ['Rk','Team','Age','W','L','PW','PL','MOV','SOS','SRS','ORtg','DRtg','NRtg','Pace','FTr','3PAr','TS%','Unnamed: 17_level_1','eFG%_off','TOV%_off','ORB%_off','FT/FGA_off','Unnamed: 22_level_1','eFG%_def','TOV%_def','DRB%_def','FT/FGA_def','Unnamed: 27_level_1','Arena','Attend.','Attend./G']

                shooting_cols_team = ['Rk','Team','G','MP','FG%','Dist.','Unnamed: 6_level_1','pct_FGA_2P','pct_FGA_0-3','pct_FGA_3-10','pct_FGA_10-16','pct_FGA_16-3P','pct_FGA_3P','Unnamed: 13_level_1','fga_pct_2P','fga_pct_0-3','fga_pct_3-10','fga_pct_10-16','fga_pct_16-3P','fga_pct_3P','Unnamed: 20_level_1','pct_ast_2P', 'pct_ast_3P','Unnamed: 23_level_1','dunk_FGA%','dunk_Md.','Unnamed: 26_level_1','layup_FGA%','layup_Md.','Unnamed: 29_level_1','corner_%3PA','corner_3P%',"heaves_att","heaves_md"]

                shooting_cols_opponent = shooting_cols_team[:-2]

                # if "advanced" in css_id:
                #     stats_df.columns = advanced_cols
                #     stats_df = stats_df.drop(['Unnamed: 17_level_1','Unnamed: 22_level_1','Unnamed: 27_level_1'],axis=1).copy(deep=True)
                #     stats_df["Team"] = stats_df["Team"].apply(lambda team_name: team_name.replace("*",""))
                #     stats_df = stats_df.iloc[:-1]
                #     return stats_df
                # elif css_id == "shooting-team":
                #     stats_df.columns = shooting_cols_team
                #     stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1','Unnamed: 32_level_1'],axis=1).copy(deep=True)
                #     stats_df["Team"] = stats_df["Team"].apply(lambda team_name: team_name.replace("*",""))
                #     stats_df = stats_df.iloc[:-1]
                #     return stats_df
                # elif css_id == "shooting-opponent":
                #     stats_df.columns = shooting_cols_opponent
                #     stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1'],axis=1).copy(deep=True)
                #     stats_df["Team"] = stats_df["Team"].apply(lambda team_name: team_name.replace("*",""))
                #     stats_df = stats_df.iloc[:-1]
                #     return stats_df
                # else:
                #     stats_df["Team"] = stats_df["Team"].apply(lambda team_name: team_name.replace("*",""))
                #     stats_df = stats_df.iloc[:-1]
                #     return stats_df

                # can reduce this further with a dictionary for column renaming and then probably a function to pass all unnamed column names to the drop method
                if "advanced" in css_id:
                    stats_df.columns = advanced_cols
                    stats_df = stats_df.drop(['Unnamed: 17_level_1','Unnamed: 22_level_1','Unnamed: 27_level_1'],axis=1).copy(deep=True)
                elif css_id == "shooting-team":
                    stats_df.columns = shooting_cols_team
                    stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1','Unnamed: 32_level_1'],axis=1).copy(deep=True)
                elif css_id == "shooting-opponent":
                    stats_df.columns = shooting_cols_opponent
                    stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1'],axis=1).copy(deep=True)

                stats_df["Team"] = stats_df["Team"].apply(lambda team_name: team_name.replace("*",""))
                stats_df = stats_df.iloc[:-1]
                return stats_df
            
            else:
                # so, is this good user experience to do this? how do they know which method to use? get_stats is kinda all encompassing
                raise Exception("Cannot use this method for this object")

        def get_league_awards(self):
            pass

        def get_players_of_the_week(self):
            pass

        def get_players_of_the_month(self):
            pass
        
        # https://www.basketball-reference.com/playoffs/NBA_2023.html
        def get_playoff_per_game_stats():
            pass

        def get_playoff_total_stats():
            pass

        def get_playoff_per_100_poss_stats():
            pass

        def get_playoff_advanced_stats():
            pass

        def get_playoff_shooting_stats():
            pass

        # https://www.basketball-reference.com/leagues/NBA_2023_per_game.html
        #how do I want to combine these? I can use probably one URL to get all this info

        def get_player_per_game_stats():
            pass

        def get_points_pg_leaders():
            pass

        def get_rebounds_pg_leaders():
            pass
        
        def get_assists_pg_leaders():
            pass

        def get_steals_pg_game_leaders():
            pass

        def get_blocks_pg_game_leaders():
            pass

        def get_field_goal_pct_leaders():
            pass

        def get_free_throw_pct_leaders():
            pass

        def get_3pt_field_goal_pct_leaders():
            pass

        def get_2pt_field_goal_pct_leaders():
            pass

        def get_eff_field_goal_pct_leaders():
            pass
        
        def get_minutes_pg_leaders():
            pass

# League Leaders Categories
# points
# points per game -> inculuded
# total rebounds
# rebounds per game -> included 
# offensive rebounds
# defensive rebounds
# assists
# assists per game -> included
# steals
# steals per game -> included
# blocks
# blocks per game -> included
# field goal percentage -> included
# free throw percentage -> included
# 3-pt field goal percentage -> included
# 2-pt field goal percentage -> included
# effective field goal percentage (pct) -> included
# true shooting pct 
# field goals  
# field goal attempts 
# 2-pt field goals 
# 2-pt field goal attempts 
# 3-pt field goals 
# 3-pt field goal attempts 
# field goals missed 
# free throws 
# free throw attempts 
# minutes played 
# minutes per game 
# turnovers 
# personal fouls
# player efficiency rating 
# win shares 
# offensive win shares
# defensive winshares 
# win shares per 48 mins 
# box plus/minus
# offensive box plus/minus
# value over replacement player 
# offensive rating 
# defensive rating 
# usage pct 
# total rebound pct 
# offensive rebound pct 
# assist pct 
# defensive rebound pct 
# steal pct 
# block pct 
# turnover pct 

# x = BasketBallReferenceConnection("NBA","regular","team","2022-23")
# print(x.url)
# x = BasketBallReferenceConnection("NBA","regular","player","2022-23")
# print(x.url)
# x = BasketBallReferenceConnection("NBA","playoffs","team","2022-23")
# print(x.url)
# x = BasketBallReferenceConnection("NBA","playoffs","player","2022-23")
# print(x.url)
# x = BasketBallReferenceConnection("NBA","regular","team","1995-96")
# print(x.url)
        
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

        # See if you can publish the package on PyPi. Would be a good add
