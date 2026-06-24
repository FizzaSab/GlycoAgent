import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Glycosylation Research Agent", page_icon="🧪", layout="wide")
st.title("🧪 Glycosylation Research Agent")

@st.cache_data
def load_data():
    excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
    if excel_files:
        try:
            return pd.read_excel(excel_files[0], sheet_name='All Papers')
        except:
            return pd.DataFrame()
    return pd.DataFrame()

papers = load_data()

if len(papers) == 0:
    st.warning("Upload your Excel file")
    uploaded = st.file_uploader("Choose Excel file", type=['xlsx'])
    if uploaded:
        papers = pd.read_excel(uploaded, sheet_name='All Papers')
        st.rerun()
else:
    st.success(f"Loaded {len(papers)} papers")
    
    keyword = st.text_input("Search papers", placeholder="e.g. NIS, sialic acid")
    if keyword:
        mask = papers['Title'].str.contains(keyword, case=False, na=False)
        results = papers[mask]
        st.write(f"Found {len(results)} papers")
        for _, row in results.head(20).iterrows():
            with st.expander(f"[{row.get('Year', '?')}] {row.get('Title', '')[:80]}..."):
                st.write(f"**Journal:** {row.get('Journal', '?')}")
                st.write(f"**Topic:** {row.get('Topic', '?')}")
                st.write(f"**Abstract:** {str(row.get('Abstract', ''))[:500]}...")
