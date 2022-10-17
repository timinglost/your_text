from django.forms import ModelForm, PasswordInput, CharField
from django import forms
from auth_app.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field_name


class UserPasswordEditForm(PasswordChangeForm):
    old_password = CharField(required=True, label='Старый пароль', widget=PasswordInput(
        attrs={'class': 'form-control'}),
                             error_messages={'required': 'Неверно введен пароль.'})

    new_password1 = CharField(required=True, label='Новый пароль',
                              widget=PasswordInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  'required': 'Пароль не соответствует стандартам. Используйте цифры и латинские буквы разных регистров.'})
    new_password2 = CharField(required=True, label='Повторите новый пароль',
                              widget=PasswordInput(attrs={'class': 'form-control'}),
                              error_messages={
                                  'required': 'Пароли не совпадают. Попробуйте еще раз'})

    def clean_new_password2(self):

        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    'Пароли не совпадают! '
                    'Пожалуйста введите новый пароль и повторите его для подтверждения.'
                )
        return password2

    def __init__(self, *args, **kwargs):
        super(UserPasswordEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
