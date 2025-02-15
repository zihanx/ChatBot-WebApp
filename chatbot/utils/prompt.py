from jinja2 import Environment, FileSystemLoader
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
# print(TEMPLATE_DIR)

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)

# Load the XML template
template = env.get_template("chatbot/prompt_template.xml")
# print(template.render(latest_user_prompt="Hello, AI!", name="Alex", mood="Happy", preferences="No preferences", conversation_summary="", chat_history=[]))
# def generate_prompt