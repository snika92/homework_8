from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["title", "image", "description", "lesson_count"]


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
