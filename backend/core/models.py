from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class RewriteHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rewrites")
    original_text = models.TextField()
    rewritten_text = models.TextField()
    tone = models.CharField(max_length=50, default="formal")
    language = models.CharField(max_length=50, default="english")  # 👈 NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rewrite by {self.user.username} on {self.created_at}"


