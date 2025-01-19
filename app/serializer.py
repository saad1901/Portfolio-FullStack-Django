from .models import CustomUser, Info
from rest_framework import serializers

class InfoSrlz(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = "__all__"

class UserSrlz(serializers.ModelSerializer):
    infos = InfoSrlz(read_only=True, many=True, source='info')
    class Meta:
        model = CustomUser
        fields = "__all__"