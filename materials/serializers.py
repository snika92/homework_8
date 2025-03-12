from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_link


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    is_subscribed = SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if request:
            user = request.user
        return Subscription.objects.filter(course=obj, user=user).exists()

    class Meta:
        model = Course
        fields = ["title", "image", "description", "lesson_count", "owner", "is_subscribed"]


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = SerializerMethodField(read_only=True)
    is_subscribed = SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if request:
            user = request.user
        return Subscription.objects.filter(course=obj, user=user).exists()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "image", "description", "lesson_count", "lessons", "owner", "is_subscribed"]


class LessonSerializer(ModelSerializer):
    video = URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"
