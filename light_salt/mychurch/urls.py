from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView

from mychurch.views import MychurchIndex, Board, BoardView, BoardWrite, BoardEdit, DeleteFile, \
     Comments, ImageUpload, ImageDelete, ImageRecovery,MychurchAdmin, MyMembers
from mychurch import views

app_name = 'mychurch'

urlpatterns = [
    # ex: /mychurch/
    path('', MychurchIndex.as_view(), name='index'),
    path('admin/<int:church_no>/', MychurchAdmin.as_view(), name='myadmin'),
    path('admin/<int:church_no>/mymembers/', MyMembers.as_view(), name='mymembers'),
    path('board/', Board.as_view(), name='board_index'),
    path('board/<int:board_no>/', Board.as_view(), name='board_list'),
    path('board/<int:board_no>/view/<int:board_content_no>/', BoardView.as_view(), name='board_view'),
    path('board/<int:board_no>/view/<int:board_content_no>/comment/', Comments.as_view(), name='comment'),
    path('board/<int:board_no>/edit/<int:board_content_no>/', BoardEdit.as_view(), name='board_edit'),
    path('board/<int:board_no>/reply/<int:board_content_no>/', BoardWrite.as_view(), name='board_reply'),
    path('board/<int:board_no>/write/', BoardWrite.as_view(), name='board_write'),
    path('board/<int:board_no>/image/upload/', views.ImageUpload, name='image_upload'),
    path('board/<int:board_no>/image/delete/', views.ImageDelete, name='image_delete'),
    path('board/<int:board_no>/image/recovery/', views.ImageRecovery, name='image_recovery'),
    path('board/<int:board_no>/view/download/<path:filename>/', views.FileDownload, name='file_download'),
    path('board/<int:board_no>/delete/<int:board_content_no>/', views.DeleteContents, name='board_delete'),
    path('board/<int:board_no>/delete/<int:board_content_no>/<int:file_attach_no>/<path:filename>/', views.DeleteFile, name='file_delete')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
