import re

def parse_content(blog_content):
    title_match = re.search(r"^# (.+)$", blog_content, re.MULTILINE)
    title = title_match.group(1) if title_match else None
    tldr_match = re.search(r"### tl;dr\s+(.*?)\s+(?=##|$)", blog_content, re.DOTALL)
    tldr = tldr_match.group(1).strip() if tldr_match else None
    return title, tldr