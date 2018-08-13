from django.shortcuts import render
from django.core import serializers
from video.models import LSVD002M

# Create your views here.
def media(request):
    live_info = serializers.serialize("json", LSVD002M.objects.all(), fields=('video_no', 'pastor_id', 'stream_key'))

    return render(request, 'media.html', {'live_info': live_info})
