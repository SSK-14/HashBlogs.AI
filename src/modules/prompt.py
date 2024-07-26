from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
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

def banner_image_prompt(title, tldr):
    prompt = f"You have to create a banner image for the blog post with title {title}. The image should be engaging, creative."
    f"Here is the short summary of the blog post: {tldr}"
    f"Create a banner image with the right alignment with the title and summary."
    f"Dont not include any text in the image."
    return prompt

def search_blog_prompt(user_query, search_result, images, blog_content=None, feedback=None):
    current_date = time.strftime("%Y-%m-%d")
    prompt = (
        SystemMessage(
            content=f"Role: You are the best blogger in the world, todays date: {current_date}\n"
                    f"Task: Write a blog post based user question and search result\n"
                    f"Format: Write a blog post in markdown format including:\n"
                    f"1.Title:, 2.Subtitle, 3.tl:dr 4.Introduction 6.Body with appropriate sections 7.conclusion, 8.reference\n"
        ),
        HumanMessage(
             content=[
                {
                    "type": "text", 
                    "text": f"User question: ```{user_query}``` .\n"
                            f"Search result: ```{json.dumps(search_result)}```\n\n"
                            f"Images: {json.dumps(images)}\n\n"
                            f"Add only necessary images in the blog only if needed.\n"
                            f"Must be engaging, creative, include emojis.\n"
                            f"Blog in markdown: "
                },
                {"type": "image_url", "image_url": {"url": images[0]}},
                {"type": "image_url", "image_url": {"url": images[1]}},
                {"type": "image_url", "image_url": {"url": images[2]}},
                {"type": "image_url", "image_url": {"url": images[3]}},
            ],
        )
    )
    if blog_content and feedback:
        new_prompt = (
            AIMessage(
                content=blog_content
            ),
            HumanMessage(
                content=f"User Feedback: {feedback}"
                f"Refactored Blog in markdown: "
            )
        )
        prompt += new_prompt
    return prompt