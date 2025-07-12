from django.contrib import admin

from chat.models import ChatMessage


# Register your models here.
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'timestamp')
    search_fields = ('sender__username', 'message')
    ordering = ('-timestamp',)