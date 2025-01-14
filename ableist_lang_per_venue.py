import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import colors


data_df = pd.read_excel('ableist_lang_by_year.xlsx')
data_df = data_df.drop(columns=['Unnamed: 0'])
cleaned_df = data_df['paper_ID'].str.split("_")
data_df['venue']= cleaned_df

data_df["venue"] = data_df["venue"].str[0]

data_df = data_df.pivot_table(index='Year', columns='venue', values='ableist_lang_ratio', aggfunc='mean')
data_df_ordered = data_df[['IJSR', 'ICHRI', 'THRI', 'ICRA','SR',"CHI",'Other']]
data_df_ordered = data_df_ordered.iloc[::-1]

good_colors = ['#5ba300','#89ce00','#0073e6','#e6308a','#b51963']
bad_colors = good_colors[::-1]

#
#
print(data_df_ordered.head())

cmap = colors.ListedColormap(good_colors)
sns.set(font_scale=1.2)
#
sns.heatmap(data_df_ordered, annot=True, cmap=cmap)

#
#

#plt.scatter(x = data_df['Year'], y=data_df['ableist_lang_ratio'])

plt.show()