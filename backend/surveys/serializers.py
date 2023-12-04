from rest_framework import serializers
from .models import Survey


class LevelSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.FloatField(default=1.0)


class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField()
    levels = LevelSerializer(many=True)


class SurveySerializer(serializers.Serializer):
    attributes = AttributeSerializer(many=True, required=True)
    constraints = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(),
            required=False,
        ),
        required=False,
        default=list,
    )
    restrictions = serializers.ListField(
        child=serializers.DictField(), required=False, default=[]
    )
    filename = serializers.CharField(required=False, default="survey.js")
    profiles = serializers.IntegerField(required=False, default=2)
    tasks = serializers.IntegerField(required=False, default=5)
    randomize = serializers.IntegerField(required=False, default=1)
    noDuplicates = serializers.IntegerField(required=False, default=0)
    random = serializers.IntegerField(required=False, default=0)


class ShortSurveySerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=True)
    constraints = serializers.ListField(
        child=serializers.ListField(
            child=serializers.CharField(),
            required=False,
        ),
        required=False,
        default=list,
    )

    class Meta:
        model = Survey
        fields = ["attributes", "constraints"]

    def create(self, validated_data):
        profile = self.context["request"].user
        # Assuming the Survey model has an 'attributes' field that accepts JSON
        # and a 'constraints' field that also accepts JSON.
        # Adjust this according to your actual Survey model fields.
        attributes_data = validated_data.pop("attributes")
        constraints_data = validated_data.pop("constraints", [])
        survey = Survey.objects.create(
            profile=profile, attributes=attributes_data, constraints=constraints_data
        )
        return survey
