from django import forms


class AddImageForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField(label='Your image name', max_length=100)
    lower_thresh = forms.IntegerField(min_value=0, max_value=255)
    upper_thresh = forms.IntegerField(min_value=0, max_value=255)

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)
