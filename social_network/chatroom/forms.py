
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'file']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type a message...'}),
        }
