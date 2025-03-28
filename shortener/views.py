from django.http import Http404
from django.shortcuts import redirect
from rest_framework import status, views
from rest_framework.response import Response

from .serializers import CreateURLSerializer, URLResponseSerializer
from .services import URLShortenerService


class URLMapView(views.APIView):
    def post(self, request, hash=None):
        serializer = CreateURLSerializer(data=request.data)
        if serializer.is_valid():
            service = URLShortenerService()
            url_map = service.create(serializer.validated_data["url"])
            response_serializer = URLResponseSerializer(url_map)
            data = response_serializer.data
            data.update(
                {
                    "_links": {
                        "self": request.build_absolute_uri(f"/api/shorturls/{url_map.hash}/"),
                        "redirect": request.build_absolute_uri(f"/{url_map.hash}"),
                    }
                }
            )
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, hash=None):
        if not hash:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        service = URLShortenerService()
        url_map = service.get(hash)
        if not url_map:
            raise Http404
        data = {
            "original_url": url_map.original_url,
            "_links": {
                "self": request.build_absolute_uri(),
                "redirect": request.build_absolute_uri(f"/{hash}"),
            },
        }
        return Response(data)

    def delete(self, request, hash):
        service = URLShortenerService()
        if service.delete(hash):
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise Http404


class RedirectToURLView(views.APIView):
    def get(self, request, hash):
        service = URLShortenerService()
        url_map = service.get(hash)
        if not url_map:
            raise Http404
        return redirect(url_map.original_url)
