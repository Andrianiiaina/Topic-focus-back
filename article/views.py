from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Publication, Category, Comment, Like, FavoriteTopic
from user.models import User
from .serializers import PublicationSerializer,CommentSerializer
from django.http import JsonResponse 
import requests
from django.views.decorators.csrf import csrf_exempt

import article.utilities.similarity_calcul as similarity_calcul


@api_view(['POST'])
def create_publication(request):
    user_id = request.user.pk
    data = request.data.copy()
    data['author'] = user_id  
    data['link']=""
    data['extra']={}
    serializer = PublicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def show_publication(request,publication_id):
    try:
        publication = Publication.objects.get(id=publication_id)
        serializer = PublicationSerializer(publication)
        return JsonResponse(serializer.data,status=200)
    except Publication.DoesNotExist:
        return JsonResponse({'error':'Publication not found'}, status=400)

@csrf_exempt
@api_view(['GET'])
def get_recommendations(request):
    try:
        user=request.user
        recommended_articles=similarity_calcul.display_feed_hierarchy(user)
        serializer = PublicationSerializer(recommended_articles,many=True)
        return JsonResponse(serializer.data,status=200,safe=False)
    except Publication.DoesNotExist:
        return JsonResponse({'error':'no publication found for this user'}, status=400)

@csrf_exempt
@api_view(['GET'])
def get_user_publications(request,user_id):
    try:
        publications = Publication.objects.filter(author_id=user_id)[:6]
        serializer = PublicationSerializer(publications,many=True)
        return JsonResponse(serializer.data,status=200,safe=False)
       
    except Publication.DoesNotExist:
        return JsonResponse({'error':'no publication found for this user'}, status=400)

#@csrf_exempt
@api_view(['POST'])
def create_comment(request, publication_id):
    user=request.user
    try:
        data = request.data.copy()
        comment,created=Comment.objects.get_or_create(
                content=data['content'],
                publication_id=publication_id,
                owner_id=user.pk,
            )
        category=Publication.objects.get(pk=publication_id).category   
        favorite_topic, created_topic=FavoriteTopic.objects.get_or_create(user, category)
        favorite_topic.weight += 2.0
        favorite_topic.save()
        weight=favorite_topic.weight
        #print(f"poids de l'article commenté:{weight}")
        if(created):
            return JsonResponse({'message':"commented",'comment':comment},status=201)
        return JsonResponse({
            'message':'commentaire enrégistré',
            'comment':comment.content
        })
    except Exception as e:
        return JsonResponse({'error':'une erreur!'})

@csrf_exempt
@api_view(['POST'])
def like_publication(request,publication_id):
    user=request.user
    if not user.is_authenticated:
        return JsonResponse({'error':'authentifiez vous XD'})
    
    try:
        like, created=Like.objects.get_or_create(user=user, publication=publication_id)
        
        category=Publication.objects.get(pk=publication_id).category   
        favorite_topic, created_topic=FavoriteTopic.objects.get_or_create(user, category)
        favorite_topic.weight += 1.0
        favorite_topic.save()
        weight=favorite_topic.weight
        #print(f"poids de l'article liké +1:{weight}")

        if(created):
            return JsonResponse({'message':"Pulication_liked",'like':True},status=201)
        else:
            like.delete()
            return JsonResponse({'message':"Like removed",'like':False},status=200)
    except Exception as e:
            return JsonResponse({'error':"something went wrong!"},status=405)








@api_view(['GET'])
def search_publications(request,q):
    
    api_key = "cc7e05da68ed43b6895773e3d1161727"
    url = f'https://newsapi.org/v2/everything?q={q}&pageSize=10&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        raise Exception(f"Erreur when recuperate articles, please verify your connexion : {response.status_code}")
   