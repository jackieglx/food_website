from django import forms

from accounts.models import User, UserProfile
from accounts.validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    # def clean(self): 方法会在表单的 is_valid() 方法被调用时自动执行
    def clean(self):
        # 调用父类的 clean 方法，并获取已经清理和验证过的表单数据
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[allow_only_images_validator]
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'btn btn-info'}),
        validators=[allow_only_images_validator]
    )

    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city',
                  'pin_code', 'latitude',
                  'longitude']

    # 在 UserProfileForm 类中的 __init__ 方法是用来初始化表单的。当你创建表单实例时，这个方法会被自动调用
    # 对于每一个字段，如果字段的名字是 'latitude' 或 'longitude'，就会将这些字段的显示属性设置为只读 (readonly)。这意味着用户不能直接编辑这些字段的内容。
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
