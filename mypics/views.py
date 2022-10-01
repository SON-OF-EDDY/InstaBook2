import re

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import PictureForm,EditUserForm,PasswordChangeForm,PasswordForm,EditSettingsForm,SongForm,MessageForm,QueryForm,CritiqueForm,HelpForm,SignUpForm
from .models import Picture,Profile,Song,Conversation,Help
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from .webscraping import find_trending,most_watched,russian_youtube
import datetime
from django.http import JsonResponse
import json

########################################################################################################################
# TO DO:
########################################################################################################################

#??????     CURRENTLY WORKING ON  ????????????
#???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
#???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
#??????     CURRENTLY WORKING ON  ????????????
# get it working and that's it!!!
#???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
#???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

# MAYBE
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#%%%%%%%    STYLE AND LATER      %%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
########################################################################################################################
########################################################################################################################

def report(request):

    current_user = str(request.user).lower()

    if request.method == 'POST':

        form = QueryForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)
            post.user_filing_complaint = str(request.user).lower()
            form.save()

            messages.success(request, ('Complaint Sent to Admin!'))

            form = QueryForm()

            return render(request, 'report.html', {

                'form': form,
                'current_user': current_user,
            })

    else:

        form = QueryForm()

        return render(request, 'report.html', {

            'form': form,
            'current_user': current_user,

        })


def help(request):

    current_user = str(request.user.username).lower()

    try:
        entry = Help.objects.get(user_asking_help = current_user )
    except:
        entry = Help(user_asking_help=current_user,dialogue = 'ADMIN: How can I help?')
        entry.save()

    return render(request, 'help.html', {

        "entry":entry,
        "current_user":current_user,

    })


def critique(request):

    current_user = str(request.user).lower()

    if request.method == 'POST':

        form = CritiqueForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user_making_recommendation = str(request.user).lower()
            form.save()

            messages.success(request, ('Recommendation Sent to Admin!'))

            form = CritiqueForm()

            return render(request, 'critique.html', {

                'form': form,
                'current_user': current_user,
            })

    else:

        form = CritiqueForm()

        return render(request, 'critique.html', {

            'form': form,
            'current_user': current_user,

        })


def search(request):

    url_id = '1'

    url_id_b = '1'

    show = False

    if request.method == 'POST':

        query = request.POST['my_query']

        query = query.lower()

    # we need to look through all users and check the usernames
    # we need to look through all profiles and check the first and last names
    # any User that has a match gets added to a final list
    # final list is passed to the template and a list of results is displayed (at least initially)

        all_users = Profile.objects.all()

        final_list = []

        for user in all_users:

            #check username first

            username = str(user.member.username).lower()

            match_object = re.search(query,username)

            if match_object:

                final_list.append(user)

            # if not in username check first name

            else:

                first_name = str(user.member.first_name).lower()

                match_object = re.search(query,first_name)

                if match_object:
                    final_list.append(user)

                # if not in username check last name

                else:

                    last_name = str(user.member.last_name).lower()

                    match_object = re.search(query, last_name)

                    if match_object:
                        final_list.append(user)


        user_id = request.user.profile.id

        current_profile = Profile.objects.get(pk=user_id)

        if current_profile in final_list:
            final_list.remove(current_profile)

        if final_list != []:
            show = True

        user_profile = request.user

        member_id_from_user = user_profile.profile.id

        member_instance = Profile.objects.get(pk=member_id_from_user)

        member_instance_friends = member_instance.friend_id_list

        requests_sent = member_instance.pendings

        people_who_already_sent_you_requests = member_instance.requests

        list_people_who_already_sent_you_requests = []

        if member_instance in final_list:
            final_list.remove(member_instance)

        if people_who_already_sent_you_requests != None and people_who_already_sent_you_requests != "":

            if people_who_already_sent_you_requests[0] == ',':
                people_who_already_sent_you_requests = people_who_already_sent_you_requests[1:]

            list_people_who_already_sent_you_requests = people_who_already_sent_you_requests.split(sep=',')
            list_people_who_already_sent_you_requests = list(map(int, list_people_who_already_sent_you_requests))


        if requests_sent != None:

            list_requests_sent = requests_sent.split(sep=',')

            if list_requests_sent != [] and list_requests_sent != [""]:

                if list_requests_sent[0] == '':
                    list_requests_sent = list_requests_sent[1:]
                    member_instance.pendings = ','.join(list_requests_sent)
                    member_instance.save()
                    list_requests_sent = list(map(int, list_requests_sent))

                else:
                    list_requests_sent = list(map(int, list_requests_sent))

            else:
                list_requests_sent = []
                list_requests_sent = list(map(int, list_requests_sent))

        else:

            list_requests_sent = []
            list_requests_sent = list(map(int, list_requests_sent))


        if member_instance_friends != None:

            temp = member_instance.friend_id_list.split(sep=',')

            if temp != [] and temp != [""]:

                if member_instance_friends[0]==',':
                    member_instance_friends = member_instance_friends[1:]
                    member_instance.friend_id_list = member_instance_friends
                    member_instance.save()
                    temp = [int(member_instance_friends)]

                else:
                    temp = member_instance.friend_id_list.split(sep=',')
                    temp = list(map(int, temp))

                current_friends = temp

            else:
                current_friends = []

        else:
            current_friends = []

        return render(request, 'search.html', {
            "query":query,
            "final_list":final_list,
            "list_requests_sent":list_requests_sent,
            "list_people_who_already_sent_you_requests":list_people_who_already_sent_you_requests,
            "current_friends":current_friends,
            "member_instance_friends":member_instance_friends,
            "url_id":url_id,
            "url_id_b":url_id_b,
            "show":show,

        })

    else:

        return redirect('home')



def delete_account(request,user_id):

    account = User.objects.get(id=user_id)

    current_user_profile_id = request.user.profile.id

    current_profile = Profile.objects.get(pk=current_user_profile_id)

    all_pics = Picture.objects.all()

    for pic in all_pics:

        if pic.hearted != '':

            if len(pic.hearted) > 2:

                hearted_list = pic.hearted.split(sep=',')
                # ['2','13','15']

                num_likes = pic.likes

                if str(current_user_profile_id) in hearted_list:

                    hearted_list.remove(str(current_user_profile_id))

                    # ['13','15]

                    num_likes = str(int(num_likes) - 1)

                    hearted_list_as_str = ','.join(hearted_list)

                    pic.hearted = hearted_list_as_str

                    pic.likes = num_likes

                    pic.save()

                    # '13,15'

            elif len(pic.hearted) == 2:

                hearted_list = pic.hearted.split(sep=',')
                # ['2','13']

                num_likes = pic.likes

                if str(current_user_profile_id) in hearted_list:

                    hearted_list.remove(str(current_user_profile_id))

                    # ['13']

                    num_likes = str(int(num_likes) - 1)

                    hearted_list_as_str = ''.join(hearted_list)

                    pic.hearted = hearted_list_as_str

                    pic.likes = num_likes

                    pic.save()

            elif len(pic.hearted) == 1:

                #'13'

                num_likes = pic.likes

                if str(current_user_profile_id) == pic.hearted:

                    num_likes = str(int(num_likes) - 1)

                    hearted_list_as_str = ''

                    pic.hearted = hearted_list_as_str

                    pic.likes = num_likes

                    pic.save()

    account.delete()
    messages.success(request,('Account Deleted!'))

    return redirect("home")

    # associate each pic with a user account...
    # its author tag probably, or maybe a different tag...
    # also for each pic in Pictures, we need to delete from their hearted the deleted users id number...





def my_requests(request):

    # ###############################################################
    # # profile, friend request stuff
    #
    url_id = '1'

    url_id_b = '1'

    accepted_list = None

    declined_list = None

    show = False

    show_2 = True
    #
    user = request.user
    #
    final_list = []

    list_2 = []

    list_3 = []

    list_4 = []

    if user.is_authenticated:

        profiles = Profile.objects.all()

        profile_instance_id = user.profile.id

        profile_instance = Profile.objects.get(pk=profile_instance_id)

        friend_requests = profile_instance.requests

        if profile_instance.pendings == "" or profile_instance.pendings == None :
            show_2 = False


        if profile_instance.pendings != None:

            pending_list = profile_instance.pendings.split(sep=',')

            for profile in profiles:
                if str(profile.id) in pending_list:
                    list_3.append(Profile.objects.get(pk=profile.id))



        #######accepted#############

        if profile_instance.accepted != None:

            accepted_list = profile_instance.accepted.split(sep=',')

            for profile in profiles:
                if str(profile.id) in accepted_list:
                    list_2.append(Profile.objects.get(pk=profile.id))

            profile_instance.accepted = None
            profile_instance.save()


        #######declined#############


        if profile_instance.declined != None:

            declined_list = profile_instance.declined.split(sep=',')

            for profile in profiles:
                if str(profile.id) in declined_list:
                    list_4.append(Profile.objects.get(pk=profile.id))

            profile_instance.declined = None
            profile_instance.save()


        # requests

        if friend_requests != None:

            list_friend_requests = friend_requests.split(sep=',')

            final_list = []

            for profile in profiles:
                if str(profile.id) in list_friend_requests:
                    final_list.append(Profile.objects.get(pk=profile.id))

            if final_list != []:
                show = True
            else:
                show = False



        return render(request, 'my_requests.html', {

            'show': show,
            'show_2': show_2,
            'final_list': final_list,
            'accepted_list': accepted_list,
            'declined_list': declined_list,
            'list_2': list_2,
            'list_3': list_3,
            'list_4': list_4,
            'url_id': url_id,
            'url_id_b':url_id_b,

        })

    else:
        return redirect('login_user')


def accept(request,id,url_id):

    user = request.user

    user_profile_id = user.profile.id

    profile_to_edit = Profile.objects.get(pk=user_profile_id)

    sender_profile_to_edit = Profile.objects.get(pk=id)

    current_requests = profile_to_edit.requests
    current_requests_list = current_requests.split(sep=',')
    current_requests_list.remove(str(id))
    temp = current_requests_list
    temp = ",".join(temp)

    current_friends = profile_to_edit.friend_id_list

    if current_friends != None:
        current_friends_list = current_friends.split(sep=',')
        current_friends_list.append(str(id))

    else:
        current_friends_list = [str(id)]

    temp2 = current_friends_list
    temp2 = ",".join(temp2)

    sender_current_friends = sender_profile_to_edit.friend_id_list
    sender_current_pending = sender_profile_to_edit.pendings

    if sender_current_friends != None:
        sender_current_friends_list = sender_current_friends.split(sep=',')
        sender_current_friends_list.append(str(user_profile_id))
        temp3 = sender_current_friends_list
    else:
        temp3 = [str(user_profile_id)]

    temp3 = ','.join(temp3)

    ##################################

    if sender_current_pending != None:

        sender_current_pending_list = sender_current_pending.split(sep=',')
        if str(user_profile_id) in sender_current_pending_list:
            sender_current_pending_list.remove(str(user_profile_id))
            temp4 = sender_current_pending_list
            temp4 = ','.join(temp4)
    else:
        temp4 = None

    profile_to_edit.requests = temp
    profile_to_edit.friend_id_list = temp2
    sender_profile_to_edit.friend_id_list = temp3
    sender_profile_to_edit.pendings = temp4


    ########################accepts#####################

    sender_profile_to_edit_accepted = sender_profile_to_edit.accepted

    if sender_profile_to_edit_accepted != None:
        temp5 = sender_profile_to_edit_accepted.split(sep=',')
        temp5.append(str(user_profile_id))
        temp5 = ','.join(temp5)
    else:
        temp5 = str(user_profile_id)


    sender_profile_to_edit.accepted = temp5

    profile_to_edit.save()
    sender_profile_to_edit.save()

    messages.success(request,('Request Accepted!'))

    # determine where to redirect: homepage or recommendations

    current_url = url_id

    if current_url == '1':
        return redirect(f'/my_requests')
    else:
        return redirect(f'/my_recommendations/{user.id}')


def decline(request,id,url_id):

    user = request.user

    user_profile_id = user.profile.id

    profile_to_edit = Profile.objects.get(pk=user_profile_id)

    current_requests = profile_to_edit.requests

    current_requests_list = current_requests.split(sep=',')

    current_requests_list.remove(str(id))

    temp = current_requests_list

    temp = ",".join(temp)
    messages.success(request, ('Request Declined!'))

    sender_profile_to_edit = Profile.objects.get(pk=id)

    sender_current_pending = sender_profile_to_edit.pendings

    sender_current_pending_list = sender_current_pending.split(sep=',')

    sender_current_pending_list.remove(str(user_profile_id))

    temp4 = sender_current_pending_list

    temp4 = ','.join(temp4)

    profile_to_edit.requests = temp
    sender_profile_to_edit.pendings = temp4

    ########################declines#####################

    sender_profile_to_edit_declined = sender_profile_to_edit.declined

    if sender_profile_to_edit_declined != None:
        temp5 = sender_profile_to_edit_declined.split(sep=',')
        temp5.append(str(user_profile_id))
        temp5 = ','.join(temp5)
    else:
        temp5 = str(user_profile_id)

    sender_profile_to_edit.declined = temp5

    profile_to_edit.save()
    sender_profile_to_edit.save()

    # determine where to redirect: homepage or recommendations

    current_url = url_id

    if current_url == '1':
        return redirect(f'/my_requests')
    else:
        return redirect(f'/my_recommendations/{user.id}')


def test(request):

    return render(request, 'test.html', {

    })


def my_recommendations(request,id):

    logged_in_user_id = request.user.id

    if int(id) == logged_in_user_id:
        display = True
    else:
        display = False

    url_id = '2'

    url_id_b = '2'

    profiles = Profile.objects.all()

    user_profile = User.objects.get(pk=id)

    member_id_from_user = user_profile.profile.id

    member_instance = Profile.objects.get(pk=member_id_from_user)

    member_instance_friends = member_instance.friend_id_list

    requests_sent = member_instance.pendings

    people_who_already_sent_you_requests = member_instance.requests

    list_people_who_already_sent_you_requests = []

    if people_who_already_sent_you_requests != None and people_who_already_sent_you_requests != "":

        if people_who_already_sent_you_requests[0] == ',':
            people_who_already_sent_you_requests = people_who_already_sent_you_requests[1:]

        list_people_who_already_sent_you_requests = people_who_already_sent_you_requests.split(sep=',')
        list_people_who_already_sent_you_requests = list(map(int, list_people_who_already_sent_you_requests))


    final_list = []

    if member_instance_friends != None:

        list_member_instance_friends = member_instance_friends.split(sep=',')

        for profile in profiles:
            if str(profile.id) not in list_member_instance_friends:
                final_list.append(Profile.objects.get(pk=profile.id))


    else:

        for profile in profiles:
            final_list.append(Profile.objects.get(pk=profile.id))


    final_list.remove(member_instance)


    if requests_sent != None:


        list_requests_sent = requests_sent.split(sep=',')


        if list_requests_sent != [] and list_requests_sent != [""]:

            if list_requests_sent[0] == '':
                list_requests_sent = list_requests_sent[1:]
                member_instance.pendings = ','.join(list_requests_sent)
                member_instance.save()
                list_requests_sent = list(map(int, list_requests_sent))

            else:
                list_requests_sent = list(map(int,list_requests_sent))

        else:
            list_requests_sent = []
            list_requests_sent = list(map(int, list_requests_sent))

    else:

        list_requests_sent = []
        list_requests_sent = list(map(int, list_requests_sent))


    return render(request, 'my_recommendations.html', {

        'final_list': final_list,
        'list_requests_sent':list_requests_sent,
        "list_people_who_already_sent_you_requests":list_people_who_already_sent_you_requests,
        'url_id':url_id,
        'url_id_b':url_id_b,
        'id': id,
        'logged_in_user_id': logged_in_user_id,
        'display':display

    })


def home(request):

    user = request.user

    if user.is_authenticated:

        top_stories = find_trending()

        embed_code = russian_youtube()

        top_videos = most_watched()

        return render(request,'home.html',{

            'user':user,
            'top_stories':top_stories,
            'top_videos':top_videos,
            'unique_embed_code_for_number_one_video':'https://www.youtube.com/embed/'+embed_code

        })

    else:
        return redirect('login_user')

def my_profile(request,id):

    pics_show = False

    songs_show = False

    show = True

    entries = Picture.objects.all()

    entries_2 = Song.objects.all()

    user_1 = User.objects.get(pk=id)

    current_user = str(user_1).lower()

    logged_on_user = request.user

    logged_on_user_formatted = str(request.user.username).lower()

    member_id_from_user = user_1.profile.id

    member_instance = Profile.objects.get(pk=member_id_from_user)

    member_private = member_instance.private

    list_str_logged_on_user_friends = []


    if logged_on_user.username != current_user:

        if member_instance.private == True:

            str_logged_on_user_friends = logged_on_user.profile.friend_id_list

            if str_logged_on_user_friends != None:

                list_str_logged_on_user_friends = str_logged_on_user_friends.split(sep=',')

                if str(member_id_from_user) in list_str_logged_on_user_friends:
                    show = True

                else:
                    show = False

            else:
                show = False


    list_of_users_pics = []

    for entry in entries:
        if entry.author == current_user:
            list_of_users_pics.append(entry)

    if list_of_users_pics != []:
        pics_show = True


    ####################################################################################################

    # we need to extract info from list_of_users_pics

    list_whose_hearted_for_each_pic = []

    for entry in list_of_users_pics:

        if entry.hearted != None:
            temp = entry.hearted.split(sep=',')
        else:
            temp = ['']

        if temp != ['']:
            temp2 = list(map(int,temp))
        else:
            temp2 = []

        list_whose_hearted_for_each_pic.append([entry.id,temp2])
        # this is a list of: [int,[str,str,str,str]]...
        # it needs to be: [int,[int,int,int,int]]...

########################################################################################################################


    list_of_users_songs = []

    for entry in entries_2:
        if entry.author == current_user:
            list_of_users_songs.append(entry)

    if list_of_users_songs != []:

        #list_of_users_songs = list(map(lambda x:x.title.lower(),list_of_users_songs))
        songs_show = True


    return render(request, 'my_profile.html', {

        'show':show,
        'pics_show':pics_show,
        'songs_show':songs_show,
        'user_1': user_1,
        'member_id_from_user':member_id_from_user,
        'member_instance':member_instance,
        'list_of_users_pics':list_of_users_pics,
        'list_of_users_songs':list_of_users_songs,
        'current_user':current_user,
        'member_private':member_private,
        'list_str_logged_on_user_friends':list_str_logged_on_user_friends,
        'str_id':str(member_id_from_user),
        'logged_on_user':logged_on_user,
        'list_whose_hearted_for_each_pic':list_whose_hearted_for_each_pic,
        'logged_on_user_formatted':logged_on_user_formatted,
        'text': 'simon\njohn\nemily'




    })


def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:

            messages.success(request, (f'Successfully logged in. Welcome back, "{str(user).capitalize()}"!'))
            login(request, user)
            # change database entry here
            current_user = request.user
            current_user_id = current_user.profile.id
            current_profile = Profile.objects.get(pk=current_user_id)
            current_profile.online = True
            current_profile.save()
            return redirect("home")

        else:
            messages.success(request,('There was an error logging in!'))
            return redirect('login_user')

    else:
        return render(request,'login_user.html',{})


def logout_user(request):

    current_user = request.user
    current_user_cap = str(current_user).capitalize()

    logout(request)
    messages.success(request, (f'Successfully logged out. Bye, "{current_user_cap}"!'))
    current_user_id = current_user.profile.id
    current_profile = Profile.objects.get(pk=current_user_id)
    current_profile.online = False
    current_profile.save()
    return redirect("login_user")


def register(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            messages.success(request, (f'Successfully Registered. Welcome,{username}!'))
            user = authenticate(request, username=username, password=password)

            new_profile = Profile(member=user)
            new_profile.save()

            login(request,user)

            return redirect('home')

        else:

            messages.success(request, ('Error in form....'))
            return render(request, 'register.html', {

                'form': form,

            })


    else:

        form = SignUpForm()

        return render(request,'register.html',{

            'form':form,

        })


def edit_profile(request,id):

    user_profile = User.objects.get(pk=id)

    entries = Picture.objects.all()

    if request.method == 'POST':

        form = EditUserForm(request.POST or None, request.FILES or None,instance=user_profile)

        old_username = str(user_profile.username)

        if form.is_valid():

            form.save()

            username = str(form.cleaned_data['username'])

            for entry in entries:

                if entry.author == str(old_username).lower():
                    entry.author = str(username).lower()
                    entry.save()

            messages.success(request, (f"Updates successful!"))

            return redirect('home')


        else:

            messages.success(request, ('Error in form....'))
            return render(request, 'edit_profile.html', {

                'form': form,

            })


    else:

        username = request.user

        form = EditUserForm(instance=user_profile)

        return render(request, 'edit_profile.html', {

            'form': form,
            'username':username,
            'entries':entries,

        })


def add_pics(request):


    show_table = False

    total_loops = 0

    current_user = str(request.user).lower()

    entries = Picture.objects.all()

    if request.method == 'POST':

        form = PictureForm(request.POST,request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            #OVER HERE!#
            post.author = str(request.user).lower()
            post.connected_user = User.objects.get(username=str(request.user).lower())

            form.save()
            messages.success(request, ('Picture added!'))

            show_table = True

            form = PictureForm()

            return render(request, 'add_pics.html', {

                'form': form,
                'entries': entries,
                'current_user': current_user,
                'total_loops': total_loops,
                'show_table': show_table,


            })


        else:

            messages.success(request, ('Error adding picture!!!'))
            form = PictureForm()

            for entry in entries:
                if current_user == entry.author:
                    show_table = True
                    break

            return render(request, 'add_pics.html', {

                'form': form,
                'entries': entries,
                'current_user': current_user,
                'total_loops': total_loops,
                'show_table': show_table,


            })

    else:

        form = PictureForm()

        for entry in entries:
            if current_user == entry.author:
                show_table = True
                break

    return render(request, 'add_pics.html', {

        'form': form,
        'entries': entries,
        'current_user':current_user,
        'total_loops':total_loops,
        'show_table':show_table,


    })


def delete_pic(request,pic_id):

    pic = Picture.objects.get(pk=pic_id)
    pic.delete()
    messages.success(request, ('Image Deleted!'))

    return redirect("add_pics")

def delete_song(request,song_id):

    track = Song.objects.get(pk=song_id)
    track.delete()
    messages.success(request, ('Song Deleted!'))

    return redirect("add_song")


def delete_friend(request,friend_id):

    # should only be allowed if....

    current_user = Profile.objects.get(member=request.user)

    profile_instance_target = Profile.objects.get(pk=friend_id)

    temp_str = current_user.friend_id_list

    variant_1 = ','+friend_id
    variant_2 = ','+friend_id+','
    variant_3 = friend_id+','
    variant_4 = friend_id

    if variant_1 in current_user.friend_id_list:

        temp_str = temp_str.replace(variant_1,'')
        current_user.friend_id_list = temp_str
        current_user.save(update_fields=['friend_id_list'])
        messages.success(request,('Friend Deleted!'))


    elif variant_2 in current_user.friend_id_list:

        temp_str = temp_str.replace(variant_2,',')
        current_user.friend_id_list = temp_str
        current_user.save(update_fields=['friend_id_list'])
        messages.success(request, ('Friend Deleted!'))


    elif variant_3 in current_user.friend_id_list:

        temp_str = temp_str.replace(variant_3, '')
        current_user.friend_id_list = temp_str
        current_user.save(update_fields=['friend_id_list'])
        messages.success(request, ('Friend Deleted!'))

    elif variant_4 in current_user.friend_id_list:
        current_user.friend_id_list = ''
        current_user.save(update_fields=['friend_id_list'])
        messages.success(request, ('Friend Deleted!'))

    ############################################################################

    temp_str = profile_instance_target.friend_id_list

    variant_5 = ',' + str(current_user.id)
    variant_6 = ',' + str(current_user.id) + ','
    variant_7 = str(current_user.id) + ','
    variant_8 = str(current_user.id)

    if variant_5 in profile_instance_target.friend_id_list:

        temp_str = temp_str.replace(variant_5,'')
        profile_instance_target.friend_id_list = temp_str
        profile_instance_target.save(update_fields=['friend_id_list'])



    elif variant_6 in profile_instance_target.friend_id_list:

        temp_str = temp_str.replace(variant_6,',')
        profile_instance_target.friend_id_list = temp_str
        profile_instance_target.save(update_fields=['friend_id_list'])



    elif variant_7 in profile_instance_target.friend_id_list:

        temp_str = temp_str.replace(variant_7, '')
        profile_instance_target.friend_id_list = temp_str
        profile_instance_target.save(update_fields=['friend_id_list'])


    elif variant_8 in profile_instance_target.friend_id_list:
        profile_instance_target.friend_id_list = ''
        profile_instance_target.save(update_fields=['friend_id_list'])


    all_members = Profile.objects.all()

    member_id_from_user = current_user.id

    member_instance = Profile.objects.get(pk=member_id_from_user)

    member_instance_friends = member_instance.friend_id_list

    list_member_instance_friends = member_instance_friends.split(sep=',')

    final_list = []

    for member in all_members:
        if str(member.id) in list_member_instance_friends:
            final_list.append(Profile.objects.get(pk=member.id))



    return render(request, 'add_friend.html', {

        'all_members': all_members,
        'member_id_from_user': member_id_from_user,
        'list_member_instance_friends': list_member_instance_friends,
        'final_list': final_list,
        'display':True

    })





def edit_pic(request,pic_id):

    pic = Picture.objects.get(pk=pic_id)
    form = PictureForm(request.POST or None,request.FILES or None,instance=pic)

    if form.is_valid():
        post = form.save(commit=False)
        #OVER HERE!#
        post.author = str(request.user).lower()
        post.connected_user = User.objects.get(username=str(request.user).lower())
        form.save()
        messages.success(request, ('Image Updated!'))
        return redirect('add_pics')

    return render(request,'edit_pic.html',{

        'form':form,
    })


def edit_song(request,song_id):

    song = Song.objects.get(pk=song_id)
    form = SongForm(request.POST or None,request.FILES or None,instance=song)

    if form.is_valid():
        post = form.save(commit=False)
        #OVER HERE!#
        post.author = str(request.user).lower()
        post.connected_user = User.objects.get(username=str(request.user).lower())
        form.save()
        messages.success(request, ('Song Updated!'))
        return redirect('add_song')

    return render(request,'edit_song.html',{

        'form':form,
    })

def add_song(request):

    show_table = False

    total_loops = 0

    current_user = str(request.user).lower()

    entries = Song.objects.all()

    if request.method == 'POST':

        form = SongForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            #OVER HERE!#
            post.author = str(request.user).lower()
            post.connected_user = User.objects.get(username=str(request.user).lower())
            form.save()
            messages.success(request, ('Song added!'))

            show_table = True

            form = SongForm()

            return render(request, 'add_song.html', {

                'form': form,
                'entries': entries,
                'current_user': current_user,
                'total_loops': total_loops,
                'show_table': show_table,

            })


        else:

            messages.success(request, ('Error adding song!!!'))
            form = SongForm()

            for entry in entries:
                if current_user == entry.author:
                    show_table = True
                    break

            return render(request, 'add_song.html', {

                'form': form,
                'entries': entries,
                'current_user': current_user,
                'total_loops': total_loops,
                'show_table': show_table,

            })

    else:

        form = SongForm()

        for entry in entries:
            if current_user == entry.author:
                show_table = True
                break

    return render(request, 'add_song.html', {

        'form': form,
        'entries': entries,
        'current_user': current_user,
        'total_loops': total_loops,
        'show_table': show_table,

    })


def password(request):

    if request.method == 'POST':

        form = PasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            messages.success(request, ("Password successfully updated!"))

            return redirect('home')

        else:

            messages.success(request, ("Error in form..."))

            return render(request, 'password.html', {

                'form': form,

            })

    else:

        form = PasswordForm(request.user)

        return render(request, 'password.html', {

            'form': form,

        })


def edit_settings(request,id):

    user_profile = User.objects.get(pk=id)

    member_id_from_user = user_profile.profile.id

    member_instance = Profile.objects.get(pk=member_id_from_user)


    if request.method == 'POST':

        form = EditSettingsForm(request.POST,request.FILES or None,instance=member_instance)

        if form.is_valid():
            form.save()
            messages.success(request, ("Settings were successfully updated!"))
            return redirect('home')

        else:

            form = EditSettingsForm(instance=member_instance)

            messages.success(request, ('Error in form....'))
            return render(request, 'edit_settings.html', {

                'form': form,

            })

    else:

        form = EditSettingsForm(instance=member_instance)

        return render(request, 'edit_settings.html', {

            'form':form,

        })


def add_friend(request,id):

    logged_in_user_id = request.user.id

    if int(id) == logged_in_user_id:
        display = True
    else:
        display = False

    all_members = Profile.objects.all()

    user_profile = User.objects.get(pk=id)

    member_id_from_user = user_profile.profile.id

    member_instance = Profile.objects.get(pk=member_id_from_user)

    member_instance_friends = member_instance.friend_id_list

    final_list = []

    if member_instance_friends != None:

        list_member_instance_friends = member_instance_friends.split(sep=',')

        for member in all_members:
            if str(member.id) in list_member_instance_friends:
                final_list.append(Profile.objects.get(pk=member.id))


        return render(request,'add_friend.html',{

            'all_members': all_members,
            'id':id,
            'logged_in_user_id':logged_in_user_id,
            'display':display,
            'user_profile': user_profile,
            'member_id_from_user':member_id_from_user,
            'list_member_instance_friends':list_member_instance_friends,
            'final_list':final_list,


        })

    else:

        return render(request, 'add_friend.html', {

            'all_members': all_members,
            'display': display,
            'id': id,
            'logged_in_user_id': logged_in_user_id,
            'user_profile': user_profile,
            'member_id_from_user': member_id_from_user,

        })



def add_message(request,conversation_partner_2):

    current_user = request.user

    current_user_name = str(request.user)

    partner_profile = Profile.objects.get(pk=conversation_partner_2)

    conversation_partner_name = Profile.objects.get(pk=conversation_partner_2).member.username

    current_user_profile_id = current_user.profile.id

    all_conversation_items = Conversation.objects.all()

    exists = False

    for item in all_conversation_items:
        if (str(item.member_1) == current_user_name and str(item.member_2) == str(conversation_partner_name)) or (str(item.member_1) == str(conversation_partner_name) and str(item.member_2) == current_user_name):
            exists = True
            break

    #create a dummy dialogue just in case there is no existing conversation...
    if not exists:

        current_time = datetime.datetime.now()
        current_time_modified = current_time.strftime("[%H:%M %p]  --- [%d/%m/%Y]")
        current_user_name = current_user_name.upper()
        new_conversation_object = Conversation(member_1_id=current_user_profile_id,member_2_id=conversation_partner_2,dialogue=f"{current_user_name}: Hey!")
        new_conversation_object.save()
        exists = True

    try:

        entry = Conversation.objects.get(member_1=current_user_profile_id,member_2=conversation_partner_2)

    except:

        entry = Conversation.objects.get(member_1=conversation_partner_2,member_2=current_user_profile_id)


    return render(request, 'add_message.html', {

        #'form': form,
        #'profiles':profiles,
        'entry': entry,
        'current_user': current_user,
        'conversation_partner_2': conversation_partner_2,
        'conversation_partner_name':conversation_partner_name,
        'exists':exists,
        'all_conversation_items':all_conversation_items,
        'current_user_name':current_user_name,
        'partner_profile':partner_profile,
        'current_user_profile_id':current_user_profile_id,


    })

def getConversations(request):
    conversations = Conversation.objects.all()
    return JsonResponse({"conversations":list(conversations.values())})

def getUsers(request):

    all_profiles = Profile.objects.all()

    member_username_list = []

    for profile in all_profiles:

        member_username_list.append({'member_id':str(profile.id),'username':str(profile.member.username).lower(),'user_id':profile.member.id})

        #member_username_list.append({'member_id':str(profile.id),'username':profile.member.username})

    return JsonResponse({"all_profiles":member_username_list})

def getHelp(request):
    helps = Help.objects.all()
    return JsonResponse({"helps":list(helps.values())})

def getStatus(request):

    all_profiles = Profile.objects.all()

    status_list = []

    for profile in all_profiles:
        status_list.append({'member_id':str(profile.member.id),'online':profile.online})

    return JsonResponse({"all_profiles":status_list})

def getPictures(request):
    pictures = Picture.objects.all()
    logged_on_user_profile_id = request.user.profile.id
    logged_user_name = str(request.user.username.lower())
    return JsonResponse({"pictures":list(pictures.values()),"current_user":logged_on_user_profile_id,"username":logged_user_name})

def send_request(request,id,url_id_b):

    url_id_b = url_id_b

    user = request.user

    profile_sending_request = user.profile.id

    profile_sending_request_full = user.profile

    profile_to_send_request_to = Profile.objects.get(pk=id)

    if profile_sending_request_full.pendings != None:

        list_pendings = profile_sending_request_full.pendings.split(',')

        if str(profile_to_send_request_to.id) not in list_pendings:
            temp2 = profile_sending_request_full.pendings + ',' + str(profile_to_send_request_to.id)

        else:
            temp2 = profile_sending_request_full.pendings


        profile_sending_request_full.pendings = temp2
        profile_sending_request_full.save()



    elif profile_sending_request_full.pendings == None:

        temp2 = str(profile_to_send_request_to.id)


        profile_sending_request_full.pendings = temp2
        profile_sending_request_full.save()




    elif profile_sending_request_full.pendings == [""]:


        temp2 = str(profile_to_send_request_to.id)
        profile_sending_request_full.pendings = temp2
        profile_sending_request_full.save()





    if profile_to_send_request_to.requests != None:

        list_profile_to_send_request_to = profile_to_send_request_to.requests.split(',')

        if str(profile_sending_request) in list_profile_to_send_request_to:

            temp = profile_to_send_request_to.requests
        else:

            temp = profile_to_send_request_to.requests + ',' + str(profile_sending_request)

        profile_to_send_request_to.requests = temp
        profile_to_send_request_to.save()

        messages.success(request, ('Friend Request Sent!!!'))

        #coming from myrecommend page
        if url_id_b == '2':
            return redirect(f'/my_recommendations/{user.id}')

        #coming from search results page
        else:
            return redirect(f'/my_requests')

    else:

        temp = str(profile_sending_request)

        profile_to_send_request_to.requests = temp
        profile_to_send_request_to.save()

        messages.success(request,('Friend Request Sent!!!'))

        #coming from myrecommend page
        if url_id_b == '2':
            return redirect(f'/my_recommendations/{user.id}')

        #coming from search results page
        else:
            return redirect(f'/my_requests')


def CreateMessage2(request):

    if request.method == 'POST':

        message = request.POST['message']

        current_user = request.user

        help_to_update = Help.objects.get(user_asking_help=str(current_user.username).lower())

        if message != '':

            new_message_entry = '\n'+'\n'+ str(current_user.username).upper()+": "+message

            help_to_update.dialogue += new_message_entry

            help_to_update.save()


def CreateMessage(request):

    if request.method == 'POST':

        message = request.POST['message']
        partner = request.POST['partner']

        current_user = request.user

        current_user_profile_id = current_user.profile.id

        current_partner_id = int(partner)

        try:

            conversation_to_update = Conversation.objects.get(member_1=current_user_profile_id,member_2=current_partner_id)

        except:

            conversation_to_update = Conversation.objects.get(member_1=current_partner_id,member_2=current_user_profile_id)


        if message != '':

            current_time = datetime.datetime.now()

            current_time_modified = current_time.strftime("[%H:%M %p] --- [%d/%m/%Y]")

            new_message_entry = '\n'+'\n'+ str(current_user.username).upper()+": "+message

            conversation_to_update.dialogue += new_message_entry

            conversation_to_update.save()



def put_like(request):

    if request.method == 'POST':

        id = request.POST['userid']

        logged_in_user = str(request.user.username).lower()

        pic_we_need = Picture.objects.get(pk=id)

        author_of_pic_we_need = str(pic_we_need.author).lower()

        #########hearted stuff####################

        if pic_we_need.hearted == None:
            pic_we_need.hearted = ''

        if pic_we_need.hearted == '':
            pic_we_need.hearted = str(request.user.profile.id)
        else:
            pic_we_need.hearted += ',' + str(request.user.profile.id)

        if logged_in_user != author_of_pic_we_need:

            current_num_likes = int(pic_we_need.likes)

            num_likes = str(current_num_likes + 1)

            pic_we_need.likes = num_likes

        else:
            num_likes = 0

        pic_we_need.save()

        return HttpResponse(f"{num_likes}")


def filter_songs(request):

    if request.method == 'POST':

        song_query= request.POST['song_name']

        if song_query != '' or song_query != None:

            user_name = request.POST['user_name']

            user_name = user_name.lower()

            song_query = song_query.lower()

            # i wanna replace everything that isn't alphanumeric with null string???

            song_query = song_query.replace(' ','')

            all_songs = Song.objects.all()

            user_songs = []

            for song in all_songs:

                if str(song.author).lower() == user_name:
                    user_songs.append(song)

            filtered_song_list = []

            for song in user_songs:

                check_1 = str(song.title).lower().replace(' ','')
                check_2 = str(song.artist).lower().replace(' ','')

                match_object = re.search(song_query,check_1+check_2)
                match_object_2 = re.search(song_query, check_2+check_1)
                match_object_3 = re.search(check_1, song_query)
                match_object_4 = re.search(check_2, song_query)

                ready_text = f"<b>Title:</b><br>{song.title}<br><br><b>Artist:</b><br>{song.artist}<br><br><audio id='audio-player' controls='controls' src='{song.song_file.url}' style='width: 300px;' type='audio/mpeg'>"


                if match_object:

                    filtered_song_list.append([ready_text])

                elif match_object_2:

                    filtered_song_list.append([ready_text])

                elif match_object_3:

                    filtered_song_list.append([ready_text])

                elif match_object_4:

                    filtered_song_list.append([ready_text])

            return JsonResponse({"filtered_song_list":filtered_song_list})


        else:

            filtered_song_list = []

            return JsonResponse({"filtered_song_list":filtered_song_list})









def remove_like(request):

    if request.method == 'POST':

        id = request.POST['userid']

        logged_in_user = str(request.user.username).lower()

        pic_we_need = Picture.objects.get(pk=id)

        author_of_pic_we_need = str(pic_we_need.author).lower()

        ######### removing hearted stuff####################


        if len(pic_we_need.hearted) != 1:

            list_hearted = pic_we_need.hearted.split(sep=',')

            logged_in_user_profile_id = str(request.user.profile.id)

            list_hearted.remove(logged_in_user_profile_id)

            str_hearted = ','.join(list_hearted)

            pic_we_need.hearted = str_hearted

        else:

            pic_we_need.hearted = ''

        ###############################################################


        if logged_in_user != author_of_pic_we_need:

            current_num_likes = int(pic_we_need.likes)

            num_likes = str(current_num_likes - 1)

            pic_we_need.likes = num_likes

        else:
            num_likes = 0

        pic_we_need.save()

        return HttpResponse(f"{num_likes}")







def delete_dialogue(request,mem1,mem2):

    current_user = request.user

    current_user_name = current_user.username.upper()

    current_user_profile_id = current_user.profile.id

    current_time = datetime.datetime.now()

    current_time_modified = current_time.strftime("[%H:%M %p] --- [%d/%m/%Y]")

    try:

        conversation_to_update = Conversation.objects.get(member_1=mem1, member_2=mem2)

    except:

        conversation_to_update = Conversation.objects.get(member_1=mem2, member_2=mem1)


    conversation_to_update.dialogue = f"{current_user_name}: Hey! I refreshed our dialogue!"

    conversation_to_update.save()


    if mem1 == current_user_profile_id:
        needed_id = mem2
    else:
        needed_id = mem1

    return redirect(f'/add_message/{needed_id}')


























































