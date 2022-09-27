from django.contrib import admin
from django.utils.html import format_html

from .models import Picture,Profile,Song,Conversation,Query,Critique,Help

#admin.site.register(Picture)
admin.site.register(Profile)
#admin.site.register(Song)
admin.site.register(Conversation)
admin.site.register(Query)
admin.site.register(Critique)
admin.site.register(Help)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):

    list_display = ('author','title','pic_preview')
    ordering = ('-author',)
    search_fields = ('author','title')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('author', 'title','artist')
    ordering = ('-author',)
    search_fields = ('author', 'title')







