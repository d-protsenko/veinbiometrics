from django import forms


class AddImageForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField(label='Your image name', max_length=100)

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)
