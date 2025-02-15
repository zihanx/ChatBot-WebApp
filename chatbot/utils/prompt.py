from jinja2 import Environment, FileSystemLoader
import os
from chatbot.models import Conversation, Message, Profile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)

# Load the XML template
template = env.get_template("chatbot/prompt_template.xml")


def generate_prompt(user):
    """Generates the XML-formatted prompt for the LLM based on user context and chat history."""
    
    # Fetch user profile
    try:
        profile = Profile.objects.get(user=user)
        user_context = {
            "name": profile.name or "User",
            "mood": profile.current_mood_level,
            "preferences": profile.interests or "Not specified",
            "conversation_summary": profile.conversation_summary or "",
        }
    except Profile.DoesNotExist:
        user_context = {
            "name": "User",
            "mood": "Neutral",
            "preferences": "Not specified",
            "conversation_summary": "",
        }

    # Fetch the latest conversation for the user
    try:
        conversation = Conversation.objects.get(user=user)
        messages = Message.objects.filter(conversation=conversation).order_by("timestamp")
    except Conversation.DoesNotExist:
        messages = []

    # Extract the last user message
    latest_user_prompt = ""
    chat_history = []

    for message in messages:
        chat_history.append({"role": message.author, "content": message.text})
        if message.author != "AI":
            latest_user_prompt = message.text

    # Render the template
    prompt_xml = template.render(
        latest_user_prompt=latest_user_prompt,
        name=user_context["name"],
        mood=user_context["mood"],
        preferences=user_context["preferences"],
        conversation_summary=user_context["conversation_summary"],
        chat_history=chat_history
    )

    return prompt_xml
