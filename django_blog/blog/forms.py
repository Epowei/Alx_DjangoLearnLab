from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from .models import Post, Comment
from taggit.models import Tag
from django.utils.safestring import mark_safe

class TagWidget():
    """
    Custom widget for rendering a more user-friendly tag input field.
    Adds a list of popular tags below the input for easy selection.
    """
    def render(self, name, value, attrs=None, renderer=None):
        # First render the standard TextInput
        html = super().render(name, value, attrs, renderer)
        
        # Get the 10 most commonly used tags
        common_tags = Tag.objects.all().order_by('name')[:10]
        
        if common_tags:
            # Add a list of popular tags that can be clicked
            html += '<div class="tag-suggestions">'
            html += '<p class="tag-suggestions-title">Popular tags:</p>'
            html += '<div class="tag-suggestions-list">'
            
            for tag in common_tags:
                html += f'<span class="tag-suggestion" data-tag="{tag.name}">{tag.name}</span>'
            
            html += '</div></div>'
            
            # Add JavaScript to make the tags clickable and add them to the input
            html += '''
            <script type="text/javascript">
                document.addEventListener('DOMContentLoaded', function() {
                    var tagInput = document.getElementById("id_tags_input");
                    var suggestions = document.querySelectorAll(".tag-suggestion");
                    
                    suggestions.forEach(function(tag) {
                        tag.addEventListener("click", function() {
                            var tagName = this.getAttribute("data-tag");
                            var currentValue = tagInput.value.trim();
                            
                            if (currentValue) {
                                // Check if tag is already in the input
                                var tags = currentValue.split(",").map(t => t.trim());
                                if (!tags.includes(tagName)) {
                                    tagInput.value = currentValue + ", " + tagName;
                                }
                            } else {
                                tagInput.value = tagName;
                            }
                            
                            // Focus the input after adding a tag
                            tagInput.focus();
                        });
                    });
                });
            </script>
            <style>
                .tag-suggestions {
                    margin-top: 8px;
                }
                .tag-suggestions-title {
                    font-size: 0.85em;
                    color: #666;
                    margin-bottom: 5px;
                }
                .tag-suggestions-list {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 5px;
                }
                .tag-suggestion {
                    display: inline-block;
                    background-color: #f0f0f0;
                    color: #444;
                    padding: 3px 8px;
                    border-radius: 12px;
                    font-size: 0.85em;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                .tag-suggestion:hover {
                    background-color: #e0e0e0;
                }
            </style>
            '''
        
        return mark_safe(html)

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
        widget=TagWidget(attrs={'placeholder': 'tag1, tag2, tag3', 'class': 'form-control'}),
        help_text='Click on a tag below to add it, or type your own tags separated by commas'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags_input']
    
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
