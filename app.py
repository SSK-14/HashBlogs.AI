import asyncio
import streamlit as st
from src.modules.model import initialise_model, llm_generate, llm_stream, generate_image
from src.modules.search import ai_search
from src.modules.prompt import search_query_prompt, search_blog_prompt, banner_image_prompt
from src.components.sidebar import side_info
from src.components.ui import example_questions, regenerate_blog, upload_document
from src.modules.search import initialise_tavily
from src.modules.utils import parse_content

if "blog_content" not in st.session_state:
    st.session_state.blog_content = None
if "blog_content_edit" not in st.session_state:
    st.session_state.blog_content_edit = False
if "blog_banner" not in st.session_state:
    st.session_state.blog_banner = None
if "blog_content_regenerate" not in st.session_state:
    st.session_state.blog_content_regenerate = None
if "question" not in st.session_state:
    st.session_state.question = None
if "search_context" not in st.session_state:
    st.session_state.search_context = None
if "search_images" not in st.session_state:
    st.session_state.search_images = None


async def main():
    st.title("#️⃣ AI.:blue[Playground]")
    st.info("###### 👋 Welcome to HashBlogs.ai ✨ A playground to generate blog content using AI companion 🚀")
    side_info()
    initialise_model()
    initialise_tavily()

    if st.session_state.blog_content is None:
        if not st.session_state.search_context:
            if st.button("📚 Add your notes"):
                upload_document()
        else:
            if st.button("🗑️ Remove your notes"):
                st.session_state.search_context = None

        question_input = st.text_area(
            "Enter your idea 👇",
            placeholder="Type here... Eg: How to make perfect coffee?",
        )
        if question_input:
            st.session_state.question = question_input
        example_questions()

    if st.session_state.question and st.session_state.blog_content is None:
        if not st.session_state.search_context:
            with st.spinner("AI is working. Please wait."):
                search_query = await llm_generate(search_query_prompt(st.session_state.question))
                search_results = ai_search(search_query)
            if search_results["results"]:
                search_context = []
                for result in search_results["results"]:
                    search_context.append({
                        "title": result["title"],
                        "content": result["content"],
                        "url": result["url"],
                    })
                st.session_state.search_context = search_context
                st.session_state.search_images = search_results["images"]
                st.rerun()
            else:
                st.warning("No results found! 😔")
        else:
            with st.container(height=710, border=True):
                with st.container(height=620, border=False):
                    if st.session_state.blog_content is None:
                        st.write_stream(llm_stream(search_blog_prompt(st.session_state.question, st.session_state.search_context, st.session_state.search_images)))
                        st.rerun()
        

    if st.session_state.blog_content_regenerate:
        with st.container(height=710, border=True):
            with st.container(height=620, border=False):
                st.write_stream(llm_stream(search_blog_prompt(st.session_state.question, st.session_state.search_context, st.session_state.search_images, st.session_state.blog_content, st.session_state.blog_content_regenerate)))
                st.session_state.blog_content_regenerate = None
                st.rerun()

    if st.session_state.blog_content:
        title, tldr = parse_content(st.session_state.blog_content)
        with st.container(height=710, border=True):
            if st.session_state.blog_content_edit:
                new_blog_content = st.text_area("Blog content", height=590, value=st.session_state.blog_content, label_visibility="hidden")
            else:
                with st.container(height=620, border=False):
                    if st.button(f"🎨 {'Re Generate' if st.session_state.blog_banner else 'Generate'} Banner"):
                        st.session_state.blog_banner = generate_image(banner_image_prompt(title, tldr), 1)
                        st.rerun()
                    if st.session_state.blog_banner:
                        st.image(st.session_state.blog_banner, use_column_width=True)
                    st.markdown(st.session_state.blog_content)
                
            col1, col2, col = st.columns([3, 3, 6])
            if col1.button(f"📝 {'Save' if st.session_state.blog_content_edit else 'Edit'}", use_container_width=True):
                if st.session_state.blog_content_edit:
                    st.session_state.blog_content = new_blog_content
                    st.session_state.blog_content_edit = False
                    st.rerun()
                else:
                    st.session_state.blog_content_edit = True
                    st.rerun()
            if col2.button("🔄 Re Generate", use_container_width=True, type="primary"):
                regenerate_blog()


if __name__ == "__main__":
    st.set_page_config(page_title="HashBlogs.ai", page_icon="✨")
    asyncio.run(main())