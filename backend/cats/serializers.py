import requests
from rest_framework import serializers
from .models import SpyCat, Mission, Target

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'

    def validate_breed(self, value):
        response = requests.get(f"https://api.thecatapi.com/v1/breeds")
        if response.status_code != 200:
            raise serializers.ValidationError("Breed validation service unavailable")
        breeds = [breed['name'] for breed in response.json()]
        if value not in breeds:
            raise serializers.ValidationError("Invalid breed")
        return value

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'mission', 'name', 'country', 'notes', 'completed']

    def validate(self, data):
        mission = self.context.get('mission')
        if mission and (mission.completed or data.get('completed')):
            if 'notes' in data and data['notes'] != self.instance.notes:
                raise serializers.ValidationError("Cannot update notes if mission or target is completed")
        return data

class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat = serializers.PrimaryKeyRelatedField(queryset=SpyCat.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'completed', 'targets']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', None)
        instance.completed = validated_data.get('completed', instance.completed)
        cat = validated_data.get('cat', instance.cat)
        if cat is not None:
            instance.cat = cat
        instance.save()
        if targets_data is not None:
            for target_data in targets_data:
                target_id = target_data.get('id', None)
                if target_id:
                    target = Target.objects.get(id=target_id, mission=instance)
                    if instance.completed or target.completed:
                        if 'notes' in target_data and target_data['notes'] != target.notes:
                            raise serializers.ValidationError("Cannot update notes if mission or target is completed")
                    for attr, value in target_data.items():
                        if attr != 'id':
                            setattr(target, attr, value)
                    target.save()
        return instance