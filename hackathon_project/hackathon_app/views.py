from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import RegisteredUser, Hackathon
from .serializers import RegisteredUserSerializer, LoginSerializer, HackathonSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegisteredUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            return Response({"message": "Login successful", "user_id": user_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserHackathonCreateView(APIView):
    def post(self, request, **kwargs):
        user_id = kwargs.get('user_id')
        user = RegisteredUser.objects.get(id=user_id)
        serializer = HackathonSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            hackathon = serializer.save(created_by=user)
            return Response({'message': 'Hackathon created successfully', 'hackathon_id': hackathon.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserHackathonUpdateView(APIView):
    def put(self, request, user_id, hackathon_id):
        user = RegisteredUser.objects.get(id=user_id)
        try:
            hackathon = Hackathon.objects.get(id=hackathon_id, created_by=user)
        except Hackathon.DoesNotExist:
            return Response({'message': 'Hackathon not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = HackathonSerializer(hackathon, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Hackathon updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserHackathonDeleteView(APIView):
    def delete(self, request, user_id, hackathon_id):
        user = RegisteredUser.objects.get(id=user_id)
        try:
            hackathon = Hackathon.objects.get(id=hackathon_id, created_by=user)
        except Hackathon.DoesNotExist:
            return Response({'message': 'Hackathon not found'}, status=status.HTTP_404_NOT_FOUND)

        hackathon.delete()
        return Response({'message': 'Hackathon deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
