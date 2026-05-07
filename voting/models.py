from django.db import models
from accounts.models import User


# -------------------------
# ELECTION MODEL
# -------------------------
class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# -------------------------
# CANDIDATE APPLICATION
# -------------------------
class CandidateApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    position = models.CharField(max_length=100)

    manifesto = models.TextField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.email} - {self.election.title}"


# -------------------------
# VOTE MODEL
# -------------------------
class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidate_votes")
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election')  # prevents double voting

    def __str__(self):
        return f"{self.voter.email} voted for {self.candidate.email}"