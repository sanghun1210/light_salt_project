# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.db import connection, transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import LSCH004M, LSCH003M, LSCH006D, LSCH005D
from django.views.generic import TemplateView, UpdateView
from django.shortcuts import get_object_or_404
from mychurch.pagingHelper import pagingHelper
from datetime import date, datetime
from django.core.files.storage import FileSystemStorage
from django.forms import forms
from django.conf import settings
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import loader
from html.parser import HTMLParser
from .forms import BoardForm


class MyHTMLParser(HTMLParser): 
    def __init__(self, *args, **kwargs):
        self.data_list = []
        HTMLParser.__init__(self, *args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for (attr, value) in attrs:
                if attr =='src':
                    self.data_list.append(value)				

    def get_image_set(self):
        return self.data_list

class MychurchIndex(LoginRequiredMixin, TemplateView):
    church_no=1
    board_no = []
    board_title= []		
    
    def get(self,request):
        imgList=[] #list(=array), dictionary(key=>value):{}
	
       #교회 게시판정보 목록 조회    
        boardConfList = LSCH003M.get_church_alllist(self.church_no)
        for conf in boardConfList:	
            self.board_no.append(conf.board_no)
            self.board_title.append(conf.board_title_name)

        noticeList = LSCH004M.get_board_list5(1)
        counselList = LSCH004M.get_board_list5(2)
    
        #TO-DO 첨부가능 여부 조회 필요
        #join을 위한 queryset은 느린가?
        galleryList = LSCH004M.get_board_list5(3)
        for gallery in galleryList:	
          
            #img=LSCH006M.objects.filter(
            #    board_content_no=gallery.board_content_no
            #)[:1]
            #if len(img) > 0:
            for img in LSCH006D.objects.raw("SELECT 1 as file_attach_no, file_name FROM LSCH006D WHERE board_content_no=%s AND file_type_code='IMG' LIMIT 1",[gallery.board_content_no]):
                #list자료구조에 dictionary정보 저장
                if img:
                    imgList.append({'path':'/mychurch'+img.file_name, 'board_content_no':gallery.board_content_no, 'subject':gallery.subject, 'create_time':gallery.create_time, })
        
        #current_page =1
        #totalCnt = LSCH004M.objects.all().count()
        #pagingHelperIns = pagingHelper();
        #totalPageList = pagingHelperIns.getTotalPageList( totalCnt, rowsPerPage)
        #print 'totalPageList', totalPageList

	#####################################################################
        #Person.objects.raw('SELECT id, first_name, last_name, birth_date FROM myapp_person')
        #star_set = Star.objects.all()
        # iterator() 메서드는 전체 레코드의 일부씩만 DB에서 가져오므로
        # 메모리를 절약할 수 있다.
        #for star in star_set.iterator():
            #print(star.name)

        #atom_set = Atom.objects.all()

        # 첫 번째 쿼리로 레코드를 가져오기 시작한다
        #atom_iterator = atom_set.iterator()

        # 첫 번째 레코드를 감지(peek)한다
        #try:
            #first_atom = next(atom_iterator)
        #except StopIteration:
            # 레코드가 없다면 아무 일도 하지 않는다
            #pass
        #else:
            # 레코드가 하나라도 존재한다면
            # 모든 레코드를 순회한다(첫 번째 레코드를 포함해서)
            #from itertools import chain
            #for atom in chain([first_atom], atom_set):
            #print(atom.mass)    
        return render(request, 'mychurch/main.html', {'boardNo':self.board_no, 'boardTitle':self.board_title, 'noticeList': noticeList, 'counselList': counselList, 'imgList': imgList, })


class Board(LoginRequiredMixin, TemplateView):
     
    #목록조회
    def get(self, request, board_no):
        board_conf = get_object_or_404(LSCH003M, pk=board_no)
        searchStr = request.GET.get('searchStr')
        searchKey = request.GET.get('searchKey')
        page = request.GET.get('page')
      
        if board_conf.board_type_code == 'IMG' :
            board_list = LSCH004M.objects.raw("""SELECT a.board_content_no, a.board_no, a.subject, \
            a.hit_count, a.create_time, b.name as user_id, MAX(c.file_name) as content \
            FROM LSCH004M as a LEFT JOIN LSMB001M as b ON a.user_id=b.member_id LEFT OUTER JOIN LSCH006D as c ON a.board_content_no=c.board_content_no \
            WHERE a.board_no=%s AND c.file_name IS NOT NULL  \
            GROUP BY a.board_content_no, a.board_no, a.subject, a.hit_count, a.create_time, b.name, a.group_no, a.group_order ORDER BY a.group_no DESC, a.group_order ASC """, [board_no])
        else :
            board_list = LSCH004M.objects.raw("""SELECT a.board_content_no, a.board_no, a.subject, \
            a.hit_count, a.password, a.create_time, b.name as user_id \
            FROM LSCH004M as a, LSMB001M as b  WHERE a.user_id=b.member_id AND a.board_no=%s \
            ORDER BY a.group_no DESC, a.group_order ASC """, [board_no])		

        paginator = Paginator(list(board_list), board_conf.list_count) # Show count board list per page
        try:
            page_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_list = paginator.page(paginator.num_pages)
        #cursor = connection.cursor()
        #cursor.execute("UPDATE yourtablename SET field1=value1, .. WHERE .. ")

        #transaction.set_dirty()        
        #transaction.commit()
        return render(request, 'mychurch/board/board_list.html', {'searchKey':'', 'searchStr':'', 'board_conf': board_conf, 'page_list': page_list, 'page':page})	

    def post(self, request, board_no):
        board_conf = get_object_or_404(LSCH003M, pk=board_no)
        searchStr = request.POST.get('searchStr')
        searchKey = request.POST.get('searchKey')
        page = request.POST.get('page')
        	
        if searchKey == "1":
            board_list = LSCH004M.objects.raw("""SELECT a.board_content_no, a.board_no, a.subject, a.content, \
            a.hit_count, a.password, a.create_time, b.name as user_id \
            FROM LSCH004M as a, LSMB001M as b WHERE a.user_id=b.member_id AND board_no=%s AND a.subject LIKE CONCAT('%%',%s,'%%') \
            ORDER BY group_no DESC, group_order ASC """, [board_no, searchStr])  
        elif searchKey == "2":
            board_list = LSCH004M.objects.raw("""SELECT a.board_content_no, a.board_no, a.subject, a.content, \
            a.hit_count, a.password, a.create_time, b.name as user_id \
            FROM LSCH004M as a, LSMB001M as b WHERE a.user_id=b.member_id AND board_no=%s AND a.content LIKE CONCAT('%%',%s,'%%') \
            ORDER BY group_no DESC, group_order ASC """, [board_no, searchStr])
        elif searchKey == "3":
            board_list = LSCH004M.objects.raw("""SELECT a.board_content_no, a.board_no, a.subject, a.content, \
            a.hit_count, a.password, a.create_time, b.name as user_id \
            FROM LSCH004M as a, LSMB001M as b WHERE a.user_id=b.member_id AND board_no=%s AND CONCAT(a.subject,a.content) LIKE CONCAT('%%',%s,'%%') \
            ORDER BY group_no DESC, group_order ASC """, [board_no, searchStr])
        else:
            raise forms.ValidationError('Invalid access error')			
        
        paginator = Paginator(list(board_list), board_conf.list_count) # Show count board list per page
        page = request.GET.get('page')
        try:
            page_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_list = paginator.page(paginator.num_pages)

        return render(request, 'mychurch/board/board_list.html', {'searchKey':searchKey, 'searchStr':searchStr, 'board_conf': board_conf, 'page_list': page_list, 'page':page})

class Comments(LoginRequiredMixin, TemplateView):
    def post(self, request, board_no, board_content_no) :  #댓글저장
        comment = request.POST.get('comment', False)
        comment_no = request.POST.get('comment_no', False)
        page = request.POST.get('page', False)
        secret_comment_yn = request.POST.get('secret_comment_yn', False)

        if not comment :
            raise forms.ValidationError('댓글 내용을 입력 하세요.')   
        
        tmp_no = request.POST.get('board_content_no')
        if str(tmp_no) != str(board_content_no):
            raise forms.ValidationError(('Invalid access %s.%s') % (tmp_no, board_content_no)) 
        
        if secret_comment_yn is None :
            secret_comment_yn = "N"

        #raise forms.ValidationError(('comment_no:%s')%(comment_no))				
        if int('0' + comment_no) > 0: #답글등록
            parent = get_object_or_404(LSCH005D, pk=int(comment_no))
            # 왜 오류가 나지?
            #LSCH005D.objects.filter(board_content_no=parent.board_content_no, group_order > parent.group_order, group_no=parent.group_no  ).update(group_order=F('group_order') + 1)
            cursor = connection.cursor()
            cursor.execute("UPDATE LSCH005D SET group_order=group_order+1 WHERE board_content_no=%s AND group_order > %s AND group_no=%s", [parent.board_content_no,parent.group_order,parent.group_no])

            new_comment = LSCH005D(board_content_no=board_content_no, group_no=parent.group_no, group_order=parent.group_order+1, depth=parent.depth+1, comment=comment, secret_comment_yn=secret_comment_yn, user_id=request.user.member_id)
            new_comment.save()

        else :
            new_comment = LSCH005D(board_content_no=board_content_no, secret_comment_yn=secret_comment_yn, comment=comment, user_id=request.user.member_id)
            new_comment.save()

            #group no update
            c_no = LSCH005D.objects.latest('comment_no')
            LSCH005D.objects.filter(pk=c_no.comment_no).update(group_no=c_no.comment_no)
            
		#댓글 조회
        return self.getCommentList(request, board_content_no, page)

    #댓글삭제
    def get(self, request, board_no, board_content_no) :
        comment_no = request.GET.get('comment_no', False)
        group_order_no = request.GET.get('group_order', False)
        group_no = request.GET.get('group_no', False)
        page = request.GET.get('page', False)
        if comment_no is None:
            raise forms.ValidationError('Invalid access')
        if group_order_no is None:
            raise forms.ValidationError('Invalid access')

        #세션ID와 user_id가 같은때만 삭제
        LSCH005D.objects.filter(comment_no=comment_no, user_id=request.user.member_id).delete()
        #하위 댓글도 삭제
        cursor = connection.cursor()
        cursor.execute("DELETE FROM LSCH005D WHERE group_no=%s AND group_order > %s", [group_no, group_order_no])

        return self.getCommentList(request, board_content_no, page)       	
        #return redirect('mychurch:board_view', board_no=board_no, board_content_no=board_content_no)

    def getCommentList(self, request, board_content_no, page=1) :
        #댓글 조회
        comment_list = LSCH005D.get_comment_all(board_content_no)
        template = loader.get_template('mychurch/board/comments.html')
          
        page_list = self.getPageList(request, comment_list, page)
        
        context = {'comment_list': comment_list, 'comment_page':page_list, }

        return HttpResponse(template.render(context,request))	     

    def getPageList(self, request, comment_list, page=1)	:
        paginator = Paginator(list(comment_list), 20) # Show count board list per page
        try:
            page_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_list = paginator.page(paginator.num_pages)

        return page_list

@login_required  
def ImageUpload(request,board_no):
    f = request.FILES.get('file')
    folder= settings.MEDIA_ROOT+'/'+request.user.member_id+'/'+str(date.today())+'/'
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    if f.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
        return HttpResponse(('Please keep filesize under %s. Current filesize %s') % (settings.MAX_IMAGE_UPLOAD_SIZE, f.size))                                       
        
    #파일저장
    fs = FileSystemStorage(location=folder)
    filename = fs.save(f.name, f) 
    file_url = fs.url('/'+request.user.member_id+'/'+str(date.today())+'/'+filename)

    return JsonResponse({'location': '/mychurch'+file_url})

@login_required  
def ImageDelete(request,board_no):
    import os
    filename=request.POST.get('imageName')
    f = os.path.basename(filename)
    file_path = settings.MEDIA_ROOT + filename[len('/mychurch'+settings.MEDIA_URL)-1:]
    file_path_bak =file_path+".bak"

    if os.path.isfile(file_path):
        os.rename(file_path, file_path_bak)  

    return HttpResponse("SUCCESS")

def ImageRecovery(request,board_no):
    import os
    filename=request.POST.get('filePath')
    f = os.path.basename(filename)
    file_path = settings.MEDIA_ROOT + filename[len('/mychurch'+settings.MEDIA_URL)-1:]
    file_path_bak =file_path+".bak"

    if os.path.isfile(file_path_bak):
        os.rename(file_path_bak, file_path)  

    return HttpResponse("SUCCESS")

@login_required
def FileDownload(request,board_no, filename): 
    import functools
    import os
    import urllib.parse
    import mimetypes

    file=os.path.basename(filename)
    #file_path = functools.reduce(os.path.join, (settings.MEDIA_ROOT, filename))
    file_path = settings.MEDIA_ROOT + filename[len(settings.MEDIA_URL)-1:] # "/pro/2018-06-15/test.txt" 
    
    encoding=None
    response = HttpResponse()

    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as fp:
            response = HttpResponse(fp.read())
        content_type, encoding = mimetypes.guess_type(file_path)

        if content_type is None:
            content_type = 'application/octet-stream'
        response['Content-Type'] = content_type
        response['Content-Length'] = str(os.stat(file_path).st_size)

    if encoding is not None:
        response['Content-Encoding'] = encoding

    if u'WebKit'in request.META.get('HTTP_USER_AGENT', u'Webkit'):
        filename_header = 'filename="%s"' % urllib.parse.quote(file)
        #raise forms.ValidationError(('filename_header:%s')%(filename_header))
    elif u'MSIE' in request.META.get('HTTP_USER_AGENT', u'MSIE'):
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.parse.quote(file)
        
    response['Content-Disposition'] = 'attachment; ' + filename_header

    return response

@login_required
def DeleteFile(request, board_no, board_content_no, file_attach_no, filename):
    import os
    import urllib.parse
    filename = urllib.parse.unquote(filename)
    file_path = settings.MEDIA_ROOT + filename[len(settings.MEDIA_URL)-1:]
    if os.path.isfile(file_path):
        os.remove(file_path)    
    LSCH006D.objects.filter(file_attach_no=file_attach_no).delete()    
    return redirect('mychurch:board_edit', board_content_no=board_content_no, board_no=board_no, )


@login_required
def DeleteContents(request,board_no, board_content_no):
    import os
    import urllib.parse
    board_conf = get_object_or_404(LSCH003M, pk=board_no)
    request.POST.get('user_id', False)
    group_order_no = request.POST.get('group_order', False)
    group_no = request.POST.get('group_no', False)

    #file 삭제
    if board_conf.file_attach_yn == 'Y':
        
        for file in LSCH006D.objects.raw('SELECT file_attach_no, file_name FROM LSCH006D WHERE board_content_no=%s',[board_content_no]):
            filename = urllib.parse.unquote(file.file_name)
            if filename:
                file_path = settings.MEDIA_ROOT + filename[len(settings.MEDIA_URL)-1:]
                #raise forms.ValidationError(('filename_header:%s')%(file_path))
                if os.path.isfile(file_path):
                    os.remove(file_path)    
            LSCH006D.objects.filter(file_attach_no=file.file_attach_no).delete()

    #댓글 삭제
    if board_conf.comment_use_yn == 'Y':
        LSCH005D.objects.filter(board_content_no=board_content_no).delete()

    #테이블 내용 삭제
    LSCH004M.objects.filter(board_no=board_no, board_content_no=board_content_no).delete()

    #하위 내용(답글)도 삭제(댓글 및 첨부파일 포함)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM LSCH004M WHERE board_no=% AND group_no=%s AND group_order > %s", [board_no, group_no, group_order_no])

    return redirect('mychurch:board_list', board_no=board_no)

class BoardView(LoginRequiredMixin, TemplateView):   
    def get(self, request, board_no, board_content_no):
        board_content = get_object_or_404(LSCH004M, pk=board_content_no) 
        board_conf = get_object_or_404(LSCH003M, pk=board_no)
        password = request.GET.get("password_in", False)
        page = request.GET.get("page", False)

        if not page :
            page=1

        #raise forms.ValidationError(('password:%s')%(board_content.password))
        if not board_content.password in [None, ''] :
            if not password : #패스워드 입력화면
                return render(request, 'mychurch/board/board_password.html', {'board_no':board_no, 'board_content_no':board_content_no, 'error_message':'', 'page':page})   
            elif password != board_content.password :
                return render(request, 'mychurch/board/board_password.html', {'board_no':board_no, 'board_content_no':board_content_no, 'error_message':'패스워드가 일치하지 않습니다', 'page':page})

        if board_conf.file_attach_yn == 'Y':
            file_list= LSCH006D.get_board_list(board_content_no)
        else :
            file_list = None
        
        #조회수 증가
        LSCH004M.objects.filter(pk=board_content_no).update(hit_count=F('hit_count') + 1) 

        #댓글 조회
        if board_conf.comment_use_yn == 'Y' :
            comment_list = LSCH005D.get_comment_all(board_content_no)
            #raise forms.ValidationError(('comment_list:%s')%(comment_list))
            comment_obj = Comments()
            page_list = comment_obj.getPageList(request,comment_list, 1)
            
        return render(request, 'mychurch/board/board_view.html', {'board_no': board_no, 'board_content': board_content, 'board_conf': board_conf, 'file_list':file_list, 'comment_list':comment_list, 'comment_page':page_list, 'page':page})

class BoardEdit(LoginRequiredMixin, UpdateView):   
    def get(self, request, board_no, board_content_no):
        board_contents = get_object_or_404(LSCH004M, pk=board_content_no) 
        board_conf = get_object_or_404(LSCH003M, pk=board_no)
        page = request.GET.get('page', False)

        if board_conf.file_attach_yn == 'Y':
            file_list= LSCH006D.get_board_list(board_content_no)
        else :
            file_list = None
        
        return render(request, 'mychurch/board/board_edit.html', {
        'board_contents': board_contents,
        'board_no': board_no, 
        'board_conf': board_conf, 
        'file_list':file_list,
        'page':page })

    def post(self, request, board_no, board_content_no):
        import os
        files = request.FILES.getlist('file_field')
        folder= settings.MEDIA_ROOT+'/pro/'+str(date.today())+'/'
        if not os.path.exists(folder):
            os.makedirs(folder)

        password = request.POST.get('password', False)
        #비번검증
        #if password:
        #    if not LSCH004M.objects.filter(pk=board_content_no, password=password).exists():
        #        raise forms.ValidationError(('password is not correct')) 		
        user_id = request.POST.get('user_id', False)
        subject = request.POST.get('subject', False)
        content = request.POST.get('content', False)
        page = request.POST.get('page', False)
        
        if request.user.member_id != user_id:
            raise forms.ValidationError(('작성자만 수정이 가능 합니다(%s:%s)') % (request.user.member_id,user_id))

        if password :
            LSCH004M.objects.filter(pk=board_content_no).update(subject=subject,content=content, password=password, user_id=request.user.member_id)
        else :
            LSCH004M.objects.filter(pk=board_content_no).update(subject=subject,content=content, user_id=request.user.member_id)
        
        fs = FileSystemStorage(location=folder)

        for f in files:
            if f.size > int(settings.MAX_FILE_UPLOAD_SIZE):
                raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (settings.MAX_FILE_UPLOAD_SIZE, f.size))		
     
            #파일저장
            filename = fs.save(f.name, f) 
            file_url = fs.url('/'+request.user.member_id+'/'+str(date.today())+'/'+filename)
            extension = filename.split('.')[-1]
            #raise forms.ValidationError(('파일(%s:%s)') % (filename,file_url))
            data = LSCH006D.objects.create(board_content_no=board_content_no, file_name=file_url, file_size=f.size, file_type_code=extension, download_count=0, user_id=request.user.member_id ) 

        #내용안의 이미지링크 추출
        parser = MyHTMLParser() 
        content = request.POST.get('content', False)
        parser.feed(content)

        #기존 이미지 첨부 삭제
        LSCH006D.objects.filter(board_content_no=board_content_no, file_type_code='IMG').delete()
        #이미지 정보 재저장
        if parser.get_image_set() :
            for url in parser.get_image_set():  
                extension = 'IMG'
                file_url = 	url.replace("/mychurch", "")				
                data = LSCH006D.objects.create(board_content_no=board_content_no, file_name=file_url, file_size=0, file_type_code=extension, download_count=0, user_id=request.user.member_id )   

        return redirect('mychurch:board_list', board_no=board_no)

class BoardWrite(LoginRequiredMixin, TemplateView): 
    church_no=1

    def get(self, request, board_no, board_content_no=0):
        board_conf = get_object_or_404(LSCH003M, pk=board_no)
        form = BoardForm({'file_attach_yn': board_conf.file_attach_yn})
        page = request.GET.get('page', False)
        if not page :
            page=1

        return render(request, 'mychurch/board/board_write.html',{
        'form': form,
        'board_no':board_no,
        'user_id':request.user.member_id,
        'file_attach_yn':board_conf.file_attach_yn,
		'board_content_no':board_content_no,
        'page':page
        })

    def post(self, request, board_no, board_content_no=0):
        form = BoardForm({'file_attach_yn':request.POST.get('file_attach_yn', False)}, request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        board_content_no = request.POST.get('board_content_no', False)
        folder= settings.MEDIA_ROOT+'/'+request.user.member_id+'/'+str(date.today())+'/'
        page = request.POST.get('page', False)
        if not page :
            page=1
        
        import os
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        if form.is_valid():
            if int(board_content_no) > 0 : #답글등록
                parent = get_object_or_404(LSCH004M, pk=int(board_content_no))
                cursor = connection.cursor()
                cursor.execute("UPDATE LSCH004M SET group_order=group_order+1 WHERE board_no=%s AND board_content_no=%s AND group_order > %s AND group_no=%s", [board_no, board_content_no,parent.group_order,parent.group_no])

                subject =  request.POST.get('subject', False)
                content =  request.POST.get('content', False)
                password =  request.POST.get('password', False)

                #post=new_content = LSCH004M(board_no=board_no, group_no=parent.group_no, group_order=parent.group_order+1, depth=parent.depth+1, subject=subject, content=content, password=password, create_time=datetime.now(), user_id=request.user.member_id)
                post= form.save(group_order=parent.group_order+1, group_no=parent.group_no, depth=parent.depth+1)
            else :
                post = form.save(group_order=1, group_no=1,depth=0) # BoardForm 클래스에 정의된 save() 메소드 호출
                
            board_content = LSCH004M.objects.order_by('board_content_no').last()
            if int(board_content_no) <= 0 : # 답글이 아닐경우 group no update
                LSCH004M.objects.filter(pk=board_content.board_content_no).update(group_no=board_content.board_content_no)

            fs = FileSystemStorage(location=folder)
            #num=0
            
            for f in files:

                if f.size > int(settings.MAX_FILE_UPLOAD_SIZE):
                    #delete contents
                    LSCH004M.objects.filter(board_content_no=board_content.board_content_no).delete() 
                    raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (settings.MAX_FILE_UPLOAD_SIZE, f.size))                                       

                #파일저장()
                filename = fs.save(f.name, f) 
                file_url = fs.url('/'+request.user.member_id+'/'+str(date.today())+'/'+filename)
                extension = filename.split('.')[-1]
                #num=num+1
                #rows=LSCH006D()
                #rows.board_content_no=board_content.board_content_no 
                #rows.file_attach_no=num
                #rows.file_name=file_url
                #rows.file_size=f.size
                #rows.file_type_code=extension
                #rows.create_time=datetime.now()
                #rows.ser_id=request.POST.get('user_id', False)
                #rows.save()
                data = LSCH006D.objects.create(board_content_no=board_content.board_content_no, file_name=file_url, file_size=f.size, file_type_code=extension, download_count=0, user_id=request.user.member_id )
                #cursor = connection.cursor()
                #cursor.execute("INSERT INTO LSCH006D(board_content_no,file_name,file_size,file_type_code,create_time,user_id) VALUES( %s, %s, %s,%s, now(), %s)",[board_content_no,file_url,f.size,extension,request.POST.get('user_id', False)])
            
            #내용안의 이미지링크 추출
            parser = MyHTMLParser() 
            content = request.POST.get('content', False)
            parser.feed(content)

            if parser.get_image_set() :
                for url in parser.get_image_set():  
                    extension = 'IMG'
                    file_url = 	url.replace("/mychurch", "")				
                    data = LSCH006D.objects.create(board_content_no=board_content.board_content_no, file_name=file_url, file_size=0, file_type_code=extension, download_count=0, user_id=request.user.member_id )

            url = (("%s?page=%s") % (reverse('mychurch:board_list', args=[board_no]), page))
            return redirect(url) 
        else:
            form = BoardForm({'file_attach_yn':request.POST.get('file_attach_yn', False)})
         
            return render(request, 'mychurch/board/board_write.html',{
            'form': form, 	# 검증에 실패시 form.error 에 오류 정보를 저장하여 함께 렌더링
            'board_no':board_no,
            'user_id':request.user.member_id,
            'file_attach_yn':board_conf.file_attach_yn,
            'page':page
            })
 