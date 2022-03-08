from rest_framework import generics
from rest_framework.response import Response


__all__ = ["StatusRetrieveAPIView"]


class StatusRetrieveAPIView(generics.RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        return Response()
