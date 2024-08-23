from django.contrib import admin
from .models import Book, Subscription, CreativeWork, BookIssue, Genre

# Registering models without custom admin classes
admin.site.register(Book)
admin.site.register(Subscription)
admin.site.register(CreativeWork)
admin.site.register(BookIssue)

# Customizing Genre display with GenreAdmin
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Registering the Genre model with the GenreAdmin class
admin.site.register(Genre, GenreAdmin)
