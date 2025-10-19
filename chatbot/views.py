# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatbotQuery
from .serializers import ChatbotQuerySerializer

class ChatbotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_query = request.data.get('query', '').lower()
        page = request.data.get('page', None) # Get the current page from the frontend

        # First, try to find a specific answer for the current page
        if page:
            page_queries = ChatbotQuery.objects.filter(category='PAGE_HELP', page_identifier=page)
            for query_obj in page_queries:
                keywords = [kw.strip().lower() for kw in query_obj.keywords.split(',')]
                if any(keyword in user_query for keyword in keywords):
                    serializer = ChatbotQuerySerializer(query_obj)
                    return Response(serializer.data)

        # If no page-specific answer, search general keywords
        general_queries = ChatbotQuery.objects.exclude(category='PAGE_HELP')
        for query_obj in general_queries:
            keywords = [kw.strip().lower() for kw in query_obj.keywords.split(',')]
            if any(keyword in user_query for keyword in keywords):
                serializer = ChatbotQuerySerializer(query_obj)
                return Response(serializer.data)

        # If nothing is found, send a default response
        default_response = {
            "answer_en": "I'm sorry, I don't have an answer for that. Please try another question.",
            "answer_hi": "मुझे क्षमा करें, मेरे पास इसका उत्तर नहीं है। कृपया कोई दूसरा प्रश्न पूछें।",
            "answer_hinglish": "Sorry, iska jawab mere paas nahi hai. Please kuch aur pucho."
        }
        return Response(default_response)