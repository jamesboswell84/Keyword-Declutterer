import pandas as pd
import re
import streamlit as st

### The following is used to store the dataframes between reruns
if 'df' not in st.session_state:
	st.session_state.df = None
if 'df4' not in st.session_state:
	st.session_state.df4 = None
if 'df5' not in st.session_state:
	st.session_state.df5 = None
if 'df6' not in st.session_state:
	st.session_state.df6 = None
if 'df9' not in st.session_state:
	st.session_state.df9 = None
if 'df10' not in st.session_state:
	st.session_state.df10 = None
if "alwaysshow" not in st.session_state:
        st.session_state.alwaysshow = False	
if 'files_xlsx' not in st.session_state:
	st.session_state.files_xlsx = None
	
st.write("""
	# 🧹 Keyword Declutterer
	#### Merge and declutter your competitor keyword lists, removing >90% of the brand, irrelevant and nonsense keywords.
""")
st.write("""
	##### Simple 3-step setup:
	1. Choose at least 3 of your client's top competitors per product (this tool filters off any keywords if less than 3 competitors are on page 1 for it - removing irrelevant and brand in the process)*
	2. Go to SEMRush and download keyword lists for each of your chosen competitors (they must be the same xlsx format and filename as you downloaded them from SEMRush - if not this will stop the tool from working)
	3. Upload your files below and click the start button
""")

### Upload your Excel files
files_xlsx = st.file_uploader("", accept_multiple_files=True, type=['xlsx'])
st.session_state.files_xlsx = files_xlsx

### Read files and create single dataframe
		
if st.button('Start merge & declutter'):
	st.session_state.alwaysshow = True
	if len(files_xlsx) > 2:
		df = pd.DataFrame()
		with st.spinner("Merging files & decluttering..."):
			progbar = st.progress(0)
			counter = 0
			for f in range(len(files_xlsx)):
				progbar.progress(counter/len(files_xlsx))
				counter = counter + 1
				data = pd.read_excel(files_xlsx[f], 'Sheet 1')
				sitename = re.findall(r"(.*)\-organic\.Positions",files_xlsx[f].name)
				data["Site"] = sitename * len(data)
				df = df.append(data)

			### filter down keyword list 
			df2 = df.groupby(['Keyword','Site']).size().reset_index(name='Count')
			df2 = df2[df2.Count < 2]
			df2 = df2.merge(df,how="inner",on=["Keyword","Site"])
			df2 = df2[df2.Traffic > 9]
			df3 = pd.pivot_table(df2, values="Site", index="Keyword", aggfunc=pd.Series.nunique)
			df3 = df3[df3.Site > 3].reset_index()
			df3 = df3.rename({"Keyword": "Keyword", "Site": "Site Count"}, axis='columns')
			df4 = df2[df2["Keyword"].isin(df3.Keyword)]
			df4 = df4.drop(['Count'], axis=1)	

			### pivot the data for a very quick SEMRush data look at estimated clicks by site
			df5 = pd.pivot_table(df4, values="Traffic", index="Site", aggfunc=sum).sort_values(by=['Traffic'], ascending=False)		
			df6 = pd.pivot_table(df4, values="Traffic Cost", index="Site", aggfunc=sum).sort_values(by=['Traffic Cost'], ascending=False)		

			### pivot the data for a very quick SEMRush data look at estimated clicks by sub-folder
			df7 = df4
			df7 = df7["URL"].str.split('/', expand=True)
			df7 = df7.iloc[: , 3:].reset_index()
			df7 = df7.set_index("index").stack().reset_index(level=1, drop=True).to_frame("Sub").reset_index()
			df8 = df4.reset_index()
			df7 = df7.merge(df8,how="inner",on=["index"])
			df7["Sub"] = df7["Sub"].replace(r'^s*$', float('NaN'), regex = True)
			df7.dropna(inplace = True)
			df7["Subfolder/Page"] = df7["Sub"]
			df9 = pd.pivot_table(df7, values="Traffic", index="Subfolder/Page", aggfunc=sum).sort_values(by=['Traffic'], ascending=False)
			df10 = pd.pivot_table(df7, values="Traffic Cost", index="Subfolder/Page", aggfunc=sum).sort_values(by=['Traffic Cost'], ascending=False)
		st.session_state.df = df
		st.session_state.df4 = df4
		st.session_state.df5 = df5			
		st.session_state.df6 = df6			
		st.session_state.df9 = df9
		st.session_state.df10 = df10		
	else:
		st.write("""
				Not enough files.
		""")
	### if button has been pushed to session state do the following
	if st.session_state.alwaysshow:
		### show and allow download of cluttered unedited file
		try:
			st.write("""
				#### Merged keyword list (cluttered):
			""")
			st.dataframe(df[:100]) 
			### The following allows downloading to csv file

			def convert_df(df):
			# IMPORTANT: Cache the conversion to prevent computation on every rerun
				return df.to_csv().encode('utf-8')
			csv = convert_df(df)
			st.download_button('Download merged file (unedited)', csv, file_name="merged_file.csv",mime='text/csv')
		except TypeError:
			pass
		except AttributeError:
			pass
		except NameError:
			pass

		### show and allow download of decluttered edited file
		try:
			st.write("""
				#### Decluttered keyword list:
			""")
			st.dataframe(df4[:100]) 
				### The following allows downloading to csv file
			def convert_df(df4):
			# IMPORTANT: Cache the conversion to prevent computation on every rerun
				return df4.to_csv().encode('utf-8')
			csv = convert_df(df4)
			st.download_button('Download decluttered file (edited)', csv, file_name="decluttered_file.csv",mime='text/csv')
		except TypeError:
			pass
		except AttributeError:
			pass	
		except NameError:
			pass

		### show data tables and visualisations
		nametab1 = "Sites by traffic"
		nametab2 = "Sites by traffic value ($CPC * traffic)"
		nametab3 = "Subfolder/page by traffic"
		nametab4 = "Subfolder/page by traffic value ($CPC * traffic)"
		nametab5 = "$CPC versus difficulty"
		tab1, tab2, tab3, tab4, tab5 = st.tabs([nametab1, nametab2, nametab3, nametab4,nametab5])

		with tab1:
			try:
				st.write("""
					#### Sites by traffic:
				""")
				st.dataframe(df5[:100])		
			except TypeError:
				pass
			except AttributeError:
				pass	
		with tab2:
			try:
				st.write("""
					#### Sites by traffic value ($CPC * traffic):
				""")
				st.dataframe(df6[:100])
			except TypeError:
				pass
			except AttributeError:
				pass	
		with tab3:
			try:
				st.write("""
					#### Subfolder/page by traffic:
				""")
				st.dataframe(df9[:100])
			except TypeError:
				pass
			except AttributeError:
				pass	
		with tab4:
			try:
				st.write("""
					#### Subfolder/page by traffic value ($CPC * traffic):
				""")
				st.dataframe(df10[:100])
			except TypeError:
				pass
			except AttributeError:
				pass
		with tab5:
			try:
				st.write("""
					#### Subfolder/page by traffic value ($CPC * traffic):
				""")				
			except TypeError:
				pass
			except AttributeError:
				pass

