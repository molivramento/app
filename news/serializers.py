from rest_framework import serializers
from news.models import News, Link


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
