## THIS FILE GETS ALL THE REFERENCES OF THE PAPERS AND SAVES THEM IN AN EXCEL FILE

import PyPDF2
import re
import os
import pandas as pd
import numpy as np
import copy

directory = 'papers'
conferences = []
papers = []
refs_by_conf_dict = {}
for filename in os.listdir(directory):
    conference = filename.split('_')[0]
    paper = filename.split('.pdf')[0]
    if conference not in conferences:
        conferences.append(conference)
        refs_by_conf_dict[conference] = {}
    if paper not in papers:
        papers.append(paper)


    # f = os.path.join(directory, filename)

    # checking if it is a file

    # if os.path.isfile(f):
    #
    #     # open the pdf file
    #
    #     print(filename)

        #
paper_refs_dict = {}
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        object = PyPDF2.PdfReader(f)
        NumPages = len(object.pages)

        for i in range(0, NumPages):
            PageObj = object.pages[i]
            # print("this is page " + str(i))
            Text = PageObj.extract_text()
            if re.search(r'references(.*?)', Text, re.IGNORECASE):
                paper_refs_dict[filename.split('.pdf')[0]] = Text
#print(paper_refs_dict)
            # print all at once
            #print(text)
        #print(f)
for conf in conferences:
    for paper, citation in paper_refs_dict.items():
        if paper.split('_')[0] in conf:
            refs_by_conf_dict[conf][paper] = citation

metaDF = {'venue': [], 'paper': [], 'references': []}

for venue in refs_by_conf_dict:
    for paper in refs_by_conf_dict[venue]:
        references = refs_by_conf_dict[venue][paper]
        metaDF['venue'].append(venue)
        metaDF['paper'].append(paper)
        metaDF['references'].append(references)

refs_df = pd.DataFrame.from_dict(metaDF, orient="columns")

grouped_refs_df = refs_df.groupby(['venue'])

print(grouped_refs_df.head())

with pd.ExcelWriter("references.xlsx") as writer:
    for venue, data in grouped_refs_df:
        data.to_excel(writer, sheet_name = venue)
    # grouped_refs_df.get_group(conf).to_excel("/refs_excels/"+str(conf)+"_refs.xlsx")
    #refs_by_conf_dict[each_venue].values()
# citations_df = pd.DataFrame.from_dict(refs_by_conf_dict)
# print(citations_df)
# for conf in conferences:
#     for title in papers:
#         if title.split('_')[0] in conf:
#             refs_by_conf_dict[conf][title] = ''
#
            #refs_by_conf_dict[conference][title] = ''

#print(refs_by_conf_dict)
