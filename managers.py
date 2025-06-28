from django.contrib.auth.base_user import BaseUserManager


class UserLoginManager(BaseUserManager):
    def create_user(self, user_login_id, password, **extra_feilds):
        if not user_login_id:
            raise ValueError("user_login_id must be given.")

        user = self.model(user_login_id=user_login_id, **extra_feilds)
        user.ul_user_id = user.create_user_master()
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_login_id, password, **extras):
        extras.setdefault("is_staff", True)
        extras.setdefault("is_active", True)
        extras.setdefault("is_superuser", True)

        if extras.get("is_staff") is not True:
            raise ValueError("Super user must have is_staff=True")

        if extras.get("is_active") is not True:
            raise ValueError("Super user must have is_active=True")

        self.create_user(user_login_id, password, **extras)