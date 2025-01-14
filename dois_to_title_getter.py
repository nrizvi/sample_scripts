import pandas as pd


dois_df = pd.read_excel('paper_dois.xlsx', 'Sheet1')
venues_df = pd.read_excel('papers_by_year.xlsx', 'Included papers')
most_cited_df = pd.read_excel('most_cited_papers_dois.xlsx', 'Sheet1')
merged_df = pd.merge(left=venues_df, right=dois_df, how='left', left_on='Title', right_on='title')
merged_df = merged_df.set_index('doi')
most_cited_df = most_cited_df.set_index(0)
print(merged_df)
print(most_cited_df)
most_cited_titles = pd.merge(most_cited_df, merged_df, left_index=True, right_index=True)
print(most_cited_titles.columns.values)
most_cited_titles = most_cited_titles.rename(columns={'Unnamed: 0_x':'citation_rank'})
most_cited_titles = most_cited_titles.set_index('citation_rank')
most_cited_titles = most_cited_titles.drop_duplicates(subset=['Title'])
most_cited_titles = most_cited_titles.drop(columns=['title','Unnamed: 0_y'])
print(most_cited_titles)

merged_df = merged_df.sort_values(by=['Unnamed: 0'])
merged_df.to_excel("included_papers.xlsx")
most_cited_titles = most_cited_titles.sort_values(by=['citation_rank'])
most_cited_titles.to_excel('most_cited_papers.xlsx')
