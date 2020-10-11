from django import forms
from .models import File
from .models import Room

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('comment','ppt')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('limit', 'room_name')
