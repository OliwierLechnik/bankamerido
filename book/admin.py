from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('id', 'sender_id', 'receiver_id', 'type', 'title', 'value', 'date')