from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class LSVD001M(models.Model):
    video_no = models.BigIntegerField(primary_key=True)
    member_id = models.CharField(max_length=20, null=False)
    church_no = models.BigIntegerField(default=0)
    subject = models.CharField(max_length=50, null=False)
    server_ip = models.CharField(max_length=30, null=False)
    server_address = models.CharField(max_length=100, null=False)
    video_size = models.IntegerField(default=0, null=False)
    tag_name = models.CharField(max_length=100, null=True)
    running_time = models.IntegerField(null=False)
    public_yn = models.CharField(max_length=1, null=False)
    download_yn = models.CharField(max_length=1, null=False)
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, default=False)

    class Meta:
        db_table = 'LSVD001M'

    def __str__(self):
        return '%s %s %s' % (self.user_id, self.server_address, self.church_no)


class LSVD002M(models.Model):
    video_no = models.BigIntegerField(primary_key=True)
    pastor_id = models.CharField(max_length=30, blank=False, null=False, unique=True, help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),)
    stream_key = models.CharField(max_length=30, null=False, unique=True)
    broadcast_time = models.DateTimeField(null=False)
    max_viewer_count = models.IntegerField(null=False)
    broadcast_start_time = models.TimeField()
    broadcast_end_time = models.TimeField()
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, default=False)

    class Meta:
        db_table = 'LSVD002M'

    def __str__(self):
        return '%s %s %s' % (self.video_no, self.pastor_id, self.stream_key)

