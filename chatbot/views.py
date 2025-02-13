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

# Create your views here.
def login_action(request):
    # display the login page if the request method is GET
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('chat_page')
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
    """Handles storing user messages and getting AI responses."""
    if request.method == "POST":
        user_input = request.POST.get("text", "").strip()
        if not user_input:
            return JsonResponse({"error": "Empty message"}, status=400)

        conversation, _ = Conversation.objects.get_or_create(user=request.user)

        # Save user message
        new_message = Message.objects.create(conversation=conversation, author=request.user.username, text=user_input)

        # # Get AI response
        # chatbot = Chatbot()  
        # ai_response = chatbot.generate_response(user_input)

        # Save AI message
        # Message.objects.create(conversation=conversation, sender="ai", text=ai_response)

        return JsonResponse({
            "success": True,
            "message": {
                "author": request.user.username,  # Ensure "user" is correctly set here
                "text": user_input,
                "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
