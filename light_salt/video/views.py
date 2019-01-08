from django.shortcuts import render
from django.core import serializers
from video.models import LSVD002M
from account.models import LightSaltPastor

# Create your views here.
def media(request):
    live_info = serializers.serialize("json", LSVD002M.objects.all(),
                                      fields=('video_no', 'pastor_id', 'stream_key'))
    pastor_info = serializers.serialize("json", LightSaltPastor.objects.all(),
                                        fields=('pastor_id', 'pastor_profile_photo', 'pastor_comment', 'church_name'))

    return render(request, 'media.html', {'live_info': live_info, 'pastor_info': pastor_info})
