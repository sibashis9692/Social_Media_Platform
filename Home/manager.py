from django.contrib.auth.models import BaseUserManager

class userManager(BaseUserManager):

    def create_user(self, username, email, password, *extra_fields):
        if(email is None):
            return ValueError({"Error" : "Email can not be Null"})
        
        email = self.normalize_email(email)

        user = self.model(username = username, email = email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is None:
            return ValueError({"Error" : "Superuser must have is_staff = True"})
        if extra_fields.get('is_admin') is None:
            return ValueError({"Error" : "Superuser must have is_admin = True"})
        if extra_fields.get('is_active') is None:
            return ValueError({"Error" : "Superuser must have is_active = True"})

        return self.create_user(username, email, password, **extra_fields)