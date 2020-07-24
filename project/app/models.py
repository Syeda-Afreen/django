from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    phone=models.IntegerField()
    desc=models.TextField(max_length=300)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=10)
    content=models.TextField()
    name=models.CharField(max_length=25)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.name

class PersonalBlogPost(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    content=models.TextField()
    author=models.CharField(max_length=50)
    img=models.ImageField(upload_to='pictures',blank=True,null=True)
    timeStamp=models.DateTimeField(blank=True)

    def __str__(self):
        return self.title
    






    
