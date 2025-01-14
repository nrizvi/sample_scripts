import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

data_df = pd.read_excel('Robots & Autism_ Usage Breakdown.xlsx')
#data_c_df = data_df.drop[data_df["Paper ID"] =='CHI_12']
data_df = data_df.drop(data_df.index[11])
#print(data_df.head())

column_names = list(data_df.columns.values)
paper_ids = list(data_df['Paper ID'])
#print(paper_ids)

nodes = [
   ['id', 'label', 'color']
]

colors = sns.color_palette("blend:#84dcc6,#ff686b", len(paper_ids)).as_hex()
new_lists = []

for i in range(len(paper_ids)):
    new_list = []
    new_list.append(i)
    new_list.append(paper_ids[i])
    new_list.append(colors[i])
    new_lists.append(new_list)

for lst in new_lists:
    nodes.append(lst)

#print(nodes)

darker_colors = sns.color_palette("blend:#064247,#893508", 14).as_hex()

# print(darker_colors)
# print(column_names)




def get_nodes(given_list):
    auto_lists = []
    for i in range(len(given_list)):
        auto_list = []
        c = sns.color_palette("blend:#064247,#893508", len(given_list)).as_hex()
        #print(c)
        auto_list.append(len(nodes)-1+i)
        auto_list.append(given_list[i])
        auto_list.append(c[i])
        auto_lists.append(auto_list)

    for lst in auto_lists:
        nodes.append(lst)
    return nodes


def clean_values(lst):
    for val in lst:
        val = str(val)
        if '; ' in val:
            new_vals = val.split('; ')
            lst.remove(val)
            for i in new_vals:
                lst.append(i)
    return list(set(lst))


def mapping(lst1, lst2):
    ids_dict = {}
    for val in lst1:
        for v in lst2:
            if v in val:
                ids_dict[v] = val[0]
    return ids_dict
#print(auto_unique)
#print(data_df)

#FORMAT: the first dict should be the values from the df, second dict = map of value on the left, third dict = map of value on the right
def return_nums(dict1, dict2, dict3):
    new_dict = {}
    for k,v in dict1.items():
        for i,j in dict2.items():
            if k == i:
                for b,c in dict3.items():
                    if v == b:
                        new_dict[j] = c
    return new_dict

comm_unique = list(data_df['Communication Media'].unique())
comm_unique = clean_values(comm_unique)
get_nodes(comm_unique)
#print(nodes)
data_c_unique = list(data_df['Data Collected'].unique())

data_c_unique = clean_values(data_c_unique)
print(data_c_unique)
#print(get_nodes(use_unique))

links = [
   ['Source', 'Target', 'Value', 'Link Color']
]

comm_ids_map = mapping(nodes,comm_unique)
paper_ids_map = mapping(nodes,paper_ids)
data_c_ids_map = mapping(nodes, data_c_unique)


first_dict = dict(zip(data_df['Paper ID'], data_df['Data Collected'].str.split('; ')))
second_dict = dict(zip(data_df['Paper ID'], data_df['Data Collected'].str.split('; ')))


dict_1 = return_nums(first_dict, paper_ids_map, data_c_ids_map)
print(nodes)

# WHATEVER is the color of the key = the link color

link_list = []
for k,v in dict_1.items():
    lyst = []
    for i in nodes:
        if str(k) == str(i[0]):
            lyst.append(k)
            lyst.append(v)
            lyst.append(2)
            lyst.append(i[2])
    link_list.append(lyst)

for lyst in link_list:
    links.append(lyst)
#print(links)

## THIS PART BEGINS THE VISUALIZATION

nodes_headers = nodes.pop(0)
links_headers = links.pop(0)

df_nodes = pd.DataFrame(nodes, columns = nodes_headers)
df_links = pd.DataFrame(links, columns = links_headers)

fig = go.Figure(data=[go.Sankey(
   node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = df_nodes['label'].dropna(axis=0, how='any'),
      color = df_nodes['color']
   ),

   link = dict(
      source=df_links['Source'].dropna(axis=0, how='any'),
      target=df_links['Target'].dropna(axis=0, how='any'),
      value=df_links['Value'].dropna(axis=0, how='any'),
      color=df_links['Link Color'].dropna(axis=0, how='any'),
   )
)])

fig.update_layout(
   title_text="DataFrame-Sankey diagram",
   font_size=10
)

fig.show()

count = data_df[column_names].nunique()
print(count.sort_values(ascending=True))