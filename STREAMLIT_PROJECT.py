import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# === Google Sheets Setup ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "sodium-ray-466807-i9-4859b198bce0.json", scope
)
client = gspread.authorize(creds)

# === Load Google Sheet ===
SHEET_NAME = "report"
TAB_NAME = "ALL NEW"

try:
    worksheet = client.open(SHEET_NAME).worksheet(TAB_NAME)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error("❌ Failed to load Google Sheet. Check sheet name, tab name, or JSON credentials.")
    st.exception(e)
    st.stop()

# === Streamlit App Layout ===
st.set_page_config(page_title="Device Report Search", layout="wide")
st.title("📋 Device Report Search (ALL NEW Tab)")

tab1, tab2 = st.tabs(["🔎 Search Report", "🛠️ Other Features"])

with tab1:
    st.subheader("Search by Device Code")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        letter = st.selectbox("Select Code Prefix", ["M", "C", "P"])

    with col2:
        number = st.text_input("Enter Code Number", placeholder="e.g. 100")

    with col3:
        search = st.button("🔍 Search")

    if search:
        if letter and number:
            search_code = f"{letter.upper()}{number.strip()}"
            st.markdown(f"Searching for **{search_code}** in column B of '{TAB_NAME}' tab...")

            # === Search in Column B (index 1, assuming column B is second column) ===
            try:
                match_df = df[df[df.columns[1]].astype(str).str.upper() == search_code.upper()]

                if not match_df.empty:
                    st.success(f"✅ Found {len(match_df)} matching item(s).")
                    st.dataframe(match_df, use_container_width=True)
                else:
                    st.warning("❌ No matching device found.")
            except Exception as search_error:
                st.error("Error during search.")
                st.exception(search_error)
        else:
            st.error("⚠️ Please select a letter and enter a number.")

with tab2:
    st.info("More features will be added soon.")
