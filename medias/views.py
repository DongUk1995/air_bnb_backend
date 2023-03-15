from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Photo


class PhotoDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)
        if (photo.room and photo.room.owner != request.user) or (
            photo.experience and photo.experience.host != request.user
        ):
            raise PermissionDenied
        photo.delete()
        return Response(status=HTTP_200_OK)


class GetUploadURL(APIView):
    def post(self, reuqest):
        url = f"http://api.cloudflare.com/client/v4/accounts/img/images/v2/direct_upload"
        one_time_url = reuqest.post(
            url,
        )
        one_time_url = one_time_url.json()
        result = one_time_url.get("result")
        if result:
            return Response({"id": result("id"), "uploadURL": result.get("uploadURL")})
        else:
            return Response(
                {
                    "id": "0000",
                    "uploadURL": "http://127.0.0.1:8000/api/v1/medias/photos/upload-photo",
                }
            )
