from rest_framework import serializers
from .models import Company, Auction, Lot, Images


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction


class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
