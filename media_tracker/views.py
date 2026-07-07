from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from core.constants import messages
from core.responses.response import success_response
from core.logging.logger import log_info
from media_tracker.models import Media
from media_tracker.serializers import MediaSerializer

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    # permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = [
        "title",
        "updated_at",
        "created_at",
        "current_episode",
        "current_season",
    ]
    ordering = ["-updated_at"]

    def get_queryset(self):
        queryset = Media.objects.all()
        status_param = self.request.query_params.get("status")
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data, message=messages.SUCCESS)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(data=serializer.data, message=messages.SUCCESS)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        log_info(f"Media created: {instance.title} (ID: {instance.id})")
        return success_response(
            data=serializer.data,
            message=messages.CREATED,
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        log_info(f"Media updated: {instance.title} (ID: {instance.id})")
        return success_response(data=serializer.data, message=messages.UPDATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = instance.title
        media_id = instance.id
        self.perform_destroy(instance)
        log_info(f"Media deleted: {title} (ID: {media_id})")
        return success_response(message=messages.DELETED, status_code=status.HTTP_200_OK)

    # ── Custom Detailed Actions ──────────────────────────────────────────────────

    @action(detail=True, methods=["patch"], url_path="episode/increment")
    def increment_episode(self, request, pk=None):
        media = self.get_object()
        media.current_episode += 1
        media.status = Media.StatusChoices.WATCHING
        media.save()
        log_info(f"Media episode incremented: {media.title} (ID: {media.id}) - Season {media.current_season}, Episode {media.current_episode}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)

    @action(detail=True, methods=["patch"], url_path="episode/decrement")
    def decrement_episode(self, request, pk=None):
        media = self.get_object()
        if media.current_episode <= 0:
            raise ValidationError({"current_episode": "Episode cannot be less than 0."})
        media.current_episode -= 1
        media.status = Media.StatusChoices.WATCHING
        media.save()
        log_info(f"Media episode decremented: {media.title} (ID: {media.id}) - Season {media.current_season}, Episode {media.current_episode}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)

    @action(detail=True, methods=["patch"], url_path="season/increment")
    def increment_season(self, request, pk=None):
        media = self.get_object()
        media.current_season += 1
        media.current_episode = 0
        media.status = Media.StatusChoices.WATCHING
        media.save()
        log_info(f"Media season incremented: {media.title} (ID: {media.id}) - Season {media.current_season}, Episode {media.current_episode}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)

    @action(detail=True, methods=["patch"], url_path="season/decrement")
    def decrement_season(self, request, pk=None):
        media = self.get_object()
        if media.current_season <= 0:
            raise ValidationError({"current_season": "Season cannot be less than 0."})
        media.current_season -= 1
        media.current_episode = 0
        media.status = Media.StatusChoices.WATCHING
        media.save()
        log_info(f"Media season decremented: {media.title} (ID: {media.id}) - Season {media.current_season}, Episode {media.current_episode}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)

    @action(detail=True, methods=["patch"], url_path="complete")
    def mark_completed(self, request, pk=None):
        media = self.get_object()
        media.status = Media.StatusChoices.COMPLETED
        media.save()
        log_info(f"Media status changed: {media.title} (ID: {media.id}) - Status: {media.status}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)

    @action(detail=True, methods=["patch"], url_path="resume")
    def resume_watching(self, request, pk=None):
        media = self.get_object()
        media.status = Media.StatusChoices.WATCHING
        media.save()
        log_info(f"Media status changed: {media.title} (ID: {media.id}) - Status: {media.status}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)

    @action(detail=True, methods=["patch"], url_path="status")
    def change_status(self, request, pk=None):
        media = self.get_object()
        new_status = request.data.get("status")
        
        if not new_status:
            raise ValidationError({"status": "This field is required."})
            
        if new_status not in Media.StatusChoices.values:
            raise ValidationError({"status": f"Invalid status choice. Must be one of: {', '.join(Media.StatusChoices.values)}"})
            
        media.status = new_status
        media.save()
        log_info(f"Media status changed: {media.title} (ID: {media.id}) - Status: {media.status}")
        serializer = self.get_serializer(media)
        return success_response(data=serializer.data, message=messages.UPDATED)
