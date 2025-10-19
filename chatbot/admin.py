# chatbot/admin.py

from django.contrib import admin
from .models import ChatbotQuery # <-- Apne model ko import karo

# Is line se aapka model admin panel par dikhne lagega
admin.site.register(ChatbotQuery)