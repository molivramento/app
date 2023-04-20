from datetime import datetime, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from news.models import News, Link
from news.serializers import NewsSerializer, LinkSerializer
from collections import OrderedDict
from django.utils.crypto import get_random_string


class NewsPagination(PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class NewsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, pk=None) -> Response:
        if pk:
            news = News.objects.get(pk=pk)
            serializer = NewsSerializer(news, many=False)
            return Response(serializer.data)
        else:
            news = News.objects.all()
            paginator = NewsPagination()
            result = paginator.paginate_queryset(news, request)
            serializer = NewsSerializer(result, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request) -> Response:
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news_article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news_article = News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        news_article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TODO: add delete method, put method and expire time for link
class LinkAPIView(APIView):
    def post(self, request) -> Response:
        news_id = request.data.get('news_id')
        try:
            news = News.objects.get(id=news_id)
            link = self.generate_link(news.id)
            return Response({'link': link}, status=status.HTTP_201_CREATED)
        except News.DoesNotExist:
            return Response({'message': 'News not found'}, status=status.HTTP_404_NOT_FOUND)

    def generate_link(self, news_id):
        token = get_random_string(length=16)
        news = News.objects.get(pk=news_id)
        link = reverse('link-api-get_link', kwargs={'token': token})
        Link.objects.create(token=token, news=news)
        return link

    def get(self, request, token: str):
        try:
            link = Link.objects.get(token=token)
            serializer = NewsSerializer(link.news)
            return Response(serializer.data)
        except Link.DoesNotExist:
            return Response({'message': 'This link does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk: int):
        try:
            link = Link.objects.get(pk=pk)
            link.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Link.DoesNotExist:
            return Response({'message': 'This link does not exist'}, status=status.HTTP_404_NOT_FOUND)
