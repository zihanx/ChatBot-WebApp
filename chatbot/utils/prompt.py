from jinja2 import Environment, FileSystemLoader
import os
from chatbot.models import Profile
import tiktoken
from google import genai

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)

# Load the XML template
template = env.get_template("chatbot/prompt_template.xml")

TOKEN_LIMIT = 8192
# TOKEN_LIMIT = 800


MOOD_LEVEL_MAP = {
    1: "Very Unpleasant",
    2: "Unpleasant",
    3: "A Bit Unpleasant",
    4: "Neutral",
    5: "A Bit Pleasant",
    6: "Pleasant",
    7: "Very Pleasant",
}

def count_tokens(text):
    """Counts tokens in a text using the Gemini tokenizer."""
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text))

def summarize_text(text):
    """Summarize the given text using Gemini API."""
    API_KEY = os.getenv("GEMINI_API_KEY")  # Load API key from .env
    client = genai.Client(api_key=API_KEY)
    
    summary_prompt = f"Summarize the following conversation while keeping key insights:\n\n{text}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=[summary_prompt])
    
    return response.text.strip()

def generate_prompt(user, latest_user_prompt):
    """Generates the XML-formatted prompt for the LLM based on user context and chat history."""

    # Fetch user profile
    try:
        profile = Profile.objects.get(user=user)
        mood_level_desc = MOOD_LEVEL_MAP.get(profile.current_mood_level, "Neutral")

        # Construct mood tags description
        mood_tags_list = profile.current_mood_tag
        # mood_tags_desc = (
        #     f"The user feels {', '.join(mood_tags_list)}."
        #     if mood_tags_list else "The user has not specified mood tags."
        # )

        user_context = {
            "name": profile.name or "User",
            "age": profile.age or "Unknown",
            "gender": profile.gender or "Not specified",
            "mood_level": f"{mood_level_desc} ({profile.current_mood_level}/7)",
            "mood_tags": mood_tags_list,
            "preferences": profile.interests or "Not specified",
            "conversation_summary": profile.conversation_summary or "",
            "chat_history": profile.last_chat_history or [],
            "latest_user_prompt": latest_user_prompt
        }
    except Profile.DoesNotExist:
        user_context = {
            "name": "User",
            "age": "Unknown",
            "gender": "Not specified",
            "mood_level": "Neutral (4/7)",
            "mood_tags": "The user has not specified mood tags.",
            "preferences": "Not specified",
            "conversation_summary": "",
            "chat_history": [],
            "latest_user_prompt": latest_user_prompt
        }

    # Render the initial prompt
    formatted_context = template.render(**user_context)

    # Check if the token count exceeds the limit
    while count_tokens(formatted_context) > TOKEN_LIMIT:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Token limit exceeded. Summarizing chat history...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        if len(user_context["chat_history"]) < 2:
            break  # No need to summarize if history is too short

        # Summarize the previous 50% of history
        half_idx = len(user_context["chat_history"]) // 2
        history_to_summarize = "\n".join(
            f"User: {r['user_input']}\nAI: {r['ai_response']}" for r in user_context["chat_history"][:half_idx]
        )
        summary = summarize_text(history_to_summarize)

        # Update conversation summary and retain the latest messages
        profile.conversation_summary = summary
        profile.last_chat_history = user_context["chat_history"][half_idx:]  # Update chat history
        profile.save()
        user_context["conversation_summary"] = summary

        # Re-render prompt with updated summary and history
        user_context["chat_history"] = profile.last_chat_history
        formatted_context = template.render(**user_context)
    
    return formatted_context
