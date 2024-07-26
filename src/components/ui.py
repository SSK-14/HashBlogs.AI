import streamlit as st
import PyPDF2

def display_search_result(search_results):
    if search_results["images"]:
        with st.expander("Image Results", expanded=False):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.image(search_results["images"][0], use_column_width=True)
            col2.image(search_results["images"][1], use_column_width=True)
            col3.image(search_results["images"][2], use_column_width=True)
            col4.image(search_results["images"][3], use_column_width=True)
            col5.image(search_results["images"][4], use_column_width=True)

    with st.expander("Search Results", expanded=False):
        if search_results["results"]:
            for result in search_results["results"]:
                st.write(f"- [{result['title']}]({result['url']})")

def example_questions():
    col1, col2 = st.columns(2)
    questions = [
        "News on cricket T20 world cup 2024 final match",
        "Recent researches in the field of lung cancer"
    ]
    if col1.button(questions[0]):
        st.session_state.question = questions[0]
        st.rerun()
    if col2.button(questions[1]):
        st.session_state.question = questions[1]
        st.rerun()

@st.experimental_dialog("Upload your documents")
def upload_document():
    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")
    if uploaded_files:
        text = []
        for file in uploaded_files:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        st.session_state.search_context = text
        st.rerun()

@st.experimental_dialog("🔄 Re Generate Blog")
def regenerate_blog():
    st.write(f"Please provide what changes you want to make in the blog")
    feedback = st.text_input("Feedback...")
    if st.button("Submit"):
        st.session_state.blog_content_regenerate = feedback
        st.rerun()