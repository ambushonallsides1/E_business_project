from rest_framework import serializers

from apps.goods.models import Brand


class BrandSerializer(serializers.ModelSerializer):


    class Meta:
        model = Brand
        fields = '__all__'

    def create(self, validated_data):
        brand = Brand.cre

