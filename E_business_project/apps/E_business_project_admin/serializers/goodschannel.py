from rest_framework import serializers

from apps.goods.models import GoodsChannel, GoodsChannelGroup


class GoodsChannelSerializer(serializers.ModelSerializer):

    group = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    group_id = serializers.IntegerField()
    category_id = serializers.IntegerField()



    class Meta:
        model = GoodsChannel
        # fields = '__all__'
        fields = ['id','group', 'group_id', 'category', 'category_id', 'url', 'sequence']


class GoodsChannelGroupSerializer(serializers.ModelSerializer):


    class Meta:
        model = GoodsChannelGroup
        fields = '__all__'