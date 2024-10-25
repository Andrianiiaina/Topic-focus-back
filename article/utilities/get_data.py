from rest_framework import status
from rest_framework.response import Response
from .models import Publication, Category
from user.models import User
from django.http import JsonResponse 
import requests
from datetime import datetime

def fetch_and_store_articles_from_newsapi(request):
    categories = ['technology', 'sports', 'health','business','entertainment','general','science']
    #flush database
    Publication.objects.all().delete()
    for category in categories:
        Category.objects.get_or_create(name=category)
        pulications=fetch_articles_from_newsapi_by_category(category)
        print(category)
        store_articles_from_newsapi(pulications, category)
    return JsonResponse(pulications, safe=False)
   
  

def fetch_articles_from_newsapi_by_category(category):
    api_key = "cc7e05da68ed43b6895773e3d1161727"
    url = f'https://newsapi.org/v2/top-headlines?category={category}&pageSize=50&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        raise Exception(f"Erreur when fetch articles : {response.status_code}")
  
def store_articles_from_newsapi(publications, category):
    #seulement si l'imageUrl est valide
    filtered_publications=[
        publication_ for publication_ in publications
        if is_valid_image(publication_.get('urlToImage'))
    ]
    for publication in filtered_publications:
        Publication.objects.create(
            title=publication['title'],
            file=publication['urlToImage'],
            link=publication['url'],
            content=publication['description'],
            category=Category.objects.get(name=category),
            author=User.objects.first(),
            extra={},
            date=datetime.strptime(publication['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
        )

def is_valid_image(url):
    try:
        response= requests.head(url,timeout=5)
        if(response.status_code==200 and 'image' in response.headers.get('Content-Type','')):
            return True
        return False
    except requests.RequestException:
        return False


