from rest_framework import serializers
from apis.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
        extra_kwargs = {'owner': {'write_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.id
        return representation