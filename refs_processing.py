import PyPDF2
import re
import os
import pandas as pd
import numpy as np
import copy
from collections import Counter

CHI_df = pd.read_excel('reference_DOIS.xlsx', 'CHI')
ICHRI_df = pd.read_excel('reference_DOIS.xlsx', 'ICHRI')
ICRA_df = pd.read_excel('reference_DOIS.xlsx', 'ICRA')
IJSR_df = pd.read_excel('reference_DOIS.xlsx', 'IJSR')
Other_df = pd.read_excel('reference_DOIS.xlsx', 'Other')
SR_df = pd.read_excel('reference_DOIS.xlsx', 'SR')
THRI_df = pd.read_excel('reference_DOIS.xlsx', 'THRI')

ref_df = pd.concat([CHI_df, ICHRI_df, ICRA_df, IJSR_df, Other_df, SR_df, THRI_df], axis = 1)

#print(ref_df)
column_headers = list(ref_df.columns.values)
counter = Counter()
for column_header in column_headers:
    this_list = ref_df[column_header].values.tolist()
    if type(this_list[0]) == list:
        this_list = [this[0] for this in this_list]
    counter.update(Counter(this_list))

#print(counter)

dupes_dict = {}
ref_list = []
count_list = []
dupes_dict['doi'] = []
dupes_dict['count'] = []
for reference, count in counter.items():
    if count > 1:
        dupes_dict['doi'].append(reference)
        dupes_dict['count'].append(count)

dupes_df = pd.DataFrame.from_dict(dupes_dict)
dupes_df = dupes_df.sort_values(by=['count'], ascending=False)
cleaned_df = dupes_df[dupes_df['doi'].str.contains("doi", na=False)]
print(cleaned_df)



cleaned_df.to_excel("reference_counts.xlsx")
#
# dupes_df = ref_df[ref_df.duplicated()]
#
# papers = dupes_df.stack().values
# print(papers)