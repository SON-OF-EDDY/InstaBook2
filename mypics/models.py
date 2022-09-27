from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.utils.html import mark_safe

class Profile(models.Model):

    member = models.OneToOneField(User,null=True,on_delete=models.CASCADE,unique=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(null=True,blank=False,upload_to='images/')
    youtube_url = models.CharField(max_length=120,null=True,default='https://www.youtube.com',blank=True)
    telegram_url = models.CharField(max_length=120,null=True,default='https://web.telegram.org/k/',blank=True)
    vk_url = models.CharField(max_length=120,null=True,default='https://vk.com/',blank=True)
    friend_id_list = models.CharField(max_length=120,null=True,blank=True,validators=[validate_comma_separated_integer_list])
    requests = models.CharField(max_length=120,null=True,blank=True,validators=[validate_comma_separated_integer_list])
    pendings = models.CharField(max_length=120,null=True,blank=True,validators=[validate_comma_separated_integer_list])
    accepted = models.CharField(max_length=120,null=True,blank=True,validators=[validate_comma_separated_integer_list])
    declined = models.CharField(max_length=120, null=True, blank=True,validators=[validate_comma_separated_integer_list])
    private = models.BooleanField(null=True, blank=True)
    online = models.BooleanField(null=False,blank=False,default=False)

    def __str__(self):
        return str(self.member)



def get_default_action_status():
    return User.objects.get(username="tim")

class Picture(models.Model):

    # member = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    # models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="+")
    author = models.CharField(max_length=120,default="")

    connected_user = models.ForeignKey(User,default=get_default_action_status,on_delete=models.CASCADE,related_name="+")

    # null=True, default=None, on_delete=models.CASCADE, related_name="suppliers"
    #author = models.OneToOneField(User, default='',null=True,on_delete=models.CASCADE)

    title = models.CharField(max_length=120)
    date = models.CharField(max_length=120,blank=True)
    place = models.CharField(max_length=120,blank=True)
    description = models.TextField(blank=True)
    picture_image = models.ImageField(null=True,blank=False,upload_to='images/')
    likes = models.CharField(max_length=120,default=0)
    hearted = models.CharField(max_length=120, null=True,blank=True,default='',validators=[validate_comma_separated_integer_list])

    #def __str__(self):
        #return self.title

    def pic_preview(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.picture_image.url)



class Song(models.Model):

    title = models.CharField(max_length=120)
    artist = models.CharField(max_length=120)
    author = models.CharField(max_length=120)

    connected_user = models.ForeignKey(User, default=1, on_delete=models.CASCADE,related_name="+")

    song_file = models.FileField(upload_to='songs/')

    def __str__(self):
        return self.title

class Conversation(models.Model):

    member_1 = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="+")
    member_2 = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="+")

    dialogue = models.TextField(blank=True)

    def __str__(self):
        return str(self.member_1)+" and "+ str(self.member_2)+"'s conversation"

class Query(models.Model):

    user_filing_complaint = models.CharField(max_length=120,default=None)
    offending_user = models.CharField(max_length=120,default=None)
    # picture_song_name = models.CharField(max_length=120)
    # details = models.TextField(blank=True)

    #user_filing_complaint = models.ForeignKey(Profile,blank=False,on_delete=models.CASCADE,related_name="+")
    #offending_user = models.ForeignKey(Profile,blank=False,null=True,on_delete=models.CASCADE,related_name="+")
    picture_name = models.CharField(max_length=120,default=None,blank=True)
    song_name = models.CharField(max_length=120,default=None,blank=True)
    details = models.TextField(blank=False,default=None)

    def __str__(self):
        return "Complaint against " + str(self.offending_user)


class Critique(models.Model):

    user_making_recommendation = models.CharField(max_length=120, default=None)
    details = models.TextField(blank=False, default=None)

    def __str__(self):
        return str(self.user_making_recommendation)+"'s "+"recommendation"


class Help(models.Model):

    user_asking_help = models.CharField(max_length=120, default=None)
    dialogue = models.TextField(blank=True, default=None)

    def __str__(self):
        return str(self.user_asking_help)+ " needs help!"















