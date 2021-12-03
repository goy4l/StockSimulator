from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class SignUpForm(UserCreationForm):  
        class Meta:  
            model = User  
            fields = ('email', 'first_name', 'last_name', 'username')


class leagueuserauth(ModelForm):
    class Meta:
        model = league
        fields = ['game_code']

    
class transactionadder(ModelForm):
    class Meta:
        model = transaction
        fields = ['ttype','stock','quantity']
    def __init__(self,user, *args, **kwargs):
        super(transactionadder, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['ttype'].label = 'Transaction Type'
        self.fields['stock'].queryset = stocks.objects.filter(league=user)
        self.fields['stock'].label_from_instance = lambda obj: "%s" % (obj.name)


class transfermaker(ModelForm):
    class Meta:
        model = transfer
        fields = ['stock','quantity','from_user']
    def __init__(self,user, *args, **kwargs):
        super(transfermaker, self).__init__(*args, **kwargs)
        # without the next line label_from_instance does NOT work
        self.fields['stock'].queryset = stocks.objects.filter(league=user.lauth.league)
        self.fields['stock'].label_from_instance = lambda obj: "%s" % (obj.name)
        self.fields['from_user'].queryset = league.objects.get(id=user.lauth.league.id).users.all().exclude(id=user.id)
