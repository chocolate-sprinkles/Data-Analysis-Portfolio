# class Employee:
    
#     def __init__(self,name,emp_id,salary):
#         self.name = name
#         self.emp_id = emp_id
#         self.salary = salary

# x = Employee("James",12345,90000)
# print(x.name)

# def test():
#     return Employee("Jason",123,201239)

# print(test().salary)

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

class bbref():

    def __init__(self,stats_type):
        if stats_type == "league":
            self.stats_type = "https://www.basketball-reference.com/leagues/NBA_2023.html"
            response = requests.get(self.stats_type)
            self.stats_type = BeautifulSoup(response.content, "html.parser")
    
    def get_per_game_stats(self):
        bbref_html_table = self.stats_type.find('table', {"id": "per_game-team"})
        bbref_stats = pd.read_html(str(bbref_html_table))[0]
        bbref_stats["Team"] = bbref_stats["Team"].apply(lambda x: x.replace("*",""))
        bbref_stats = bbref_stats.iloc[:-1]
        return bbref_stats
    
    def get_total_stats(self):
        bbref_html_table = self.stats_type.find('table', {"id": "totals-team"})
        bbref_stats = pd.read_html(str(bbref_html_table))[0]
        bbref_stats["Team"] = bbref_stats["Team"].apply(lambda x: x.replace("*",""))
        bbref_stats = bbref_stats.iloc[:-1]
        return bbref_stats
    
x = bbref("league")
print(x.get_per_game_stats())
print(x.get_total_stats())
