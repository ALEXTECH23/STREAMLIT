{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPNt6auitv2ieXcDHwfDhjF"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "xzYIQVApHcv4",
        "outputId": "5d9eafe7-43eb-4613-def8-2ada1f9dcf02"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-1-2987175265.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      2\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mgspread\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0moauth2client\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mservice_account\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mServiceAccountCredentials\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mpandas\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mpd\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import gspread\n",
        "from oauth2client.service_account import ServiceAccountCredentials\n",
        "import pandas as pd\n",
        "\n",
        "# === Google Sheets Setup ===\n",
        "scope = [\"https://spreadsheets.google.com/feeds\", \"https://www.googleapis.com/auth/drive\"]\n",
        "creds = ServiceAccountCredentials.from_json_keyfile_name(\n",
        "    \"sodium-ray-466807-i9-4859b198bce0.json\", scope\n",
        ")\n",
        "client = gspread.authorize(creds)\n",
        "\n",
        "# === Load Google Sheet ===\n",
        "SHEET_NAME = \"report\"\n",
        "TAB_NAME = \"ALL NEW\"\n",
        "\n",
        "try:\n",
        "    worksheet = client.open(SHEET_NAME).worksheet(TAB_NAME)\n",
        "    data = worksheet.get_all_records()\n",
        "    df = pd.DataFrame(data)\n",
        "except Exception as e:\n",
        "    st.error(\"❌ Failed to load Google Sheet. Check sheet name, tab name, or JSON credentials.\")\n",
        "    st.exception(e)\n",
        "    st.stop()\n",
        "\n",
        "# === Streamlit App Layout ===\n",
        "st.set_page_config(page_title=\"Device Report Search\", layout=\"wide\")\n",
        "st.title(\"📋 Device Report Search (ALL NEW Tab)\")\n",
        "\n",
        "tab1, tab2 = st.tabs([\"🔎 Search Report\", \"🛠️ Other Features\"])\n",
        "\n",
        "with tab1:\n",
        "    st.subheader(\"Search by Device Code\")\n",
        "\n",
        "    col1, col2, col3 = st.columns([1, 2, 1])\n",
        "\n",
        "    with col1:\n",
        "        letter = st.selectbox(\"Select Code Prefix\", [\"M\", \"C\", \"P\"])\n",
        "\n",
        "    with col2:\n",
        "        number = st.text_input(\"Enter Code Number\", placeholder=\"e.g. 100\")\n",
        "\n",
        "    with col3:\n",
        "        search = st.button(\"🔍 Search\")\n",
        "\n",
        "    if search:\n",
        "        if letter and number:\n",
        "            search_code = f\"{letter.upper()}{number.strip()}\"\n",
        "            st.markdown(f\"Searching for **{search_code}** in column B of '{TAB_NAME}' tab...\")\n",
        "\n",
        "            # === Search in Column B (index 1, assuming column B is second column) ===\n",
        "            try:\n",
        "                match_df = df[df[df.columns[1]].astype(str).str.upper() == search_code.upper()]\n",
        "\n",
        "                if not match_df.empty:\n",
        "                    st.success(f\"✅ Found {len(match_df)} matching item(s).\")\n",
        "                    st.dataframe(match_df, use_container_width=True)\n",
        "                else:\n",
        "                    st.warning(\"❌ No matching device found.\")\n",
        "            except Exception as search_error:\n",
        "                st.error(\"Error during search.\")\n",
        "                st.exception(search_error)\n",
        "        else:\n",
        "            st.error(\"⚠️ Please select a letter and enter a number.\")\n",
        "\n",
        "with tab2:\n",
        "    st.info(\"More features will be added soon.\")\n"
      ]
    }
  ]
}