import re
from collections import Counter
from ..models import Publication,Like, Category, Like, FavoriteTopic
import math
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.decorators import api_view


def recommend_articles_hierarchy(user):
    liked_articles = Like.objects.filter(user=user).values_list('publication', flat=True)
    liked_articles = Publication.objects.filter(id__in=liked_articles)
   
    liked_frequencies = [compute_word_frequencies(pub) for pub in liked_articles]
   
    favorite_topics = FavoriteTopic.objects.filter(user=user)
    topic_weights = {fav.Category.id: fav.weight for fav in favorite_topics}
    #print(topic_weights)
    articles = Publication.objects.all()
    #si démarrage à froid: données populaire à afficher:
    if not favorite_topics.exists() and not liked_articles.exists():
        return articles[:10]
    recommendations = []
    for publication in articles:
        if publication in liked_articles:
            continue
        pub_freq = compute_word_frequencies(publication)
        similarity_score = max([cosine_similarity(pub_freq, liked_freq) for liked_freq in liked_frequencies])
       
        categories=Category.objects.all()
        category_weight = sum([
            topic_weights.get(cat.id, 0) + (topic_weights.get(cat.parent_category.id, 0) * 0.5 if cat.parent_category else 0)
            for cat in categories
        ])
       
        # Score final = Similarité + Poids des catégories
        final_score = similarity_score + category_weight
       
        recommendations.append((publication, final_score))
    recommendations.sort(key=lambda x: x[1], reverse=True)
   
    return [pub for pub, score in recommendations[:10]]

def display_feed_hierarchy(user):
    recommended_articles = recommend_articles_hierarchy(user)
    print(f"Top 10 articles recommendés pour {user.username}:")
    for pub in recommended_articles:
        print(f"- {pub.title}")
    return recommended_articles

def compute_word_frequencies(publication):
    # Extraire le texte à partir du titre et de la description
    text = (publication.title + ' ' + publication.content).lower()
    words = re.findall(r'\w+', text)
    return Counter(words)


# Calcul similarité cosinus entre deux dictionnaires de fréquence
def cosine_similarity(freq1, freq2):
    intersection = set(freq1.keys()) & set(freq2.keys())
    numerator = sum([freq1[x] * freq2[x] for x in intersection])

    sum1 = sum([freq1[x]**2 for x in freq1.keys()])
    sum2 = sum([freq2[x]**2 for x in freq2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

"""
def extract_subcategories_from_articles(article):
    all_words = []
    words = re.findall(r'\w+', article.title.lower())
    all_words.extend(words)

    # Fréquence des mots pour extraire les sous-catégories potentielles
    common_words = Counter(all_words).most_common(10)
    subcategories = [word for word, count in common_words if len(word) > 3]  # Exclure les mots courts
    return subcategories

def populate_subcategories():
    API_KEY = 'votre_cle_newsapi'
    CATEGORIES = ['business', 'entertainment', 'health', 'science', 'sports', 'technology']
    articles=Publication.objects.all()[:10]
    for article in articles:
        subcategories = extract_subcategories_from_articles(article)
        parent_category, _ = Category.objects.get_or_create(name=article.category)
        for subcategory_name in subcategories:
            Category.objects.get_or_create(name=subcategory_name, parent_category=parent_category)
"""