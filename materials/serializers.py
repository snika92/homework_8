from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField

from materials.models import Course, Lesson
from materials.validators import validate_video_link


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "image", "description", "lesson_count", "owner"]


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = SerializerMethodField()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "image", "description", "lesson_count", "lessons", "owner"]


class LessonSerializer(ModelSerializer):
    video = URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"
