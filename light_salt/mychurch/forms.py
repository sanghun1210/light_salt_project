from django import forms
from .models import LSCH004M, LSCH005D

def min_length_2_validator(value):
    if len(value) < 2:
        raise forms.ValidationError('2글자 이상 입력해주세요')
	
class BoardForm(forms.Form):
    subject = forms.CharField(validators=[min_length_2_validator], widget=forms.TextInput(attrs={'size':'50'}))
    content = forms.CharField(validators=[min_length_2_validator], widget=forms.Textarea(attrs={'id':'lightsalt'}))
    password = forms.CharField(widget=forms.PasswordInput(), required = False)
    board_no = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField(widget=forms.HiddenInput())
    #file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required = False)

    class Meta:
        model = LSCH004M

    def __init__(self, request, *args, **kwargs):
        self.file_attach_yn = kwargs.pop('file_attach_yn',None)
        if self.file_attach_yn == 'Y':
            self.fields['file_field'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required = False)
        super(BoardForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, group_order=1, group_no=1, depth=0):
        content = LSCH004M(**self.cleaned_data)
        content.group_order = group_order
        content.group_no = group_no
        content.depth = depth
        #post = LSCH004M(**self.cleaned_data)
        if commit:
            content.save()
        return content
