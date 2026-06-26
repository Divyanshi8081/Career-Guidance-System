from django.contrib import admin
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['role', 'content', 'timestamp']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'message_count', 'created_at']
    inlines = [ChatMessageInline]
