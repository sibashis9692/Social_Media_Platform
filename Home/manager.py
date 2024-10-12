from django.contrib.auth.models import BaseUserManager

class userManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        if(email is None):
            return ValueError({"Error" : "Email can not be Null"})
        
        email = self.normalize_email(email)

        user = self.model(username = username, email = email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
