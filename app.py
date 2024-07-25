import asyncio
import streamlit as st
from src.modules.model import initialise_model, llm_generate, llm_stream
from src.modules.search import ai_search
from src.modules.prompt import search_query_prompt, search_blog_prompt
from src.components.sidebar import side_info
from src.components.ui import display_search_result
from src.modules.search import initialise_tavily

if "blog_content" not in st.session_state:
    st.session_state.blog_content = None

async def main():
    st.title("#️⃣ HashBlogs.:blue[AI]")
    side_info()
    initialise_model()
    initialise_tavily()
    text_input = st.text_input(
        "Enter your idea 👇",
        placeholder="Type here... Eg: How to make perfect coffee?",
    )
    if text_input:
        search_query = await llm_generate(search_query_prompt(text_input))
        search_results = ai_search(search_query)
        if search_results["results"]:
            display_search_result(search_results)
            search_context = []
            for result in search_results["results"]:
                search_context.append({
                    "title": result["title"],
                    "content": result["content"],
                    "url": result["url"],
                })
            with st.container(height=600, border=True):
                st.write_stream(llm_stream(search_blog_prompt(text_input, search_context)))
            
        else:
            st.warning("No results found! 😔")


if __name__ == "__main__":
    st.set_page_config(page_title="HashBlogs.AI", page_icon="✨")
    asyncio.run(main())