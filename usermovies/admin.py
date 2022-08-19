from django.contrib import admin
from .models import User, Collection, Movie

# Register your models here.
admin.site.register(User)
admin.site.register(Collection)
admin.site.register(Movie)
