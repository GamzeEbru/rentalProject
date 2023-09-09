from rest_framework import serializers
from .models import IHA, Kiralama


class IHASerializer(serializers.ModelSerializer):
    class Meta:
        model = IHA
        fields = '__all__'


class KiralamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiralama
        fields = '__all__'
