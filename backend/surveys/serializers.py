from rest_framework import serializers
from .models import Survey


class ConstraintSerializer(serializers.Serializer):
    constraints = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(),
        ),
        required=False,
        default=list,
    )


class LevelSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.FloatField(default=1.0)


class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField()
    levels = LevelSerializer(many=True)


class ExportJSSerializer(serializers.Serializer):
    attributes = AttributeSerializer(many=True, required=True)
    constraints = ConstraintSerializer()
    restrictions = serializers.ListField(
        child=serializers.DictField(), required=False, default=[]
    )
    filename = serializers.CharField(required=False, default="survey.js")
    profiles = serializers.IntegerField(required=False, default=2)
    tasks = serializers.IntegerField(required=False, default=5)
    randomize = serializers.IntegerField(required=False, default=1)
    noDuplicates = serializers.IntegerField(required=False, default=0)
    random = serializers.IntegerField(required=False, default=0)


class SurveySerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=True)
    constraints = ConstraintSerializer()

    class Meta:
        model = Survey
        fields = ["attributes", "constraints"]

    def create(self, validated_data):
        return Survey.objects.create(
            profile=self.context["request"].user, **validated_data
        )
