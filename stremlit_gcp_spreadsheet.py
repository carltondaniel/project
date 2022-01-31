import streamlit as st
import pygsheets
import pandas as pd
st.set_page_config(page_title="Employee Details",layout="wide")

gc = pygsheets.authorize(service_file='/home/carlton/Downloads/creds.json')

# Create empty dataframe
update_df = pd.DataFrame()
df=pd.DataFrame()


def main():

	menu=["Enter Details","Search"]
	choice=st.sidebar.selectbox("Menu",menu)
	if choice=="Enter Details":
		st.subheader("Enter Details")
		with st.form(key='my_form1'):
			col1,col2=st.columns(2)
			dob=col1.date_input('Enter DOB')
			
			First_name = col1.text_input("First Name",)
			Last_name = col1.text_input("Last Name",)
			col1.write('Select Skill')
			option_1 = col1.checkbox('Java')
			option_2 = col1.checkbox('Shell script')
			option_3 = col1.checkbox('Python')
			option_4 = col1.checkbox('SQL')
			submit_button = st.form_submit_button(label='Submit')
			if submit_button:
				update_df['dob'] = [dob]
				update_df['First_name'] =[First_name.strip()]
				update_df['Last_name'] = [Last_name.strip()]
				update_df['Java'] = [option_1]
				update_df['Shell Script']=[option_2]
				update_df['Python'] = [option_3]
				update_df['SQL']=[option_4]
				sh = gc.open('prototype')
				wks = sh[0]
				df=wks.get_as_df()																	
				df=df.append(update_df)
				wks.set_dataframe(df,(1,1))
	elif choice =="Search":
		st.subheader("Search")
		with st.form(key='my_form2'):
			col1,col2=st.columns(2)
			First_name = col1.text_input("First Name",)
			Last_name = col1.text_input("Last Name",)
			submit_button = st.form_submit_button(label='Submit')
			if submit_button:
				sh = gc.open('prototype')
				wks = sh[0]
				df=wks.get_as_df()
				if (First_name !="" )and (Last_name!="") :
					filtered_df=df[(df['First_name'].str.strip()==(First_name.strip())) & (df['Last_name'].str.strip()==Last_name.strip())]
	
				if (Last_name) == "":

					filtered_df=df[(df['First_name'].str.strip()==(First_name.strip())) ]
				if (First_name) == "":
					filtered_df=df[(df['Last_name'].str.strip()==(Last_name.strip())) ]		
				st.write(filtered_df.reset_index(drop=True))





if __name__ =='__main__':
	main()