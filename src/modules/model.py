import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAI

model_options = {
    "GPT-4o mini": "gpt-4o-mini",
    "GPT-4o": "gpt-4o",
    "GPT-4": "gpt-4",
}

def initialise_model():
    if "llm" not in st.session_state:
        st.session_state.llm = None
    if "OPENAI_API_TOKEN" in st.secrets:
        openai_api_token = st.secrets['OPENAI_API_TOKEN']
        st.session_state.openai_api_token = openai_api_token
    if "openai_api_token" not in st.session_state or not st.session_state.openai_api_token:
        st.warning('Please provide OpenAI API key in the sidebar.', icon="⚠️")
        st.stop()
    st.session_state.llm = ChatOpenAI(
        model=model_options[st.session_state.model_name] or "gpt-4o-mini",
        temperature=st.session_state.temperature or 0.1,
        max_tokens=st.session_state.max_tokens or 2500,
        api_key=st.session_state.openai_api_token
    )
    st.session_state.openai_client = OpenAI(api_key=st.session_state.openai_api_token)


async def llm_generate(prompt):
    result = st.session_state.llm.invoke(prompt).content
    return result

def llm_stream(prompt):
    st.session_state.blog_content = ""
    for chunk in st.session_state.llm.stream(prompt):
        st.session_state.blog_content += str(chunk.content)
        yield str(chunk.content)

def generate_image(prompt, n):
    response = st.session_state.openai_client.images.generate(
                model='dall-e-3',
                prompt=prompt,
                size='1792x1024',
                quality="standard",
                n=n
            )
    return response.data[0].url