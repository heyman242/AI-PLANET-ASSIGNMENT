from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


from .models import RegisteredUser, Hackathon, EnrolledHackathon, Submission
from .serializers import RegisteredUserSerializer, LoginSerializer, HackathonSerializer, HackathonListSerializer, SubmissionSerializer


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


class HackathonListView(generics.ListAPIView):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonListSerializer


class EnrollHackathonView(APIView):
    def post(self, request, user_id, hackathon_id):
        try:
            user = RegisteredUser.objects.get(id=user_id)
            hackathon = Hackathon.objects.get(id=hackathon_id)
        except RegisteredUser.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)
        except Hackathon.DoesNotExist:
            return Response({'message': 'Invalid hackathon ID'}, status=status.HTTP_404_NOT_FOUND)

        enrollment, created = EnrolledHackathon.objects.get_or_create(user=user, hackathon=hackathon)
        if created:
            return Response({'message': 'Successfully enrolled in the hackathon'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Already enrolled in the hackathon'}, status=status.HTTP_400_BAD_REQUEST)


class SubmitHackathonView(APIView):
    def post(self, request, user_id, hackathon_id):
        try:
            user = RegisteredUser.objects.get(id=user_id)
            hackathon = Hackathon.objects.get(id=hackathon_id)
        except RegisteredUser.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)
        except Hackathon.DoesNotExist:
            return Response({'message': 'Invalid hackathon ID'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubmissionSerializer(data=request.data)
        existing_submission = Submission.objects.filter(user=user, hackathon=hackathon).exists()
        if existing_submission:
            return Response({'message': 'You have already made a submission for this hackathon'},
                            status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save(user=user, hackathon=hackathon)
            return Response({'message': 'Submission created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrolledHackathonListView(APIView):
    def get(self, request, user_id):
        try:
            user = RegisteredUser.objects.get(id=user_id)
        except RegisteredUser.DoesNotExist:
            return Response({'message': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        enrolled_hackathons = EnrolledHackathon.objects.filter(user=user)
        hackathon_data = []

        for enrolled_hackathon in enrolled_hackathons:
            hackathon = enrolled_hackathon.hackathon
            hackathon_data.append({
                'id': hackathon.id,
                'title': hackathon.title,
                'start_datetime': hackathon.start_datetime,
                'end_datetime': hackathon.end_datetime,
                'reward_prize': hackathon.reward_prize
            })

        return Response(hackathon_data, status=status.HTTP_200_OK)


class UserSubmissionsView(ListAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        hackathon_id = self.kwargs['hackathon_id']
        return Submission.objects.filter(user_id=user_id, hackathon_id=hackathon_id)