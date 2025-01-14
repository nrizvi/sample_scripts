import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd
import numpy as np

data_df = pd.read_excel('ableist_lang_by_year.xlsx')
data_df = data_df.drop(columns=['Unnamed: 0'])
grouped_df = data_df.groupby(['Year']).mean()
print(grouped_df.columns)
x = grouped_df.index.values
y = grouped_df['ableist_lang_ratio']
plt.scatter(x = grouped_df.index.values, y=grouped_df['ableist_lang_ratio'], c = '#5ba300')
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
font = {'family': 'serif',
        'weight': 'bold',
        'size': 18}

matplotlib.rc('font', **font)

#add trendline to plot
plt.plot(x, p(x), c='#b51963')
plt.show()