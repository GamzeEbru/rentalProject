from django import forms

from iha.models import IHA, Kiralama
from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This User doesnot Exist or Incorrect Password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='E-Posta')
    password = forms.CharField(label='Parola', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parola Doğrulama', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Şifreler uyuşmuyor.')

        return password2

class IHAEkleForm(forms.ModelForm):
    class Meta:
        model = IHA  # Form, IHA modeline dayanacak
        fields = '__all__'  # Tüm model alanlarını kullanın

    # Opsiyonel olarak save yöntemini tanımlayabilirsiniz
    def save(self, commit=True):
        iha = super(IHAEkleForm, self).save(commit=False)
        # Burada formdan gelen verileri işleyebilirsiniz, örneğin bazı alanları değiştirebilirsiniz.
        if commit:
            iha.save()
        return iha


class IHAEditForm(forms.ModelForm):
    class Meta:
        model = IHA
        exclude = ['id']  # ID alanını dışarıda bırak


# Kiralama crud işlemleri için
class KiralamaForm(forms.ModelForm):
    class Meta:
        model = Kiralama
        fields = '__all__'  # Tüm alanları


class KiralamaUpdateForm(forms.ModelForm):
    class Meta:
        model = Kiralama
        fields = ['kiralama_baslangic', 'kiralama_bitis']
