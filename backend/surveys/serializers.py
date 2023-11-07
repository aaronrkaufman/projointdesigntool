from rest_framework import serializers


class ExportJSSerializer(serializers.Serializer):
    attributes = serializers.ListField(child=serializers.DictField(), required=True)
    constraints = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()),
        required=False,
        default=[],
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
