from rest_framework import serializers
from .models import Survey


class LevelSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.FloatField(default=1.0)


class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField()
    levels = LevelSerializer(many=True)


class ShortSurveySerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=True)
    restrictions = serializers.JSONField(default=list)
    cross_restrictions = serializers.JSONField(default=list)
    profiles = serializers.IntegerField(default=2, min_value=2)

    class Meta:
        model = Survey
        fields = ["attributes", "restrictions", "cross_restrictions", "profiles"]

class SurveySerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True, required=True)
    constraints = serializers.JSONField(default=list)
    restrictions = serializers.JSONField(default=list)
    cross_restrictions = serializers.JSONField(default=list)
    filename = serializers.CharField(default='survey.js', allow_blank=True)
    profiles = serializers.IntegerField(default=2, min_value=2)
    advanced = serializers.JSONField(default=dict)
    tasks = serializers.IntegerField(default=5, min_value=1)
    randomize = serializers.BooleanField(default=False)
    repeat_task = serializers.BooleanField(default=False)
    random = serializers.BooleanField(default=False)
    noFlip = serializers.BooleanField(default=False)
    duplicate_first = serializers.IntegerField(default=0, min_value=0, allow_null=True)
    duplicate_second = serializers.IntegerField(default=0, min_value=0, allow_null=True)

    class Meta:
        model = Survey
        fields = [
            'id', 'attributes', 'constraints', 'restrictions', 'cross_restrictions', 'filename',
            'advanced', 'profiles', 'tasks', 'randomize', 'repeat_task', 
            'random', 'duplicate_first', 'duplicate_second', 'noFlip',
        ]


    def validate_attributes(self, value):
        """
        Check that attributes is a list of dicts with required keys 'name' and 'levels'.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Attributes must be a list.")
        
        for item in value:
            if not isinstance(item, dict) or 'name' not in item or 'levels' not in item:
                raise serializers.ValidationError("Each attribute must be a dict with 'name' and 'levels'.")
        
        return value

    def validate_restrictions(self, value):
        """
        Check that restrictions is a list of dicts with required keys.
        """
        if not isinstance(value, list):
            raise serializers.ValidationError("Restrictions must be a list.")
        
        for item in value:
            required_keys = ['ifStates', 'elseStates']
            if not all(key in item for key in required_keys):
                raise serializers.ValidationError(
                    "Each restriction must contain 'ifStates' and 'elseStates'."
                )
        
        return value
