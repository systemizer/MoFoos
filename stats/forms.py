from django import forms
from foos.main.models import UserProfile
from foos.stats.models import Comment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude=("user","update","created","deleted")
