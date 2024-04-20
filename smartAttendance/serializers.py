from rest_framework import serializers
from .models import User, Attendance,Message
from rest_framework.validators import ValidationError


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ['time', 'user']


class UserSerializer(serializers.ModelSerializer):
    attendance = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = [
            'email',
            'department',
            'username',
            'password',
            'photo',
            'attendance'
        ]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        attendance_data = validated_data.pop('attendance')
        user = User.objects.create_user(**validated_data)
        user.save()
        for attendance in attendance_data:
            Attendance.objects.create(user=user, **attendance)

        return user


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['title', 'message', 'posted_date', 'user']

# admin views