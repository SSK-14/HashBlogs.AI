import streamlit as st
from src.modules.model import model_options

def side_info():
    with st.sidebar:
        st.image("src/assets/logo.png")
        card_html = """
        <div style="background-color: #00305d; border: 2px solid #60b4ff; border-radius: 10px; padding: 0px 8px; width: 100%; box-sizing: border-box; color: white;  font-family: 'Arial', sans-serif; font-size: 15px; color: #FAFAFA; line-height: 1.3;">
            <p>HashBlogs.AI is your super-smart AI assistant for blogging! Just specify your preferences, and watch as it crawls live information 🌐, formats your content 📝, and adds engaging images 🖼️ like magic! ✨</p>
        </div>
        """
        st.components.v1.html(card_html, height=200, scrolling=False)
        if "OPENAI_API_TOKEN" not in st.secrets:
            st.text_input(
                "Openai API Key",
                type="password",
                placeholder="Paste your api key here",
                help="You can get your API key from https://platform.openai.com/account/api-keys",
                key="model_api_key"
            )

        if "TAVILY_API_KEY" not in st.secrets:
            st.text_input(
                "Tavily API Key",
                type="password",
                placeholder="Paste your tavily key here",
                help="You can get your API key from https://app.tavily.com/home",
                key="tavily_api_key"
            )

        st.sidebar.selectbox("Select a model", list(model_options.keys()), key="model_name")
        with st.popover("More settings", use_container_width=True):
            st.slider(
                "Temperature", min_value=0.0, max_value=2.0, step=0.1, value=0.1, key="temperature"
            )
            st.slider(
                "Max Tokens", min_value=0, max_value=8000, value=2500, key="max_tokens"
            )

        st.markdown("---")
        st.link_button("🔗 Source Code", "https://github.com/SSK-14/HashBlogs.AI", use_container_width=True)