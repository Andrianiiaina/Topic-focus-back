from rest_framework import serializers
from .models import Publication, Comment, Like,Category

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']  

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']  


class PublicationSerializer(serializers.ModelSerializer):
    author=serializers.StringRelatedField()
    like_count=serializers.SerializerMethodField()
    comments= CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Publication
        fields = ['pk','title', 'link','file',  'content', 'extra', 'category','author','like_count','comments']  # N'inclut pas 'author', géré dans la vue
    def get_like_count(self, obj):
        return Like.objects.filter(publication=obj).count()
    
