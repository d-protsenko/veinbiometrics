from django import forms


class AddImageForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'custom-file-input',
            }
        )
    )
    name = forms.CharField(
        label='Your biometric name',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    lower_thresh = forms.IntegerField(
        min_value=0,
        max_value=255,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': 170,
            }
        )
    )
    upper_thresh = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': 255,
                'readonly': True,
            }
        )
    )
    denoise_lvl = forms.IntegerField(
        min_value=0,
        max_value=8,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': 4,
            }
        )
    )
    clahe_lvl = forms.IntegerField(
        min_value=0,
        max_value=8,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': 4,
            }
        )
    )
    gauss_block_size = forms.IntegerField(
        min_value=1,
        max_value=41,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': 27,
            }
        )
    )
    gauss_constant = forms.IntegerField(
        min_value=-40,
        max_value=40,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'value': 8,
            }
        )
    )
    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)
