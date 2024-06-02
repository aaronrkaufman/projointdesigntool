from rest_framework import serializers
from .models import Survey


class LevelSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.FloatField(default=1.0)


class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField()
    levels = LevelSerializer(many=True)


class ConditionSerializer(serializers.Serializer):
    attribute = serializers.CharField()
    operation = serializers.CharField()
    value = serializers.CharField()
    logical = serializers.CharField(required=False)


class RestrictionSerializer(serializers.Serializer):
    condition = ConditionSerializer(many=True)
    result = ConditionSerializer(many=True)


class ShortSurveySerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=True)
    restrictions = RestrictionSerializer(
        many=True, required=False, default=list)
    cross_restrictions = serializers.JSONField(default=list)
    profiles = serializers.IntegerField(default=2, min_value=2)
    csv_lines = serializers.IntegerField(default=500)

    class Meta:
        model = Survey
        fields = ["attributes", "restrictions",
                  "cross_restrictions", "profiles", "csv_lines"]

    def validate(self, data):
        """
        Custom validation that checks each restriction for logic errors or inconsistencies.
        """
        restrictions = data['restrictions']
        for restriction in restrictions:
            if "logical" in restriction['condition'] and cond['logical'] not in ['||', '&&']:
                raise serializers.ValidationError(
                    "Invalid operation in logical.")
            for cond in restriction['condition']:
                if cond['operation'] not in ['==', '!=']:
                    raise serializers.ValidationError(
                        "Invalid operation in result.")
            for res in restriction['result']:
                if res['operation'] not in ['==', '!=']:
                    raise serializers.ValidationError(
                        "Invalid operation in result.")
        return data


class SurveySerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=True)
    constraints = serializers.JSONField(default=list, required=False)
    restrictions = RestrictionSerializer(
        many=True, required=False, default=list)
    cross_restrictions = serializers.JSONField(default=list, required=False)
    filename = serializers.CharField(default='survey.js', allow_blank=True)
    profiles = serializers.IntegerField(
        default=2, min_value=2, allow_null=True)
    tasks = serializers.IntegerField(default=5, min_value=1, allow_null=True)
    randomize = serializers.BooleanField(default=False, allow_null=True)
    repeat_task = serializers.BooleanField(default=False, allow_null=True)
    random = serializers.BooleanField(default=False, allow_null=True)
    noFlip = serializers.BooleanField(default=False, allow_null=True)
    csv_lines = serializers.IntegerField(default=500, allow_null=True)
    duplicate_first = serializers.IntegerField(
        default=0, min_value=0, allow_null=True)
    duplicate_second = serializers.IntegerField(
        default=0, min_value=0, allow_null=True)
    advanced = serializers.JSONField(default=dict)

    class Meta:
        model = Survey
        fields = [
            'id', 'attributes', 'constraints', 'restrictions', 'cross_restrictions', 'filename',
            'advanced', 'profiles', 'tasks', 'randomize', 'repeat_task',
            'random', 'duplicate_first', 'duplicate_second', 'noFlip', 'csv_lines'
        ]

    def validate(self, data):
        """
        Custom validation that checks each restriction for logic errors or inconsistencies.
        """
        restrictions = data['restrictions']
        for restriction in restrictions:
            # Example validation logic
            for cond in restriction['condition']:
                if cond['attribute'] not in ['expected', 'attribute', 'list']:
                    raise serializers.ValidationError(
                        "Invalid attribute in condition.")
            for res in restriction['result']:
                if res['operation'] not in ['==', '!=']:
                    raise serializers.ValidationError(
                        "Invalid operation in result.")
        return data

    def validate_attributes(self, value):
        """
        Check that attributes is a list of dicts with required keys 'name' and 'levels'.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Attributes must be a list.")

        for item in value:
            if not isinstance(item, dict) or 'name' not in item or 'levels' not in item:
                raise serializers.ValidationError(
                    "Each attribute must be a dict with 'name' and 'levels'.")

        return value
