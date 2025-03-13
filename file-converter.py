import streamlit as st
import pandas as pd
from io import BytesIO

# Page Configuration
st.set_page_config(page_title="File Converter", page_icon="🔄", layout="wide")

# Animated Background CSS
st.markdown("""
    <style>
    /* Background Animation */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .animated-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fad0c4, #fbc2eb);
        background-size: 400% 400%;
        animation: gradientBG 10s ease infinite;
        z-index: -1;
    }

    /* Content Wrapper */
    .content {
        position: relative;
        z-index: 1;
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }

    .stButton>button {
        background-color: #4CAF50; /* Green */
        color: white;
        border-radius: 8px;
        padding: 8px 15px;
    }
    .stDownloadButton>button {
        background-color: #007BFF; /* Blue */
        color: white;
        border-radius: 8px;
        padding: 8px 15px;
    }
    </style>

    <div class="animated-background"></div>
""", unsafe_allow_html=True)

# Content Wrapper
st.markdown('<div class="content">', unsafe_allow_html=True)

# Header
st.title("🔄 File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats with ease! 🚀")

# Sidebar File Upload
st.sidebar.header("📂 Upload Files")
files = st.sidebar.file_uploader("Upload CSV or Excel files", type=["csv", "xlsx"], accept_multiple_files=True)

# Process each uploaded file
if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.markdown(f"### 📜 Preview: {file.name}")
        st.dataframe(df.head())

        # Create layout for better spacing
        col1, col2 = st.columns([1, 1])

        # Remove Duplicates Checkbox
        with col1:
            if st.checkbox(f"🗑 Remove Duplicates - {file.name}"):
                df = df.drop_duplicates()
                st.success("✅ Duplicates removed successfully!")
                st.dataframe(df.head())

        # Fill Missing Values Checkbox
        with col2:
            if st.checkbox(f"➕ Fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.success("✅ Missing values filled with mean!")
                st.dataframe(df.head())

        # Column Selection
        selected_columns = st.multiselect(f"🎯 Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show Chart Option
        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Convert File Format
        st.markdown(f"### 🔄 Convert `{file.name}` to:")
        format_choice = st.radio("", ["CSV", "Excel"], key=file.name, horizontal=True)

        # Download Button
        if st.button(f"📥 Download `{file.name}` as {format_choice}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("📩 Download File", file_name=new_name, data=output, mime=mime)
            st.success("🎉 Processing Complete! Your file is ready.")

st.sidebar.info("📌 Tip: You can upload multiple files at once!")

# Close content wrapper
st.markdown('</div>', unsafe_allow_html=True)
