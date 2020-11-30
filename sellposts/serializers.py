from rest_framework import serializers
from .models import SellAd, AdImages
from django.contrib.auth import get_user_model

class SellAdCreateSrializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    class Meta:
        model = SellAd
        fields = ['id', 'owner', 'title', 'description', 'category', 'asked_price', 'quantity', 'location']

    def create(self, validated_data):
        owner = validated_data.pop('owner')
        adv = SellAd.objects.create(owner=owner, **validated_data)

        return adv

    def update(self, instance, validated_data):
        instance.is_verified = False
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.asked_price = validated_data.get('asked_price', instance.asked_price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        return instance

class ImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImages
        fields = ['product_img']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImages
        fields = ['id', 'product_img']

class SellAdDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    posted_at = serializers.DateTimeField(format="%b %d\'%y at %I:%M %p", read_only=True)

    class Meta:
        model = SellAd
        fields = '__all__'

class SellAdDetailSerializer2(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    posted_at = serializers.DateTimeField(format="%b %d\' %y at %I:%M %p", read_only=True)

    class Meta:
        model = SellAd
        fields = ['id', 'title', 'image', 'asked_price', 'quantity', 'location', 'posted_at']

    def get_image(self, sellad):
        request = self.context.get('request')
        image1 = sellad.images.all()[0]
        
        return request.build_absolute_uri(image1.product_img.url)

class GroupCountSerializer(serializers.Serializer):
    category = serializers.CharField(read_only=True)
    total = serializers.IntegerField(read_only=True)