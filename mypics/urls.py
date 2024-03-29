from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login_user',views.login_user,name='login_user'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('register',views.register,name='register'),
    path('add_pics',views.add_pics,name='add_pics'),
    path('delete_pic/<pic_id>',views.delete_pic,name='delete_pic'),
    path('delete_song/<song_id>',views.delete_song,name='delete_song'),
    path('delete_friend/<friend_id>',views.delete_friend,name='delete_friend'),
    path('edit_pic/<pic_id>',views.edit_pic,name='edit_pic'),
    path('edit_song/<song_id>',views.edit_song,name='edit_song'),
    path('add_friend/<id>',views.add_friend,name='add_friend'),
    path('add_message/<conversation_partner_2>',views.add_message,name='add_message'),
    path('add_song',views.add_song,name='add_song'),
    path('my_profile/<id>',views.my_profile,name='my_profile'),
    path('edit_profile/<id>', views.edit_profile, name='edit_profile'),
    path('password/', views.password, name='password'),
    path('edit_settings/<id>', views.edit_settings, name='edit_settings'),
    path('my_recommendations/<id>', views.my_recommendations, name='my_recommendations'),
    path('my_requests', views.my_requests, name='my_requests'),
    path('send_request/<id>/<url_id_b>', views.send_request, name='send_request'),
    path('accept/<id>/<url_id>/', views.accept, name='accept'),
    path('decline/<id>/<url_id>/', views.decline, name='decline'),
    path('test', views.test, name='test'),
    path('getConversations', views.getConversations, name='getConversations'),
    path('getPictures', views.getPictures, name='getPictures'),
    path('getStatus', views.getStatus, name='getStatus'),
    path('getHelp', views.getHelp, name='getHelp'),
    path('getUsers', views.getUsers, name='getUsers'),
    path('create_message', views.CreateMessage, name='CreateMessage'),
    path('create_message2', views.CreateMessage2, name='CreateMessage2'),
    path('delete_dialogue/<mem1>/<mem2>', views.delete_dialogue, name='delete_dialogue'),
    path('put_like', views.put_like, name='put_like'),
    path('remove_like', views.remove_like, name='remove_like'),
    path('filter_songs', views.filter_songs, name='filter_songs'),
    path('filter_friends', views.filter_friends, name='filter_friends'),
    path('filter_pics', views.filter_pics, name='filter_pics'),
    path('delete_account/<user_id>', views.delete_account, name='delete_account'),
    path('search', views.search, name='search'),
    path('report', views.report, name='report'),
    path('help', views.help, name='help'),
    path('critique', views.critique, name='critique'),

]