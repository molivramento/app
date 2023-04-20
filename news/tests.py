from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from news.models import News
from news.serializers import NewsSerializer


class NewsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('news-api')
        self.news_data = {
            'title': 'Test News Article',
            'content': 'This is a test news article.',
            'author': 'John Doe',
        }
        self.news_data1 = {
            'title': 'Test News Article 1',
            'content': 'This is a test news article 1.',
            'author': 'John Doe',
        }
        self.news_data2 = {
            'title': 'Test News Article 2',
            'content': 'This is a test news article 2.',
            'author': 'John Doe',
        }
        self.news = News.objects.create(**self.news_data)
        self.news1 = News.objects.create(**self.news_data1)
        self.news2 = News.objects.create(**self.news_data2)
    
    def test_get_all_news(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], self.news.title)
        self.assertEqual(response.data['results'][1]['title'], self.news1.title)
    
    def test_retrive_one_news(self):
        url = reverse('news-api-detail', args=[self.news.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = NewsSerializer(News.objects.get(id=self.news.id), many=False).data
        self.assertEqual(response.data, expected_data)

    def test_delete_one_news(self):
        url = reverse('news-api-detail', args=[self.news.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(News.objects.filter(pk=self.news.id).exists())
    
    def test_update_one_news(self):
        updated_news_data = {
            'title': 'Updated Test News Article',
            'content': 'This is an updated test news article.',
            'author': 'Alice Brown',
            "category": "politics",
        }
        url = reverse('news-api-detail', args=[self.news.id])
        response = self.client.put(url, updated_news_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = NewsSerializer(News.objects.get(pk=self.news.id)).data
        self.assertEqual(response.data, expected_data)
        
    # O erro ocorre pois a tabela "news" possui como campo obrigatório a coluna "category" que não foi enviado no teste.
    # Correção, bastou adicionar o valor da categoria no dicionário: 'category': 'technology' 
    def test_create_news(self):
        new_news_data = {
            'title': 'New Test News Article',
            'content': 'This is a new test news article.',
            'author': 'Jane Smith',
            'category': 'technology',
        }
        response = self.client.post(self.url, new_news_data, format='json')
  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_data = NewsSerializer(News.objects.get(pk=response.data['id'])).data
        self.assertEqual(response.data, expected_data)