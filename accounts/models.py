from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Custom manager for User model
class UserManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")

        # Create a new user instance
        user = self.model(
            email=self.normalize_email(email),  # Normalize the email (lowercase domain)
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)  # Hash the password
        user.save(using=self._db)  # Save the user instance
        return user

    # Method to create a superuser (admin)
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Set admin-related fields
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user


# Custom User model
class User(AbstractBaseUser):
    # User roles
    RESTAURANT = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (RESTAURANT, "Restaurant"),
        (CUSTOMER, "Customer"),
    )

    # User fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=13, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # Automatically managed timestamp fields
    date_joined = models.DateTimeField(
        auto_now_add=True
    )  # Set once when user is created
    last_login = models.DateTimeField(auto_now_add=True)  # Updated when user logs in
    created_date = models.DateTimeField(auto_now_add=True)  # Set at creation
    modified_date = models.DateTimeField(auto_now=True)  # Updated on each save

    # Permissions-related fields
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Determines access to Django admin
    is_active = models.BooleanField(default=False)  # Whether user account is active
    is_superadmin = models.BooleanField(default=False)  # Super admin flag

    # Field used for authentication (instead of default username)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]  # Required when creating a superuser

    objects = UserManager()  # Attach custom manager

    def __str__(self):
        return self.email  # Display email when printing user instance

    # Method to check if user has a specific permission
    def has_perm(self, perm, obj=None):
        return self.is_admin  # Admins have all permissions

    # Method to check if user has permission to access a specific module
    def has_module_perms(self, app_label):
        return True  # Allows access to any app


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile"
    )
    profile_picture = models.ImageField(
        upload_to="users/profile_pictures", blank=True, null=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photos", blank=True, null=True
    )
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    state = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True, db_index=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.email