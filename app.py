import asyncio
import streamlit as st
from src.modules.model import initialise_model, llm_generate, llm_stream, generate_image
from src.modules.search import ai_search, initialise_tavily
from src.modules.prompt import search_query_prompt, search_blog_prompt, banner_image_prompt, audio_blog_prompt
from src.modules.utils import init_session_state, parse_content, copy_to_clipboard
from src.modules.speech import stt, tts
from src.components.ui import example_questions, regenerate_blog, upload_document
from src.components.sidebar import side_info
from streamlit_tags import st_tags

def handle_search_context():
    if st.session_state.blog_content is None and st.session_state.question is None:
        st.info("###### 👋 Welcome to HashBlogs.ai ✨ A playground to generate blog content using AI companion 🚀")
        if not st.session_state.search_context:
            if st.button("📚 Add your notes"):
                upload_document()
        else:
            if st.button("🗑️ Remove your notes"):
                st.session_state.search_context = None
        st_tags(
            label='Enter Instructions:',
            text='Press enter to add more instructions',
            value=['Include tl:dr', 'Add emojis', 'Include key points', 'Use images'],
            maxtags=20,
            key='blog_instructions'
        )
        question_input = st.text_area(
            "Enter your idea 👇",
            placeholder="Type here...Eg: How to make a perfect cup of coffee?",
            help="Provide add your question or idea to generate blog content",
        )
        if question_input:
            st.session_state.question = question_input
        example_questions()
        if voice_question_input := stt():
            st.session_state.question = voice_question_input

async def fetch_search_results():
    if st.session_state.question and st.session_state.blog_content is None and not st.session_state.search_context:
        with st.spinner("AI is working 🖨️. Please wait..."):
            search_query = await llm_generate(search_query_prompt(st.session_state.question))
            search_results = ai_search(search_query)
        if search_results["results"]:
            st.session_state.search_context = [
                {
                    "title": result["title"],
                    "content": result["content"],
                    "url": result["url"],
                }
                for result in search_results["results"]
            ]
            st.session_state.search_images = search_results["images"]
            st.rerun()
        else:
            st.warning("No results found! 😔")

def display_search_context():
    if (st.session_state.search_context and st.session_state.blog_content is None) or st.session_state.blog_content_regenerate:
        with st.container(height=710, border=True):
            with st.container(height=620, border=False):
                st.write_stream(
                    llm_stream(
                        search_blog_prompt(
                            st.session_state.question,
                            st.session_state.blog_instructions,
                            st.session_state.search_context,
                            st.session_state.search_images,
                            st.session_state.blog_content,
                            st.session_state.blog_content_regenerate,
                        )
                    )
                )
                if st.session_state.blog_content_regenerate:
                    st.session_state.blog_content_regenerate = None
                st.rerun()

async def display_blog_content():
    if st.session_state.blog_content:
        title, tldr = parse_content(st.session_state.blog_content)
        with st.container(height=710, border=True):
            if st.session_state.blog_content_edit:
                new_blog_content = st.text_area(
                    "Blog content", height=590, value=st.session_state.blog_content, label_visibility="hidden"
                )
            else:
                with st.container(height=620, border=False):
                    if st.button(f"🎨 {'Re Generate' if st.session_state.blog_banner else 'Generate'} Banner"):
                        st.session_state.blog_banner = generate_image(banner_image_prompt(title, tldr), 1)
                        st.rerun()
                    if st.session_state.blog_banner:
                        st.image(st.session_state.blog_banner, use_column_width=True)
                    st.markdown(st.session_state.blog_content)

            col1, col2, _, col3 = st.columns([3, 3, 3, 3])
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
            if col3.button("📋 Copy Blog", use_container_width=True):
                copy_to_clipboard(st.session_state.blog_content)

        if st.session_state.blog_audio:
            st.audio(st.session_state.blog_audio)
        else:
            if st.button("🔊 Listen to Blog"):
                with st.spinner("AI is cooking 🍱. Please wait..."):
                    audio_script = await llm_generate(audio_blog_prompt(st.session_state.blog_content))
                    st.session_state.blog_audio = tts(audio_script)
                st.rerun()
            

async def main():
    st.title("#️⃣ AI.:blue[Playground]")
    init_session_state()
    side_info()
    initialise_model()
    initialise_tavily()
    handle_search_context()
    await fetch_search_results()
    display_search_context()
    await display_blog_content()

if __name__ == "__main__":
    st.set_page_config(page_title="HashBlogs.ai", page_icon="✨")
    asyncio.run(main())
