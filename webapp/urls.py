"""
URL configuration for webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chatbot.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_action, name="login"),
    path("register/", register_action, name="register"),
    path("chat/", chat, name="chat"),
    path("chat/send/", send_chat_message, name="chat_send_message"),
    path("logout/", logout_action, name="logout"),
    path("chat/stream_ai/", stream_ai_response, name="stream_ai"),
    path("profile/", profile, name="profile"),
]
