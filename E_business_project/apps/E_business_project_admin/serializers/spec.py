from rest_framework import serializers

from apps.goods.models import SPUSpecification


class SPUSpecificationSerializer(serializers.ModelSerializer):

    # 关联嵌套返回spu表的商品名
    spu = serializers.StringRelatedField(read_only=True)
    # 返回关联spu的id值
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = '__all__'