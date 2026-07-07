from rest_framework import serializers
from media_tracker.models import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "current_season",
            "current_episode",
            "status",
            "display_order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        # Trim whitespace from title
        title_stripped = value.strip()
        if not title_stripped:
            raise serializers.ValidationError("Title cannot be empty.")

        # Case insensitive check for duplicate titles
        queryset = Media.objects.filter(title__iexact=title_stripped)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("A media entry with this title already exists.")
        
        return title_stripped

    def validate_current_season(self, value):
        if value < 0:
            raise serializers.ValidationError("Season cannot be less than 0.")
        return value

    def validate_current_episode(self, value):
        if value < 0:
            raise serializers.ValidationError("Episode cannot be less than 0.")
        return value

    def update(self, instance, validated_data):
        progress_changed = any(
            field in validated_data and validated_data[field] != getattr(instance, field)
            for field in ("current_season", "current_episode")
        )

        instance = super().update(instance, validated_data)

        if progress_changed:
            instance.status = Media.StatusChoices.WATCHING
            instance.save()

        return instance
