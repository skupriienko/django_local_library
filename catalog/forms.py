import datetime
from django import forms
from django.forms import ModelForm  # Helper class to create forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from catalog.models import BookInstance


# Base class to create forms
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter date in between 4 weeks (default 3).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if data is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid data - renewal in past'))

        # Check if data in the allowed range (+4 weeks from today)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid data - renewal data more than 4 weeks ahead'))

        # Remember to always return cleaned data.
        return data


# Helper class to create forms (as RenewBookForm above)
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('New renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
