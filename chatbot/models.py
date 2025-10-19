# chatbot/models.py
from django.db import models

class ChatbotQuery(models.Model):
    CATEGORY_CHOICES = [
        ('GREETING', 'Greeting'),           # For hello, hi, etc.
        ('META', 'About Bot'),              # For "who made you?", etc.
        ('ERP', 'ERP Question'),            # For general ERP questions
        ('PAGE_HELP', 'Page Specific Help'),# For questions about a specific page
    ]

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='ERP')
    page_identifier = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., '/about', '/login'")

    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords, e.g., 'fees,cost,admission fee'")

    answer_en = models.TextField()
    answer_hi = models.TextField(blank=True)
    answer_hinglish = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category} - {self.keywords}"