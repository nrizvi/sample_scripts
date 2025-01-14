import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colors


#data_df = pd.read_excel('cleaned_papers.xlsx')
df = pd.read_excel('Robots & Autism_ Usage Breakdown.xlsx')
# print(df['gender minorities representation'])
# count = (df['gender minorities representation'] > 0.33).sum()
# #result = df[df['gender minorities representation'] >= 0.33].groupby('Year')['Year'].count()
# result = df[df['gender minorities representation'] >= 0.33].groupby('conference')['conference'].count()
# less_than_point_three_three = df[df['gender minorities representation'] < 0.33].groupby('conference')['conference'].count()
# 
# 'conference'
# print(less_than_point_three_three)
# 
# print(result)
# data_df = data_df.drop(columns=['Unnamed: 0'])
#cleaned_df = data_df['paper_ID'].str.split("_")
# data_df['venue']= cleaned_df
print(df['Robot Type'].value_counts())
# #data_df["venue"] = data_df["venue"].str[0]
# data_df.to_excel("gender_rep.xlsx")
#
# print(data_df.head())
# data_df['Year'] = data_df['Year'].astype(int)
# data_df = data_df.pivot_table(index='Year', columns='conference', values='gender minorities representation', aggfunc='mean')
# print(data_df)
# # data_df_ordered = data_df[['IJSR', 'ICHRI', 'THRI', 'ICRA','SR',"CHI",'Other']]
# # good_colors = ['#5ba300','#89ce00','#0073e6','#e6308a','#b51963']
# # bad_colors = good_colors[::-1]
# # sns.set(font_scale=1.2)
#
# # cmap = colors.ListedColormap(bad_colors)
# # #cmap = LinearSegmentedColormap.from_list(colors=bad_colors)
# #
# # sns.heatmap(data_df_ordered, annot=True, cmap=cmap)
# # plt.show()
#
# avg_per_conf_year = df.groupby("conference").mean()
#
# # Group the data by year and calculate the mean per conference
# avg_per_year_conf = df.groupby("Year").mean()
#
# # Print the average per year and per conference
# print("Average per year and per conference:")
# print(avg_per_conf_year)
# print("\nAverage per conference and per year:")
# print(avg_per_year_conf)