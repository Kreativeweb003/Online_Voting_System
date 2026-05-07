from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ('voter', 'Voter'),
        ('candidate', 'Candidate'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    voter_id = models.CharField(max_length=25, unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
        







