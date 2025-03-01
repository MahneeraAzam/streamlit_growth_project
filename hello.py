import streamlit as st
import pandas as pd
import os
from io import BytesIO

# set up our App

st.set_page_config(page_title="✨Data sweeper",layout="wide")
st.title("✨ Data sweeper")
st.write("Transfrom your files between CSV and excel formats with built-in data cleaning and visualization")


uploaded_file = st.file_uploader("Upload you files (CSV or Excel file):",type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display info about the files
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/2024}")

        # show 5 rows of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Option for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button("Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed Successfully!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["numbers"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Filled Successfully!")

                #Choose specific columns to keep or Convert
            
        st.subheader("Select Columns to or Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        # Create some Visualizations
        st.subheader("💥 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Covert the file -> CSV to Excel
        st.subheader("💾 Conversation Options")
        Conversation_type = st.radio(f"Convert {file.name} to:",("CSV","Excel"), key=file.name)
        if st.button(f"Convert File"):
            buffer = BytesIO()
            if Conversation_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime = "text/csv"

            elif Conversation_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)


            #Download Button
            st.download_button(
                label=f"🎇 Download {file_name} as {Conversation_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 All files processed Successfully!")




    



            






































