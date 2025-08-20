
# Django Authentication, Roles & Permissions — In-Depth Notes

This document consolidates all concepts we discussed, written as a **complete study & reference guide**.  
Everything is structured step by step for easy revision.

---

## 1. Roles & Permissions in Django

### Built-in System
- Django comes with a **built-in permission system**:
  - **Permissions** are tied to models (add, change, delete, view).
  - **Groups** are collections of permissions → used to simulate *roles*.
  - Example:  
    - `Admin` group → full CRUD permissions.  
    - `Editor` group → add/change, but no delete.  
    - `Viewer` group → view only.  

### Custom Roles
- For more flexibility, projects often define **custom roles** on top of Groups.  
- Implementation approaches:
  - Extend `AbstractUser` or `AbstractBaseUser`.
  - Add a `role` field (`choices` like `ADMIN`, `STAFF`, `CUSTOMER`).
  - Map each role to a set of permissions.
  - Optionally, integrate **Groups** with custom role logic.

👉 **Real Projects:**  
- For **small/medium projects** → Built-in Groups + Permissions are enough.  
- For **enterprise projects** → Often a **custom role model** is introduced for fine-grained control.

---

## 2. Signals (Brief Recap)

- Django provides **signals** to react to model/user events.
- Example: Automatically assign default role/group when a user is created.

```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name="Viewer")
        instance.groups.add(group)
````

📌 Use `signals` when you want **automation** (e.g., assigning groups, logging actions).
But keep in mind — avoid overusing signals for core business logic → prefer services/explicit calls.

---

## 3. `django.contrib.auth.models` Deep Dive

This is the core of Django’s **authentication framework**.

### 3.1 `AbstractUser`

* Subclass of `AbstractBaseUser` + `PermissionsMixin`.
* Provides:

  * `username`, `email`, `first_name`, `last_name`, `is_staff`, `is_active`.
* Easiest way to extend user model:

  ```python
  from django.contrib.auth.models import AbstractUser

  class CustomUser(AbstractUser):
      phone_number = models.CharField(max_length=20, blank=True, null=True)
  ```
* ✅ Recommended if you just need to **add fields**.

---

### 3.2 `AbstractBaseUser`

* The **lowest-level class** for custom users.
* Provides only:

  * `password`, `last_login`, `is_active`.
* Requires implementing:

  * `USERNAME_FIELD`
  * `objects` → must use custom manager (`BaseUserManager`)
  * `__str__`, `get_full_name`, etc.
* ✅ Use when you want **complete control** (e.g., login with phone instead of username).

---

### 3.3 `PermissionsMixin`

* Provides:

  * `groups` (ManyToMany to Group).
  * `user_permissions` (ManyToMany to Permission).
  * Helper methods like `has_perm`, `has_module_perms`.
* Usually combined with `AbstractBaseUser`.

---

### 3.4 `BaseUserManager`

* Helps create users & superusers when using custom user models.
* Example:

  ```python
  from django.contrib.auth.models import BaseUserManager

  class CustomUserManager(BaseUserManager):
      def create_user(self, email, password=None, **extra_fields):
          if not email:
              raise ValueError("Users must have an email")
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_fields)
          user.set_password(password)
          user.save(using=self._db)
          return user

      def create_superuser(self, email, password=None, **extra_fields):
          extra_fields.setdefault("is_staff", True)
          extra_fields.setdefault("is_superuser", True)
          return self.create_user(email, password, **extra_fields)
  ```

---

### 3.5 `UserManager`

* The **default manager** for Django’s built-in `User` model.
* Extends `BaseUserManager`.
* Provides `create_user` and `create_superuser`.

---

### 3.6 `AnonymousUser`

* Represents a user who is not authenticated.
* Always returned by `request.user` if the user is not logged in.
* Properties:

  * `is_authenticated = False`
  * `is_anonymous = True`
* Useful in permission checks:

  ```python
  if request.user.is_authenticated:
      ...
  else:
      ...
  ```

---

## 4. Visual Diagram — Relationships

```
AbstractBaseUser
     │
     └── PermissionsMixin (adds groups, permissions)
             │
             └── AbstractUser (ready-to-use base model)
                      │
                      └── User (default Django user model)
```

* `BaseUserManager` → Used with `AbstractBaseUser`.
* `UserManager` → Default manager for `User`.
* `AnonymousUser` → Used for non-logged-in users.

---

## 5. Practical Notes

* **When to use `AbstractUser`:**
  Need username/email login but want to add extra fields.

* **When to use `AbstractBaseUser`:**
  Need a fully customized authentication system (e.g., login by phone).

* **Permissions in real apps:**

  * Small apps → Built-in Groups + Permissions.
  * Enterprise apps → Custom Role model + PermissionsMixin.

* **AnonymousUser:** Always check `.is_authenticated` before accessing sensitive info.

---

## 6. Summary

* Django has a **flexible authentication system**.
* For most projects → `AbstractUser` + Groups + Permissions is enough.
* For special cases → `AbstractBaseUser` + PermissionsMixin + BaseUserManager.
* Roles = Groups (built-in) OR custom Role model (enterprise).
* Signals are helpful for automations (assign groups, logging).
* Always plan user model early → changing it later is painful.

