from django.utils import timezone
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from chatbot.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from chatbot.models import *
from django.http import StreamingHttpResponse
import time
import random
from google import genai
from dotenv import load_dotenv
import os

from chatbot.utils.prompt import generate_prompt

# Create your views here.
def login_action(request):
    # display the login page if the request method is GET
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('chat')
        form = LoginForm()
        context = {
            "form": form
            }
        return render(request, "chatbot/login.html", context)
    # login
    form = LoginForm(request.POST)
    if not form.is_valid():
        context = {
            "form": form
            }
        return render(request, "chatbot/login.html", context)
    # form validated, login the user
    new_user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
    login(request, new_user)
    return redirect('chat')
    
def register_action(request):
    # display the registration page if the request method is GET
    if request.method == "GET":
        form = RegisterForm()
        context = {
            "form": form
            }
        return render(request, "chatbot/register.html", context)
    
    # registration
    form = RegisterForm(request.POST)
    if not form.is_valid():
        context = {
            "form": form
            }
        return render(request, "chatbot/register.html", context)
    # form validated, register and login the user
    new_user = User.objects.create_user(username=form.cleaned_data["username"], 
                                        password=form.cleaned_data["password"])
    new_user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
    login(request, new_user)
    return redirect('chat')

def logout_action(request):
    logout(request)
    return redirect('login')


def chat(request):
    conversation, created = Conversation.objects.get_or_create(user=request.user)
    messages = conversation.messages.all().order_by("timestamp")
    form = ChatMessageForm()

    return render(request, "chatbot/chat.html", {"chat_form": form, "messages": messages})



@login_required
def send_chat_message(request):
    if request.method == "POST":
        user_input = request.POST.get("text", "").strip()
        if not user_input:
            return JsonResponse({"error": "Empty message"}, status=400)

        conversation, _ = Conversation.objects.get_or_create(user=request.user)

        # Save user message
        new_message = Message.objects.create(conversation=conversation, author=request.user.username, text=user_input)

        return JsonResponse({
            "success": True,
            "message": {
                "author": request.user.username,  # Ensure "user" is correctly set here
                "text": user_input,
                "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        })

    return JsonResponse({"error": "Invalid request"}, status=400)



def generate_ai_response_mock():
    responses = [
        "I understand. Sometimes taking a break helps.",
        "It’s okay to feel that way. Remember to breathe.",
        "Talking to a friend or journaling might help you process these emotions."
    ]
    response_text = random.choice(responses)  # Select a random mock response

    for word in response_text.split():
        # yield word + " "  # Stream one word at a time
        yield f"data: {word} \n\n"
        time.sleep(0.3)  # Simulate AI "thinking"


def generate_ai_response(request, user_input, revised_prompt):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    accumulated_text = ""
    
    try:
        response = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=[revised_prompt])
        for chunk in response:
            encoded_data = json.dumps({"text": chunk.text})  # Encode to JSON
            yield f"data: {encoded_data}\n\n"  # Send JSON string
            # print("Chunk: ", chunk.text)
            accumulated_text += chunk.text
    except Exception as e:
        error_message = "AI response failed， please try again later."
        print("Error: ", e)
        encoded_data = json.dumps({"text": error_message})
        yield f"data: {encoded_data}\n\n"
        
        conversation = Conversation.objects.get(user=request.user)
        Message.objects.create(conversation=conversation, author="AI", text=error_message)
        return
    
    conversation = Conversation.objects.get(user=request.user)
    Message.objects.create(conversation=conversation, author="AI", text=accumulated_text)
    
    new_round = {"user_input": user_input, "ai_response": accumulated_text}
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.last_chat_history.append(new_round)
    profile.save()
    
        
        

@login_required
def stream_ai_response(request):
    user_input = request.GET.get("text", "")  # Get user input from request
    if not user_input:
        return JsonResponse({"error": "No user input provided"}, status=400)
    revised_prompt = generate_prompt(request.user, user_input)
    print("Revised prompt: ", revised_prompt)
    return StreamingHttpResponse(generate_ai_response(request, user_input, revised_prompt), content_type="text/event-stream")

@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    return render(request, "chatbot/profile.html", {"form": form})
