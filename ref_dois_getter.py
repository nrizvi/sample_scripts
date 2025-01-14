import pandas as pd
import requests
import time
import json
import numpy as np

## STEPS:
## DELETE LAST ROW IN REFERENCE_DOIS EXCEL FILE
## THIS TAKES HOURS TO RUN
## SEGMENT THE DATA, DO FIRST 500 TO TEST IF THE CODE RUNS PROPERLY
## SPLIT KEY AT "_"[0]
## COUNT HOW MANY TIMES PAPERID APPEARS
## SAVE THE OUTPUT IN AN EXCEL FILE
## OBTAIN PAPERIDS OF TOP 200 PAPERS (BASED ON COUNT), ARRANGED IN DESCENDING ORDER
## GIVE PAPERIDs and INFO (e.g. TITLE, ABSTRACT, ETC) to Naba

# Load paper_dois_all.xlsx into a dataframe
df = pd.read_excel('paper_dois_all.xlsx', sheet_name='Sheet1')

#delete the main corpus column


L = np.ravel(df.T).tolist()
paperids = list()

for element in L:
    if str(element) != "nan":
        paperids.append(element)

print(paperids)

#abstract, title, field, year, authors
#df = paperID, title, author, year, abstract

# Initialize the results dictionary
#
# # example DOI
api_url = "https://api.semanticscholar.org/v1/paper/"

# for doi in paperids:
#     response = requests.get(api_url + doi)
#     if response.status_code == 200:
#         data = json.loads(response.content)
#         paper_id = data['paperId']
#         paper_ids.append(paper_id)
#         print("Semantic Scholar Paper ID:", paper_id)
#     else:
#         print("Error getting Semantic Scholar paper ID.")
# print(paper_ids)
# # Loop through the DOIs and find their references
results_dict = {}
i = 0
for doi in paperids:
    # Wait for 50 seconds between requests
    time.sleep(3)

    # Send the request to the Semantic Scholar API
    response = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=title,fieldsOfStudy,publicationDate,abstract')

    # If the request is successful, extract the reference DOIs
    i+=1
    if response.status_code == 200:
        title = response.json()['title']
        field = response.json()['fieldsOfStudy']
        pub_date = response.json()['publicationDate']
        abstract = response.json()['abstract']
        paper_info = [title,field,pub_date,abstract]
        new_key = doi+'_'+str(i)
        results_dict[new_key] = paper_info

        # Replace the DOI keys with corresponding titles in map_dict

        # Store the reference DOIs and titles in the results_dict
        #print(results_dict)
print(results_dict)



# print(new_dict)
# Create a dataframe from the results_dict
results_df = pd.DataFrame.from_dict(results_dict, orient='index', columns=['title', 'field', 'date', 'abstract'])
results_df.to_excel('reference_info_all.xlsx')

#pd.set_option('display.max_colwidth', 10)

# print(results_df.index)

# Write the results to a new excel file
