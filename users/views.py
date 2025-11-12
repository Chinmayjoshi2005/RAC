# users/views.py
from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save() # Create user

        # --- Assign Group based on Role from Frontend ---
        role = self.request.data.get('role', 'student').lower() # Get role
        group_name = role.capitalize() # 'Student', 'Faculty', 'Parent'

        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            print(f"Warning: Group '{group_name}' not found. Assigning to 'Student'.")
            try: # Fallback to Student group
                student_group = Group.objects.get(name='Student')
                user.groups.add(student_group)
            except Group.DoesNotExist:
                print(f"Warning: Default group 'Student' not found.")
        # --- End Group Assignment ---

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        # Check username/password first
        if not serializer.is_valid():
             return Response({'error': 'Invalid Enrollment No. or Password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # --- ROLE VERIFICATION ---
        requested_role_from_frontend = request.data.get('role', 'student').lower()
        user_groups = user.groups.all()
        actual_role_in_db = 'student' # Default

        if user_groups.exists():
             group_name = user_groups.first().name.lower()
             if group_name in ['faculty', 'parent']:
                  actual_role_in_db = group_name

        # **CRITICAL CHECK:** Does frontend role match backend role?
        if requested_role_from_frontend != actual_role_in_db:
             return Response(
                 {'error': f'Login failed. Account is registered as {actual_role_in_db.capitalize()}, not {requested_role_from_frontend.capitalize()}.'}, 
                 status=status.HTTP_403_FORBIDDEN # Forbidden access
             )
        # --- END ROLE VERIFICATION ---

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': actual_role_in_db # Send the confirmed actual role
        })