from django.shortcuts import render
from django.core import serializers
from video.models import LSVD001M
from account.models import LightSaltPastor


def main(request):
    video_info = serializers.serialize("json", LSVD001M.objects.all(), fields=('server_address', 'church_no', 'user_id'))
    church_info = serializers.serialize("json", LightSaltPastor.objects.all(),
                                        fields=('pastor_id', 'church_name', 'church_address'))

    return render(request, 'base.html', {'server_address': video_info, 'church_info': church_info})

