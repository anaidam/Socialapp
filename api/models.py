from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
# Create your models here.



class Userprofile(models.Model):
    user         = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    full_name    = models.CharField(max_length=50)
    profile_pic  = models.ImageField(upload_to='images' , null=True)
    bio          = models.CharField(max_length=300)
    timeline_pic = models.ImageField(upload_to='images' , null=True)
    dob          = models.DateField(null=True)
    g_options    = (
        ('Female','Female'),
        ('Male','Male'),
        ('Trans female','Trans female'),
        ('Trans male','Trans male'),
        ('other','other')
    )
    gender       = models.CharField(max_length=20, choices=g_options ,blank=True, null=True)

    is_active    =models.BooleanField(default=True)



class Posts(models.Model):
    caption      = models.CharField(max_length=500)
    image        = models.ImageField(upload_to='images',null=True,blank=True)
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.caption


    @property
    def post_comment(self):
        return Comments.objects.filter(posts=self).annotate(ucount=Count('likes')).order_by('-ucount') 



class Comments(models.Model):
    user         = models.ForeignKey(User,on_delete=models.CASCADE, related_name='author')
    posts        = models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment      = models.CharField(max_length= 500)
    created_date = models.DateTimeField(auto_now_add=True)
    likes        = models.ManyToManyField(User,related_name='comment')

    @property
    def likes_count(self):
        return self.likes.all().count()