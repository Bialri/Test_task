from rest_framework import serializers
from ratings.models import Rating, Comic


class RatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('rating',)