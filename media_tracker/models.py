import uuid
from django.db import models

class Media(models.Model):
    class StatusChoices(models.TextChoices):
        WATCHING = "WATCHING", "Watching"
        COMPLETED = "COMPLETED", "Completed"
        PAUSED = "PAUSED", "Paused"
        DROPPED = "DROPPED", "Dropped"
        PLAN_TO_WATCH = "PLAN_TO_WATCH", "Plan to Watch"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    current_season = models.IntegerField(default=0)
    current_episode = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.WATCHING,
    )
    display_order = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Media"

    def __str__(self):
        return self.title
