from django.db import models
from django.urls import reverse

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/Ymd/<filename>
    return '{0}/%Y%m%d/{1}'.format(instance.user.id, filename)
	
#교회Layout 
class LSCH001M(models.Model):
    layout_no = models.AutoField(primary_key=True)
    church_no = models.IntegerField(null=False, default=0)
    template_no = models.IntegerField(null=False, default=0)
    layout_pos = models.IntegerField(null=False, default=1)
    content = models.TextField(null=False)
    content_type_code = models.CharField(max_length=6, null=False)
    object_id = models.CharField(max_length=50, null=True)
    disp_count = models.IntegerField(null=False, default=5 )   
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)	
   
    class Meta:
        db_table = "LSCH001M"

    def __str__(self):
       return self.name

#교회Layout template 종류
class LSCH002M(models.Model):
    template_no = models.AutoField(primary_key=True)
    template_object_id = models.CharField(max_length=50, null=True)
    template_partition_count = models.IntegerField(null=False, default=1)
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)	
   
    class Meta:
        db_table = "LSCH002M"

    def __str__(self):
        return self.name

#게시판관리
class LSCH003M(models.Model):
    board_no = models.AutoField(primary_key=True)
    church_no = models.IntegerField(null=False, default=0)
    member_id = models.CharField(max_length=20, null=False)	
    board_title_name = models.CharField(max_length=100, null=True)	
    list_count = models.IntegerField(null=False, default=10)
    page_count = models.IntegerField(null=False, default=10)
    board_type_code = models.CharField(max_length=6, null=False)
    board_access_code = models.CharField(max_length=6, null=False)
    file_attach_yn = models.CharField(max_length=20, null=False, default="Y")
    comment_use_yn = models.CharField(max_length=20, null=False, default="Y")	
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "LSCH003M"

    def __str__(self):
       return self.name

    def get_church_alllist(no): 
        listInfo = LSCH003M.objects.filter(
            church_no=no
        )
        return listInfo

#게시글	정보
class LSCH004M(models.Model):
    board_content_no = models.AutoField(primary_key=True)
    board_no = models.IntegerField(null=False, default=0)
    subject = models.CharField(max_length=100, null=False)	
    content = models.TextField(null=False)
    group_no = models.IntegerField(null=False, default=1)
    group_order = models.IntegerField(null=False, default=1)
    depth = models.IntegerField(null=False, default=0)
    hit_count = models.IntegerField(null=False, default=0)
    password = models.CharField(max_length=50, null=True)	
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "LSCH004M"
		
    def __str__(self):
        return self.name
   
    def get_board_list5(no):
        listInfo=LSCH004M.objects.filter(
            board_no=no
        ).order_by('-group_no', 'group_order')[:5]
        return listInfo

    #def get_absolute_url(self, **kwargs): # redirect시 활용
    #    page=1
    #    if kwargs is not None:
    #        page = kwargs['page']		
    #    url = (("%s?page=%s") % (reverse('mychurch:board_list', args=[self.board_no]), page))
    #    return url

#댓글 정보
class LSCH005D(models.Model):
    board_content_no = models.IntegerField(null=False, default=0)
    comment_no = models.AutoField(primary_key=True)
    group_no = models.IntegerField(null=False, default=1)
    group_order = models.IntegerField(null=False, default=1)
    depth = models.IntegerField(null=False, default=0)
    comment = models.CharField(max_length=2000, null=False)	
    secret_comment_yn = models.CharField(max_length=10, null=False, default="N")
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "LSCH005D"
        unique_together = (('board_content_no', 'comment_no'),)

    def __str__(self):
       return self.name

    def get_comment_all(no): 
        commentList = LSCH005D.objects.filter(
            board_content_no=no
        ).order_by('-group_no', 'group_order')
        return commentList

#첨부파일 정보
import os
class LSCH006D(models.Model):
    board_content_no = models.IntegerField(null=False, default=0)
    file_attach_no = models.IntegerField(null=False, default=0, primary_key=True)
    file_name = models.CharField(max_length=200, null=False)	
    file_size = models.IntegerField(null=False, default=0)
    file_type_code = models.CharField(max_length=6, null=False)
    download_count = models.IntegerField(null=False, default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "LSCH006D"
        unique_together = (('board_content_no', 'file_attach_no'),)

    def get_board_list(no):
        listInfo=LSCH006D.objects.filter(
            board_content_no=no
        ).exclude(
            file_type_code = "IMG"
        )
        return listInfo

    @property
    def filename(self):
        return os.path.basename(self.file_name)

    def __str__(self):
       return self.name

#메뉴 정보
class LSCH007M(models.Model):
    menu_no = models.AutoField(primary_key=True)
    church_no = models.IntegerField(null=False, default=0)
    board_no = models.IntegerField(null=False, default=0) #메뉴가 게시판 종류 일때만...
    menu_name = models.CharField(max_length=100, null=False)	
    menu_link_addr = models.CharField(max_length=100, null=False)
    menu_order = models.IntegerField(null=False, default=0)
    create_time = models.DateTimeField(auto_now_add=True, null=False)
    modify_time = models.DateTimeField(auto_now=True, null=False)
    user_id = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "LSCH007M"

    def __str__(self):
       return self.name