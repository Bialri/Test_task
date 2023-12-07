from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK

from ratings.models import Rating, Comic
from ratings.serializers import RatingSerializer, ComicSerializer



class RatingView(APIView):
    def post(self, request):
        serializer = RatingSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        try:
            existing_rating = Rating.objects.get(user_id=serializer.validated_data['user_id'],
                                                 comic_id=serializer.validated_data['comic_id'])
            existing_rating.VALUE = serializer.validated_data['VALUE']
            existing_rating.save()
            response_serializer = RatingSerializer(existing_rating, many=False)
        except Rating.DoesNotExist:
            serializer.save()
            response_serializer = serializer

        comic = serializer.validated_data['comic_id']
        comic.update_rating()
        return Response(response_serializer.data,status=HTTP_201_CREATED)


class ComicView(APIView):

    def get(self, request, comic_id):
        try:
            comic = Comic.objects.get(id=comic_id)
            serializer = ComicSerializer(comic)
            return Response(serializer.data,status=HTTP_200_OK)
        except Comic.DoesNotExist:
            message = {"comic_id": f"Invalid comic_id = {comic_id}, object does not exist"}
            return Response(message, status=HTTP_400_BAD_REQUEST)