from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('voter', 'Voter'),
        ('candidate', 'Candidate'),
    )

    voter_id = models.CharField(
        max_length=30,
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='voter'
    )

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'voter_id']

    def __str__(self):
        return self.email





