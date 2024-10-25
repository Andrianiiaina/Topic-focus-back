from django.db import models
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category=models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Publication(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='publications/',null=True,blank=True)
    link = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    extra = models.JSONField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name='categories')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='publications')



class FavoriteTopic(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE)
    weight=models.FloatField(default=1.0)

class Comment(models.Model):
    content = models.TextField()
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    publication=models.ForeignKey(Publication, on_delete=models.CASCADE)

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    publication=models.ForeignKey(Publication, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "f{self.user.firstname} liked {self.publication.title}"