import time
from selenium import webdriver
from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import json
from heapq import nlargest


dois_df = pd.read_excel('paper_dois.xlsx', 'Sheet1')
dois_list = dois_df.doi.values.tolist()

#print(dois_list)

#icra48506.2021.9561687?fields=citationCount

results_dict = {}
for doi in dois_list:
    #print(doi)
    driver = webdriver.Chrome()
    driver.get("https://api.semanticscholar.org/graph/v1/paper/"+str(doi)+"?fields=citationCount,title")
    driver.implicitly_wait(8)
    results_text = driver.find_element(By.XPATH, "//body").text
    if 'error' not in results_text:
        dict = json.loads(results_text)
        print(dict)
        results_dict[doi] = dict['citationCount']
print(results_dict)

res = nlargest(25, results_dict, key = results_dict.get)
results_df = pd.DataFrame.from_dict(res)
results_df.to_excel("top_most_cited_papers_dois.xlsx")
results_all_df = pd.DataFrame.from_dict([results_dict])
results_all_df.to_excel("most_cited_papers_dois.xlsx")


