from django.contrib import admin
from .models import User, Collection, Movie, RequestCounter


# Register your models here.

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("uuid", "title", "description", "user")

@admin.register(RequestCounter)
class RequestCounterAdmin(admin.ModelAdmin):
    list_display = ("id", "no_of_request", "last_update")


admin.site.register(User)
admin.site.register(Movie)
