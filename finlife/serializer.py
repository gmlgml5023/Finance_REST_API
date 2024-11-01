from rest_framework import serializers
from .models import DepositProducts, DepositOptions


class DepositProductsSerializer(serializers.ModelSerializer):
    class DepositOptionsDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptions
            fields = '__all__'

    option_set = DepositOptionsDetailSerializer(read_only=True, many=True)
    
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only = ['product']