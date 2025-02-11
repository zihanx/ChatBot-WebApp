import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from chatbot.forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

chat_messages = []

def chat(request):
    global chat_messages
    # if request.method == "POST":
    #     form = ChatMessageForm(request.POST)
    #     if form.is_valid():
    #         user_message = {
    #             "author": request.user.username,
    #             "text": form.clean_text(),
    #             "timestamp": now(),
    #         }
    #         chat_messages.append(user_message)
    #         print(chat_messages)
    #         # Mock AI response
    #         ai_response = {
    #             "author": "Chat Bot",
    #             "text": "I'm just a bot, but I'm here to chat!",
    #             "timestamp": now(),
    #         }
    #         chat_messages.append(ai_response)

    #         return redirect("chat")  # Reload chat page

    # else:
    form = ChatMessageForm()

    return render(request, "chatbot/chat.html", {"chat_form": form, "messages": chat_messages})



def send_chat_message(request):
    """ Handles chat message submission via form POST """
    if request.method == "POST":
        text = request.POST.get("text", "").strip()  # Get form data safely

        if not text:
            return JsonResponse({"success": False, "error": "Message cannot be empty"}, status=400)

        new_message = {
            "author": request.user.username,
            "text": text,
            "timestamp": now().strftime("%I:%M %p"),
        }
        chat_messages.append(new_message)

        # Mock AI response
        ai_response = {
            "author": "Chat Bot",
            "text": "I'm just a bot, but I'm here to chat!",
            "timestamp": now().strftime("%I:%M %p"),
        }
        chat_messages.append(ai_response)

        return JsonResponse({"success": True, "message": new_message})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
