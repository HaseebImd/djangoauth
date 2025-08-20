from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class RolePermission(models.Model):
    name = models.CharField(max_length=30)
    name_value = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=30)
    permissions = models.ManyToManyField(
        RolePermission, related_name="roles", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)


class CustomUser(AbstractUser):
    username = None  # Disable username field
    email = models.EmailField(unique=True)  # Use email as unique identifier
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, blank=True, null=True
    )
    role = models.ManyToManyField(Role, related_name="users", blank=True)

    groups = None
    user_permissions = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No required fields other than email
    objects = CustomUserManager()

    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role by name."""
        return self.role.filter(name=role_name).exists()

    def has_permission(self, permission_name: str) -> bool:
        """Check if user has a specific permission by name_value."""
        return self.role.filter(permissions__name_value=permission_name).exists()

    def get_all_permissions(self):
        """Return list of all permission name_values for the user."""
        return list(
            self.role.values_list("permissions__name_value", flat=True).distinct()
        )

    """
    user = CustomUser.objects.get(email="admin@example.com")

    if user.has_role("Admin"):
        print("✅ User is admin")

    if user.has_permission("payrolls"):
        print("✅ User can access payrolls")

    print(user.get_all_permissions())  
    # ['clients', 'payrolls', 'hst']

    """
