from django import forms
from .models import Push

FIELDS = ['title', 'image', 'category', 'quantity', 'unit', 'description', 'user']


class PushForm(forms.ModelForm):
    request = None  # set by FormView.get_form()
     
    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        #self.request = request

    def is_valid(self):
        import pdb; pdb.set_trace()  # <---------
        return forms.ModelForm.is_valid(self)

    class Meta:
        model = Push
        fields = FIELDS
