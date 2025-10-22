
from django import forms
from .models import Event, Category

class StyledMixin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            base_class = 'mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 text-gray-200 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                pass
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': base_class, 'rows': 4})
            else:
                 field.widget.attrs.update({'class': base_class})

class EventForm(StyledMixin):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category' , 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class CategoryForm(StyledMixin):
    class Meta:
        model = Category
        fields = ['name', 'description']