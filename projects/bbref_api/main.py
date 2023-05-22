import requests
import pandas as pd
from bs4 import BeautifulSoup
from bs4 import Comment 

class BasketballReferenceConnection:

    def __init__(self,league,season_type,data_type,year):
        
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
        elif [self.league,self.season_type,self.data_type] == ["NBA","playoffs","team"]:
            self.url_type = 2
        elif [self.league,self.season_type,self.data_type] == ["NBA","regular","player"]:
            self.url_type = 3
        elif [self.league,self.season_type,self.data_type] == ["NBA","playoffs","player"]:
            self.url_type = 4

    def get_stats(self,stats_type,opponent,**kwargs):
        # stats_type one of "pg","total","per 100","adv","shooting"

        if "player_stat_type" not in kwargs.keys() and self.data_type == "player":
            kwargs["player_stat_type"] = "pg"

        url_suffix_mapping = {"total":"_totals","pg":"_per_game","per 36":"_per_minute","per 100":"_per_poss","adv":"_advaced","pbp":"_play-by-play","shooting":"_shooting","adj shooting":"_adj_shooting"}
        base = "https://www.basketball-reference.com/"
        end = ".html"
        url_mapping = {"NBA":"NBA_","WNBA":"wnba","regular":"leagues/","playoffs":"playoffs/","team":"","player":"_per_game"}
        self.url = base + url_mapping[self.season_type] + url_mapping[self.league] + self.year[:2] + self.year[-2:] + url_suffix_mapping[kwargs["player_stat_type"]] + end
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, "html.parser")



        if self.url_type == 1:

            css_id_mapping = {"pg":"per_game-","total":"totals-","per 100":"per_poss-","adv":"advanced-","shooting":"shooting-",False:"team",True:"opponent"}
            css_id = css_id_mapping[stats_type] + css_id_mapping[opponent]
            if stats_type == "adv":
                css_id = "advanced-team"
            stats_df = pd.read_html(str(self.soup.find('table', {"id": css_id})))[0]

            advanced_cols = ['Rk','Team','Age','W','L','PW','PL','MOV','SOS','SRS','ORtg','DRtg','NRtg','Pace','FTr','3PAr','TS%','Unnamed: 17_level_1','eFG%_off','TOV%_off','ORB%_off','FT/FGA_off','Unnamed: 22_level_1','eFG%_def','TOV%_def','DRB%_def','FT/FGA_def','Unnamed: 27_level_1','Arena','Attend.','Attend./G']

            shooting_cols_team = ['Rk','Team','G','MP','FG%','Dist.','Unnamed: 6_level_1','pct_FGA_2P','pct_FGA_0-3','pct_FGA_3-10','pct_FGA_10-16','pct_FGA_16-3P','pct_FGA_3P','Unnamed: 13_level_1','fga_pct_2P','fga_pct_0-3','fga_pct_3-10','fga_pct_10-16','fga_pct_16-3P','fga_pct_3P','Unnamed: 20_level_1','pct_ast_2P', 'pct_ast_3P','Unnamed: 23_level_1','dunk_FGA%','dunk_Md.','Unnamed: 26_level_1','layup_FGA%','layup_Md.','Unnamed: 29_level_1','corner_%3PA','corner_3P%',"Unnamed: 32_level_1","heaves_att","heaves_md"]

            shooting_cols_opponent = shooting_cols_team[:-3]

            if "advanced" in css_id:
                stats_df.columns = advanced_cols
                stats_df = stats_df.drop(['Unnamed: 17_level_1','Unnamed: 22_level_1','Unnamed: 27_level_1'],axis=1).copy(deep=True)
            elif css_id == "shooting-team":
                stats_df.columns = shooting_cols_team
                stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1','Unnamed: 32_level_1'],axis=1).copy(deep=True)
            elif css_id == "shooting-opponent":
                stats_df.columns = shooting_cols_opponent
                stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1'],axis=1).copy(deep=True)

            stats_df["Team"] = stats_df["Team"].apply(lambda team_name: team_name.replace("*",""))
            stats_df = stats_df[~stats_df.isnull().T.any()]
            return stats_df
        
        elif self.url_type == 2:
            
            css_id_mapping = {"pg":"per_game-","total":"totals-","per 100":"per_poss-","adv":"advanced-","shooting":"shooting-",False:"team",True:"opponent"}
            css_id = css_id_mapping[stats_type] + css_id_mapping[opponent]
            if stats_type == "adv":
                css_id = "advanced-team"

            comment_ids = ["per_poss-team","per_poss-opponent","shooting-team","shooting-opponent"]
            tags = {}

            for comment in self.soup(text=lambda text: isinstance(text, Comment)):
                for comment_id in comment_ids:
                    if comment_id in comment.string:
                        tags[comment_id] = BeautifulSoup(comment,"html.parser")


            if css_id in tags.keys():
                stats_df = pd.read_html(str(tags[css_id].find('table', {"id": css_id})))[0]
            else:
                stats_df = pd.read_html(str(self.soup.find('table', {"id": css_id})))[0]

            advanced_cols = ['Rk','Team','Age','W','L','W/L%','PW','PL','ORtg','DRtg','NRtg','Pace','FTr','3PAr','TS%','Unnamed: 15_level_1','eFG%_off','TOV%_off','ORB%_off','FT/FGA_off','Unnamed: 20_level_1','eFG%_def','TOV%_def','DRB%_def','FT/FGA_def']

            shooting_cols_team = ['Rk','Team','G','MP','FG%','Dist.','Unnamed: 6_level_1','pct_FGA_2P','pct_FGA_0-3','pct_FGA_3-10','pct_FGA_10-16','pct_FGA_16-3P','pct_FGA_3P','Unnamed: 13_level_1','fga_pct_2P','fga_pct_0-3','fga_pct_3-10','fga_pct_10-16','fga_pct_16-3P','fga_pct_3P','Unnamed: 20_level_1','pct_ast_2P', 'pct_ast_3P','Unnamed: 23_level_1','dunk_FGA%','dunk_Md.','Unnamed: 26_level_1','layup_FGA%','layup_Md.','Unnamed: 29_level_1','corner_%3PA','corner_3P%',"Unnamed: 32_level_1","heaves_att","heaves_md"]

            shooting_cols_opponent = shooting_cols_team[:-3]

            if "advanced" in css_id:
                stats_df.columns = advanced_cols
                stats_df = stats_df.drop(['Unnamed: 15_level_1','Unnamed: 20_level_1'],axis=1).copy(deep=True)
            elif css_id == "shooting-team":
                stats_df.columns = shooting_cols_team
                stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1','Unnamed: 32_level_1'],axis=1).copy(deep=True)
            elif css_id == "shooting-opponent":
                stats_df.columns = shooting_cols_opponent
                stats_df = stats_df.drop(['Unnamed: 6_level_1','Unnamed: 13_level_1','Unnamed: 20_level_1','Unnamed: 23_level_1','Unnamed: 26_level_1','Unnamed: 29_level_1'],axis=1).copy(deep=True)

            stats_df = stats_df[~stats_df.isnull().T.any()]
            return stats_df
        
        elif self.url_type == 3:
            css_id = {"total":"totals_stats","pg":"per_game_stats","per 36":"per_minute_stats","per 100":"per_poss_stats","adv":"advanced_stats","pbp":"pbp_stats","shooting":"shooting_stats","adj shooting":"adj-shooting"}


        elif self.url_type == 4:
            css_id = {"total":"totals_stats","pg":"per_game_stats","per 36":"per_minute_stats","per 100":"per_poss_stats","adv":"advanced_stats","pbp":"pbp_stats","shooting":"shooting_stats","adj shooting":"adj-shooting"}
        
