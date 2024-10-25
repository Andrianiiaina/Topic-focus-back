"""
URL configuration for topic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from article.views import get_recommendations,search_publications,create_publication,get_user_publications,create_comment,like_publication,show_publication
from user.views import list_users
from article.utilities.get_data import fetch_and_store_articles_from_newsapi
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('fetch/', fetch_and_store_articles_from_newsapi,name="fetch_and_store"),
    path('api/publication/', create_publication, name='create_publication'),

    path('api/publication/<int:publication_id>/', show_publication, name='show_publication'),

    path('api/publications/', get_recommendations, name='recommanded_articles_for_current'),

    path('api/publication/<int:publication_id>/like/',like_publication, name='create_like'),
    path('api/publication/<int:publication_id>/comment/', create_comment, name='create_comment'),
    
    path('api/search/<str:q>/', search_publications, name='search_publication'),

    path('api/user/<int:user_id>/publications/', get_user_publications, name='user_publication'),

]
