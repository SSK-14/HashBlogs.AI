from langchain_core.messages import HumanMessage, SystemMessage
import json, time

def search_query_prompt(user_query):
    current_date = time.strftime("%Y-%m-%d")
    return (
        SystemMessage(
            content=f"Role: Create search query based on user question to write a blog, todays date: {current_date}\n"
                    f"Task: Give a detailed search query which will be used to search internet to get information for writing the blog.\n"
                    f"Rule: Only return the query, Do not answer the question.\n"
        ),
        HumanMessage(
            content=f"User question: ```{user_query}``` .\n"
                    f"Search query: "
        )
    )

def search_blog_prompt(user_query, search_result):
    current_date = time.strftime("%Y-%m-%d")
    return (
        SystemMessage(
            content=f"Role: You are the best blogger in the world, todays date: {current_date}\n"
                    f"Task: Write a blog post based user question and search result\n"
                    f"Format: Write a blog post in markdown format including:\n"
                    f"1.Title:, 2.Subtitle, 3.tl:dr 4.Sections with appropriate names 5.conclusion, 6.reference\n"
        ),
        HumanMessage(
            content=f"User question: ```{user_query}``` .\n"
                    f"Search result: ```{json.dumps(search_result)}```\n\n"
                    f"Must be engaging, creative, include emojis.\n"
                    f"Blog in markdown: "
        )
    )