from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import get_user_model

User=get_user_model()

@receiver(social_account_added)
def assign_role(request,sociallogin,**kwargs):
    user=sociallogin.user
    if hasattr(user,'user_role'):
       if user.user_role!='librarian':
           user.user_role='patron'
           user.save()
           
    else:
        user.user_role='patron'
    request.session.pop('user_role',None)