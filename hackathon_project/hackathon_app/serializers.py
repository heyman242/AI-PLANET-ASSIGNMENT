from rest_framework import serializers

from .models import RegisteredUser, Hackathon


class RegisteredUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = RegisteredUser
        fields = ['name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.password = password
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        user = RegisteredUser.objects.filter(phone_number=phone_number, password=password).first()
        if user is None:
            raise serializers.ValidationError("Invalid phone number or password")

        data['user_id'] = user.id

        return data


class HackathonSerializer(serializers.ModelSerializer):
    hackathon_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hackathon
        fields = ['hackathon_id', 'title', 'description', 'background_image', 'hackathon_image', 'submission_type',
                  'start_datetime', 'end_datetime', 'reward_prize']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        created_by = validated_data.pop('created_by', None)
        hackathon = Hackathon.objects.create(created_by=created_by, **validated_data)
        return hackathon
