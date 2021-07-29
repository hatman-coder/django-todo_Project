from django.forms import ModelForm
from todoApp.models import todoModel

class TodoForm(ModelForm):
    class Meta():
        model = todoModel
        fields = ['title', 'memo','important']
