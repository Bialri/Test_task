from rest_framework import serializers
from ratings.models import Rating, Comic


class RatingSerializer(serializers.ModelSerializer):
    """
    Сериализатор рейтинга
    """
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'


class ComicSerializer(serializers.ModelSerializer):
    """
    Сериализатор комикса
    """
    class Meta:
        model = Comic
        fields = ('rating',)