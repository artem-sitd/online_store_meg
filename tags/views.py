from rest_framework.generics import ListAPIView

from .models import Tags
from .serializers import TagsSerializer


class TagsListApiView(ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
