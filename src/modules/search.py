import streamlit as st
from tavily import TavilyClient

def initialise_tavily():
    if "TAVILY_API_KEY" in st.secrets:
        tavily_api_key = st.secrets["TAVILY_API_KEY"]
    
    if "tavily_api_key" in st.session_state and st.session_state.tavily_api_key:
        tavily_api_key = st.session_state.tavily_api_key
    else:
        st.warning('Please provide Tavily API key in the sidebar.', icon="⚠️")
        st.stop()

    st.session_state.tavily_client = TavilyClient(api_key=tavily_api_key)


def ai_search(query):
    return st.session_state.tavily_client.search(query, search_depth="advanced", include_images=True)