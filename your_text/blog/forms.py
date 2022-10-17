from django.forms import ModelForm
from .models import UserPost


class CreatePost(ModelForm):
    class Meta:
        model = UserPost
        fields = ('image', 'title', 'content')

    def __init__(self, *args, **kwargs):
        super(CreatePost, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field_name