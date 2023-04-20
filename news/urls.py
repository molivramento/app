from django.urls import path
from news.views import NewsAPIView, LinkAPIView

urlpatterns = [
    path("news/", NewsAPIView.as_view(), name="news-api"),
    path("news/<int:pk>/", NewsAPIView.as_view(), name="news-api-detail"),
    path("link/", LinkAPIView.as_view(), name="link-api"),
    path("link/<str:token>/", LinkAPIView.as_view(), name="link-api-get_link")
]
