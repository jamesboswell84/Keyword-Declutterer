import pandas as pd
import os
import re

st.write("""
# 🧹 Keyword Declutterer
Merge and declutter your competitor keyword lists, removing 99% of the brand, irrelevant and nonsense keywords.
""")

st.write("""
Simple two-step setup:
1. Choose at least 3 of your client's top competitors per product (this tool filters off any keywords if less than 3 competitors are on page 1 for it - removing irrelevant and brand in the process)*
2. Go to SEMRush and download keyword lists for each of your chosen competitors (just into the Downloads folder is fine - you only need them temporarily. They must be exactly the same as you downloaded them from SEMRush (including filenames) - if not this will stop the tool from working)
""")
### Upload your Excel files



### merge into single dataframe with a single top row and a new column for site name
path = r'C:\Users\44754\Documents\Python Scripts\Keywordle\banks keywords'
files = os.listdir(path)
files_xlsx = [f for f in files if '.xlsx' in f]
df = pd.DataFrame()
for f in files_xlsx:
    data = pd.read_excel(path+r"\\"+f, 'Sheet 1')
    sitename = re.findall(r"(.*)\-organic\.Positions",f)
    data["Site"] = sitename * len(data)
    df = df.append(data)



#%%
### filter down keyword list - only keep keywords with >2 comp on Google page 1

df2 = df.groupby(['Keyword','Site']).size().reset_index(name='Count')
df2 = df2[df2.Count < 2]
df2 = df2.merge(df,how="inner",on=["Keyword","Site"])
df2 = df2[df2.Traffic > 9]
df3 = pd.pivot_table(df2, values="Site", index="Keyword", aggfunc=pd.Series.nunique)
df3 = df3[df3.Site > 3].reset_index()
df3 = df3.rename({"Keyword": "Keyword", "Site": "Site Count"}, axis='columns')
df4 = df2[df2["Keyword"].isin(df3.Keyword)]

### allow the data to be downloaded - for categorising and uploading to STAT



#%%
### pivot the data for a very quick SEMRush data look at estimated clicks by site

df5 = pd.pivot_table(df4, values="Traffic", index="Site", aggfunc=sum).sort_values(by=['Traffic'], ascending=False)
df6 = pd.pivot_table(df4, values="Traffic Cost", index="Site", aggfunc=sum).sort_values(by=['Traffic Cost'], ascending=False)

#%%
### pivot the data for a very quick SEMRush data look at estimated clicks by sub-folder

df7 = df4
df7 = df7["URL"].str.split('/', expand=True)
df7 = df7.iloc[: , 3:].reset_index()
df7 = df7.set_index("index").stack().reset_index(level=1, drop=True).to_frame("Sub").reset_index()
df8 = df4.reset_index()
df7 = df7.merge(df8,how="inner",on=["index"])
df7["Sub_x"] = df7["Sub_x"].replace(r'^s*$', float('NaN'), regex = True)
df7.dropna(inplace = True)
df7["Subfolder/Page"] = df7["Sub_x"]
df9 = pd.pivot_table(df7, values="Traffic", index="Subfolder/Page", aggfunc=sum).sort_values(by=['Traffic'], ascending=False)
df10 = pd.pivot_table(df7, values="Traffic Cost", index="Subfolder/Page", aggfunc=sum).sort_values(by=['Traffic Cost'], ascending=False)
