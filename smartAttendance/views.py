from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from .models import User, Attendance, Message
from .serializers import UserSerializer, AttendanceSerializer, MessageSerializer
from rest_framework import generics, permissions, authentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import cv2
from deepface import DeepFace
import numpy as np
import os
from io import BytesIO
from .faceRecor import verify_user, detect_face
from rest_framework.validators import ValidationError

base_url = os.path.dirname(os.path.abspath(__file__))


def imageProcessing(image):
    print(f"image resize begins {datetime.now()} ")
    image_bytes = image.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    resizedImage = cv2.resize(image, (0, 0), fx=0.08, fy=0.08)
    # cv2.imwrite("nelson2.jpg", resizedImage)
    ret, buffer = cv2.imencode('.jpg', resizedImage)
    image_bytes = BytesIO(buffer)
    print(f"resize end {datetime.now()} ")

    return image_bytes


class ListApiView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


listApiView = ListApiView.as_view()


@api_view(["POST", ])
def signUp(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        photo1 = serializer.validated_data.pop('photo')
        faces = detect_face(photo1)
        if not faces:
            return Response(data='No face detected', status=status.HTTP_400_BAD_REQUEST)
        elif len(faces) > 1:
            return Response(data='more than one face detected', status=400)
        serializer.save(photo=photo1)
        return Response(data='your have successful registered', status=status.HTTP_201_CREATED)
    print(serializer.errors.get('email'))
    return Response(data=serializer.errors.get('email'), status=status.HTTP_400_BAD_REQUEST)


class GetIndividualAttendanceView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        print(self.request.user)
        return qs.filter(user=self.request.user).order_by("-time")


attendance = GetIndividualAttendanceView.as_view()



@api_view(["POST", "GET"])
@permission_classes((IsAuthenticated,))
def check_user(request):
    photo = request.data.get('photo')
    path = request.user.photo
    absolute_path = 'media/'+path
    image_bytes = photo.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = DeepFace.verify(absolute_path, image, enforce_detection=False)
    print(result)
    return Response(result)




class MessageListView(generics.ListAPIView):
    print(Message.objects.order_by())
    queryset = Message.objects.all().order_by('-posted_date')
    serializer_class = MessageSerializer


view_all_messages = MessageListView.as_view()

"""
admin views to create messages and 
view attendance 
"""


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        expo_tokens = []
        users = User.objects.all()
        for user in users:
            if user.expo_token:
                expo_tokens.append(user.expo_token)
        print(expo_tokens)
        return super().create(request, *args, **kwargs)


admin_create_message_view = MessageCreateView.as_view()
