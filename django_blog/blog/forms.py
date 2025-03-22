from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from .models import Post, Comment
from taggit.models import Tag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        # Convert to lowercase for consistency
        return name.lower()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if commit:
            instance.save()
        return instance

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        label='Tags (comma separated)',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_input']
        widgets = {
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tags separated by commas'
            }),
        }
        help_texts = {
            'tags': 'Enter tags separated by commas (e.g., django, python, web-dev)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # If editing an existing post, pre-populate the tags field
            self.initial['tags_input'] = ', '.join(tag.name for tag in self.instance.tags.all())
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Clear existing tags
            instance.tags.clear()
            
            # Process the tags input
            if self.cleaned_data['tags_input']:
                tag_names = [name.strip().lower() for name in self.cleaned_data['tags_input'].split(',') if name.strip()]
                
                for tag_name in tag_names:
                    # Get or create the tag
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': slugify(tag_name)}
                    )
                    instance.tags.add(tag)
                    
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
        labels = {
            'content': '',  # Hide the label
        }