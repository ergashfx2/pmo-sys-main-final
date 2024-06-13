from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .models import User
from hodimlar.models import Department, Blog


class CreateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Username kiriting')
    first_name = forms.CharField(max_length=150, label='Ism kiriting')
    last_name = forms.CharField(max_length=150, label='Familiya kiriting')
    phone = forms.CharField(max_length=150, label='Telefon raqam kiriting')
    email = forms.EmailField(label='Email kiriting')
    role = forms.ChoiceField(
        label="Foydalanuvchi ro'lini tanlang",
        choices={
            'Admin': 'Admin',
            'Loyiha menejeri': "Loyiha menejeri",
            'Loyiha egasi': "Loyiha egasi",
            'Loyiha kuratori': 'Loyiha kuratori',
            'O)ddiy': "Oddiy foydalanuvchi"
        },
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    position = forms.CharField(label='Lavozimini tanlang', max_length=150)
    blogs = {blog.blog_name: blog.blog_name for blog in Blog.objects.all()}
    departments = {department.department_name: department.department_name for department in Department.objects.all()}
    blog = forms.ChoiceField(
        label='Blokni tanlang',
        choices=blogs.items(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    department = forms.ChoiceField(
        label='Departamentni tanlang',
        choices=departments.items(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(label="Rasm yuklang", max_length=150, required=False)
    password = forms.CharField(
        label='Parolni kiriting',
        max_length=150,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'type': 'password'})
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'first_name', 'last_name', 'phone', 'email', 'role', 'position', 'department', 'blog', 'image', 'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if self.cleaned_data.get('image'):
            user.avatar = self.cleaned_data['image']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=150,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol'}))


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'position', 'role', 'blog', 'department',
                  'phone']
