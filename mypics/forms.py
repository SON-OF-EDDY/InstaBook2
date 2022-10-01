from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Picture,Profile,Song,Conversation,Query,Critique,Help

class PictureForm(ModelForm):

    class Meta:

        model = Picture

        fields = "__all__"

        exclude = ('author','likes','hearted','connected_user','date','place')

        widgets = {

            'title':forms.TextInput(attrs={'class':'form-control'}),
            #'author':forms.TextInput(attrs={'class':'form-control'}),
            #'date':forms.TextInput(attrs={'class':'form-control'}),
            #'place':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),

        }

class SongForm(ModelForm):

    class Meta:

        model = Song

        fields = "__all__"

        exclude = ('author','connected_user')

        widgets = {

            'title':forms.TextInput(attrs={'class':'form-control'}),
            'artist':forms.TextInput(attrs={'class':'form-control'}),
            #'author': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QueryForm(ModelForm):

    class Meta:

        model = Query

        fields = "__all__"

        exclude = ('user_filing_complaint',)

        widgets = {

            'offending_user':forms.TextInput(attrs={'class':'form-control'}),
            'picture_name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Picture Name/ Leave blank'}),
            'song_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter Song Name/ Leave blank'}),
            'details': forms.Textarea(attrs={'class': 'form-control'}),

        }


class CritiqueForm(ModelForm):

    class Meta:

        model = Critique

        fields = "__all__"

        exclude = ('user_making_recommendation',)

        widgets = {

            'details': forms.Textarea(attrs={'class': 'form-control'}),

        }




class EditUserForm(UserChangeForm):

    email = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))
    #last_login = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))
    # is_superuser = forms.CharField(max_length=120,widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    # is_staff = forms.CharField(max_length=120,widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    # is_active = forms.CharField(max_length=120,widget=forms.CheckboxInput(attrs={'class':'form-control'}))
    #date_joined = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')

class EditSettingsForm(ModelForm):

    bio = forms.CharField(max_length=120,required=False,widget=forms.Textarea(attrs={'class':'form-control'}))
    youtube_url =  forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    vk_url = forms.CharField(max_length=120, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    telegram_url = forms.CharField(max_length=120, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    private = forms.BooleanField(required=False)


    class Meta:

        model = Profile

        fields = ('private','bio','youtube_url','vk_url','telegram_url','profile_pic')


class PasswordForm(PasswordChangeForm):

    old_password = forms.CharField(max_length=120,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 = forms.CharField(max_length=120,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length=120,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))

    class Meta:

        fields = ('old_password','new_password1','new_password2')


class SignUpForm(UserCreationForm):

    username = forms.CharField(max_length=120,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=120,label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    password2 = forms.CharField(max_length=120,label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))


class MessageForm(ModelForm):

    dialogue = forms.CharField(max_length=120,widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:

        model = Conversation

        fields = ('dialogue',)


class HelpForm(ModelForm):

    dialogue = forms.CharField(max_length=120,widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:

        model = Help

        fields = ('dialogue',)