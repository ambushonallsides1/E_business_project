from rest_framework import serializers

from apps.goods.models import SKU, GoodsCategory, SPU, SpecificationOption, SPUSpecification, SKUSpecification


class SKUSpecificationSerialzier(serializers.ModelSerializer):
    """
        SKU规格表序列化器
    """
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification  # SKUSpecification中sku外键关联了SKU表
        fields = ("spec_id", 'option_id')


class SKUSerializer(serializers.ModelSerializer):

    spu = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    specs = SKUSpecificationSerialzier(many=True)  # 外键

    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        # 1.获取specs的数据
        data = self.context['request'].data
        specs = data.get('specs')

        # 2.把validated_data中的 specs 删除掉
        if 'specs' in validated_data:
            del validated_data['specs']

        # 3.保存sku数据
        sku = SKU.objects.create(**validated_data)

        # 4.自己手动实现specs的数据入库
        for item in specs:
            # item = {spec_id: "4", option_id: 8}
            SKUSpecification.objects.create(
                sku=sku,
                spec_id=item.get('spec_id'),
                option_id=item.get('option_id')
            )

        # 生成详情页面
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(sku.id)

        return sku

    def update(self, instance, validated_data):
        # 1.把validated_data中的 specs 删除掉
        if 'specs' in validated_data:
            del validated_data['specs']
        # 2.获取pk
        pk = self.context['view'].kwargs.get('pk')
        # 3.更新数据
        SKU.objects.filter(id=pk).update(**validated_data)

        # 4.更新规格信息
        specs = self.context['request'].data.get('specs')
        # [{spec_id: "4", option_id: 8}, {spec_id: "5", option_id: 11}]
        for item in specs:
            # item {spec_id: "4", option_id: 8}
            SKUSpecification.objects.filter(sku_id=pk,
                                            spec_id=item.get('spec_id')). \
                update(option_id=item.get('option_id'))

        # 重新生成详情页面
        from celery_tasks.html.tasks import generate_static_sku_detail_html
        generate_static_sku_detail_html.delay(pk)

        return instance

class SKUCategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class SPUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = '__all__'


class SPUOptineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecSerialzier(serializers.ModelSerializer):
    spu = serializers.StringRelatedField(read_only=True)
    spu_id = serializers.IntegerField(read_only=True)
    # 关联序列化返回 规格选项信息
    options = SPUOptineSerializer(read_only=True, many=True)  # 使用规格选项序列化器

    class Meta:
        model = SPUSpecification  # SPUSpecification中的外键spu关联了SPU商品表
        fields = "__all__"
