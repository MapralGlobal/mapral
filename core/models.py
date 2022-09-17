from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, True, True, **extra_fields)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255, blank=True, null=True)
    lname = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=255,blank=True, null=True)
    gender = models.CharField(max_length=255,blank=True, null=True)
    company = models.CharField(max_length=255,blank=True, null=True)
    aboutCompany = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=255,blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=255, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


# Create your models here.
STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    # content = RichTextField()
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS, default=0)
    slug = models.CharField(max_length=255, blank=True,
                            null=True, unique=True, editable=True)

    def save(self, *args, **kwargs):
        self.slug = (self.title.replace(" ", "-"))+"-" + \
            str(uuid4())+(self.author.replace(" ", "-"))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Resume(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    phone = models.CharField(max_length=255,blank=True, null=True)
    jobTitle = models.CharField(max_length=255,blank=True, null=True)
    aboutWork = models.TextField(blank=True, null=True)
    skills = models.CharField(max_length=255,blank=True, null=True)
    # profilePic = models.ImageField(upload_to='core/images/', blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    languages = models.CharField(max_length=255,blank=True, null=True)
    
    def __str__(self):
        return self.name

class Education(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schoolName = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    startDate = models.CharField(max_length=255)

    def __str__(self):
        return self.schoolName
    
class Experience(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=255)
    jobPosition = models.CharField(max_length=255)
    jobDescription = models.TextField()
    responsibilities = models.TextField()
    startDate = models.CharField(max_length=255)

    def __str__(self):
        return self.companyName

class JobNotifications(models.Model):
    id = models.AutoField(primary_key=True)
    jobTitle = models.CharField(max_length=255)
    dateAdded = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.jobTitle

class JobReceived(models.Model):
    id = models.AutoField(primary_key=True)
    jobTitle = models.CharField(max_length=255)
    dateAdded = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.jobTitle

    