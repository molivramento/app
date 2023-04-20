from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from news.models import News
from news.serializers import NewsSerializer

# Confifurar paginação
class NewsPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page_size'
    page_size_query_param = 'page_size'
    max_page_size = 30


class NewsAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, pk=None) -> Response:
        paginator = NewsPagination()
        if pk:
            news = News.objects.get(pk=pk)
            serializer = NewsSerializer(news, many=False)
        else:
            news = News.objects.all()
            result = paginator.paginate_queryset(news, request) # Gera paginação
            serializer = NewsSerializer(result, many=True)
            
        return paginator.get_paginated_response(serializer.data) # Retorna a paginação

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