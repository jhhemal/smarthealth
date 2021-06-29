from rest_framework import serializers
from .models import VoterID, BMA, OTP

class VoterIDSerializers(serializers.ModelSerializer):
    class Meta:
        model = VoterID
        fields = '__all__'

class BMASerializers(serializers.ModelSerializer):
    class Meta:
        model = BMA
        fields = '__all__'

class OTPSerializers(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'