import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for professional styling
st.markdown(
    """
    <style>
    /* Background and text styling */
    .stApp {
        background-color: #0d1b2a; /* Dark navy blue */
        color: #e0e1dd; /* Light grayish-white */
        font-family: 'Poppins', sans-serif;
    }

    /* Title Styling */
    h1 {
        color: #f4a261; /* Warm orange */
        text-align: center;
    }

    /* Description text */
    .stMarkdown {
        color: #e9c46a; /* Soft yellow */
        font-size: 18px;
    }

    /* File uploader */
    .stFileUploader {
        background-color: #1b263b; /* Darker blue */
        border: 2px solid #e9c46a; /* Yellow border */
        border-radius: 10px;
        padding: 10px;
    }

    /* Buttons */
    .stButton>button {
        background-color: #f4a261; /* Orange */
        color: black;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #e76f51; /* Red-orange hover */
        color: white;
    }

    /* Dataframe table */
    .dataframe {
        background-color: #1b263b;
        color: #e0e1dd;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.title("Saad's Data Sweeper: Smart Data Cleaning & Conversion")
st.write("Effortlessly clean, process, and convert your CSV/Excel files in just a few clicks!")

# File uploader
uploaded_files = st.file_uploader(
    "📂 Upload your file (Accepts CSV or Excel)", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # File details
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑 Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✔ Duplicates removed!")

            with col2:
                if st.button(f"📌 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✔ Missing values have been filled!")

        # Select columns to keep
        st.subheader("📌 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📊 Data Visualization")
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.shape[1] > 2:
            if st.checkbox(f"📈 Show Visualization for {file.name}"):
                st.bar_chart(numeric_df.iloc[:, 2])
        else:
            st.warning("⚠ Not enough numeric columns for visualization!")

        # Conversion Option
        st.subheader("🔄 Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("🎉 All files processed successfully!")
    