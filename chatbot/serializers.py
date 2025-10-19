# chatbot/serializers.py
from rest_framework import serializers
from .models import ChatbotQuery

class ChatbotQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotQuery
        fields = ['answer_en', 'answer_hi', 'answer_hinglish']