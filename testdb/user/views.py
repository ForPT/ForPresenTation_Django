from django.shortcuts import render, redirect

from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User
# add from ko
from django.views.generic import TemplateView, ListView ,UpdateView ,DetailView , DeleteView
from django.core.files.storage import FileSystemStorage
from .forms import FileForm
from .models import File
from .forms import RoomForm
from .models import Room
import os
from django.urls import reverse_lazy
from django.urls import reverse

def home(request):
    if request.session.get('user'):
        request.session.pop('user')
    else :
        pass
    user_id=request.session.get('user')
    if user_id:
        user_id = request.session.get('user')
        user_info = User.objects.get(pk=user_id) #학번 201700000
        rooms = Room.objects.filter(professor=user_info) # 관리중인 사람만 "관리중"에 뜨도록 만듬
        joined_room_list = user_info.joined_room.split('/')
        final_joined_room_list =[]
        if joined_room_list != [''] and joined_room_list:
            for i in joined_room_list:
                final_joined_room_list.append(Room.objects.get(room_name=i))
        all_rooms = Room.objects.all()
        students = User.objects.all()
        return render(request, 'index.html', {
            'students' : students,
            'joined_rooms' : final_joined_room_list,
            'rooms' : rooms,
            'all_rooms' : all_rooms,
            'user_id' : user_info,
            'user_info' : user_info.username
        })
    return render(request, 'home.html')

def login(request):
    response_data = {}

    if request.method == "GET" :
        return render(request, 'login.html')

    elif request.method == "POST":
        login_userid = request.POST.get('userid', None)
        login_password = request.POST.get('password', None)


        if not (login_userid and login_password):
            response_data['error']="아이디와 비밀번호를 모두 입력해주세요."
        else :
            myuser = User.objects.get(userid=login_userid) #db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            if login_password == myuser.password: 
                request.session['user'] = myuser.id #세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                #세션 user라는 key에 방금 로그인한 id를 저장한것.
                print('---------------Success Login-------------')
                user_id = request.session.get('user')
                user_info = User.objects.get(pk=user_id) #학번 201700000
                rooms = Room.objects.filter(professor=user_info) # 관리중인 사람만 "관리중"에 뜨도록 만듬
                joined_room_list = user_info.joined_room.split('/')
                final_joined_room_list =[]
                if joined_room_list != [''] and joined_room_list:
                    print('enter !!')
                    for i in joined_room_list:
                        final_joined_room_list.append(Room.objects.get(room_name=i))
                all_rooms = Room.objects.all()
                students = User.objects.all()
                return render(request, 'index.html', {
                    'students' : students,
                    'joined_rooms' : final_joined_room_list,
                    'rooms' : rooms,
                    'all_rooms' : all_rooms,
                    'user_id' : user_info,
                    'user_info' : user_info.username
                })
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

        return render(request, 'login.html',response_data)

def logout(request):
    request.session.pop('user')
    return redirect('/')

def register(request):
    if request.method == "GET":
        res_data = {}
        return render(request,'register.html')

    elif request.method == "POST":
        userid = request.POST.get('userid',None)
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        re_password = request.POST.get('re_password',None)
        res_data = {}
        if not (userid and username and password and re_password) :
            res_data['error'] = '모든 값을 입력해야 합니다'
        elif password != re_password :
            res_data['error'] = '비밀번호가 다릅니다'
        else :
            user = User(userid=userid, username=username, password=password)
            user.save()
            return render(request, 'home.html')
        return render(request, 'register.html', res_data)

## add for file
def file_list(request):
    user_id=request.session.get('user')
    user_info = User.objects.get(pk=user_id)
    getFiles = File.objects.filter(number=user_info) # 로그인 할때 마다 바뀜
    return render(request, 'file_list.html',{
        'getFiles' : getFiles,
        'user_id' : user_info,
        'user_info' : user_info.username
    })

def room_list(request):
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id)
    rooms = Room.objects.all()
    if user_info.joined_room :
        joined_room_list = user_info.joined_room.split('/')
        all_room_list = []
        final_room_list = []
        for r in rooms:
            all_room_list.append(Room.objects.get(room_name=r).room_name)
        print('all_room_list before remove : ', all_room_list)
        for j in joined_room_list:
            all_room_list.remove(j)
        print('room_list/joined_room_list is ', joined_room_list)
        print('room_list/rooms is ', rooms)
        print('all_room_list after remove : ', all_room_list)
        for f in all_room_list: # 이미 참여중인 방이 제외된 참여가능 목록 만들기
            final_room_list.append(Room.objects.get(room_name=f)) 
        return render(request, 'room_list.html', {
            'rooms' : final_room_list,
            'user_id' : user_info,
            'user_info' : user_info.username
            })
    else :
        return render(request , 'room_list.html', {
            'rooms' : rooms, # 모든 방
            'user_id' : user_info,
            'user_info' : user_info.username,
        })


def make_room(request):
    user_id = request.session.get('user') #id 값
    user_info = User.objects.get(pk=user_id) # 학번
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        room_limit = request.POST.get('limit', None)
        room_name = request.POST.get('room_name', None)
        rooms = Room(limit=room_limit, room_name=room_name, student=user_info.username, professor=user_info)
        # 관리 중에 추가
        if user_info.managed_room : # 이미 관리중인 방이 있다면
            if user_info.joined_room: # 관리 중 이면, 참여 중에도 추가
                user_info.managed_room = user_info.managed_room + '/' + room_name
                user_info.joined_room = user_info.joined_room + '/' + room_name
            else :
                user_info.managed_room = user_info.managed_room + '/' + room_name
                user_info.joined_room = room_name
        else :
            if user_info.joined_room:
                user_info.managed_room = room_name
                user_info.joined_room = user_info.joined_room + '/' + room_name
            else :
                user_info.managed_room = room_name
                user_info.joined_room = room_name
        user_info.save()
        if form.is_valid():
            rooms.save()
            return redirect('index')
    else :
        form = RoomForm()
    return render(request, 'make_room.html', {
        'form' : form,
        'user_id' : user_info,
        'user_info' : user_info.username
    })

def index(request):
    print('---------------index-------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id) #학번 201700000
    rooms = Room.objects.filter(professor=user_info) # 관리중인 사람만 "관리중"에 뜨도록 만듬
    joined_room_list = user_info.joined_room.split('/')
    final_joined_room_list =[]
    if joined_room_list != [''] and joined_room_list:
        print('enter !!')
        for i in joined_room_list:
            final_joined_room_list.append(Room.objects.get(room_name=i))
    all_rooms = Room.objects.all()
    students = User.objects.all()
    return render(request, 'index.html', {
        'students' : students,
        'joined_rooms' : final_joined_room_list,
        'rooms' : rooms,
        'all_rooms' : all_rooms,
        'user_id' : user_info,
        'user_info' : user_info.username
    })

def room_delete(request ,pk): #room_delete ,managed_room 수정
    print('-----------------room_delete---------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id) # 학번
    room = Room.objects.get(pk=pk) #parameter pk, "지울 방"
    room_name = room.room_name
    print('room_delete/room_name is ', room_name) # 지울려고하는 방이름
    print('index/joined_room.split(/) : ', user_info.joined_room.split('/')) # 참여중인 방목록 list로 보여줌
    print('index/managed_room.split(/) : ', user_info.managed_room.split('/')) # 관리중인 방목록 list로 보여줌
    managed_room_list = user_info.managed_room.split('/') # 관리중인 방에서 room_delete()
    managed_room_list.remove(room_name)
    final_managed_room_list = '/'.join(managed_room_list)
    print('room_delete/final_room_list is ', final_managed_room_list)
    user_info.managed_room = final_managed_room_list

    joined_room_list = user_info.joined_room.split('/') # 참여중인 방에서 room_delete()
    joined_room_list.remove(room_name)
    final_joined_room_list = '/'.join(joined_room_list)
    user_info.joined_room = final_joined_room_list
    user_info.save()
    room.delete()
    return redirect('index')

def file_delete(request, pk): # pk 는 지울파일
    print('---------------------file_delete-----------------------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id) # 학번
    delete_file = File.objects.get(pk=pk)# 지울파일
    print('delete_file is ', delete_file)
    room = Room.objects.get(room_name=delete_file.entered_room)

    room_student_list = room.student.split(',')
    index = room_student_list.index(user_info.username) # room.page를 수정하기 위해 필요한 index

    room_page_list = room.page.split('/')
    temp = int(room_page_list[index])
    temp -= 1
    room_page_list[index] = str(temp)
    final_room_page_list = '/'.join(room_page_list)
    room.page = final_room_page_list
    room.save()

    delete_file.delete() # 파일 객체 지우기
    return redirect('file_list')

def join(request):
    print('---------------------join-----------------------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id)
    rooms = Room.objects.all()
    return render(request, 'join.html', {
        'rooms' : rooms,
        'user_id' : user_info,
        'user_info' : user_info.username
    })

def invite(request, pk): # pk 는 room.id
    print('---------------invite-----------------------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id) # 학번 (ex. 2017000000)
    room = Room.objects.get(pk=pk) # 초대 방
    print('초대할 방 정보 는 ', room)
    print('초대할 방 이름 은 ', room.room_name)

    user = User.objects.all() # 모든 유저
    if room.student:
        joined_student_list = room.student.split(',')
    else :
        joined_student_list = []
    print('joined_student_list is ', joined_student_list)
    all_student_list = []
    final_student_list = []
    request.session['invite_room'] = room.room_name
    for u in user:
        all_student_list.append(u.username)
    print('all_student_list is before remove', all_student_list)
    for d in joined_student_list:
        all_student_list.remove(d)
    print('all_student_list is after remove', all_student_list)
    if all_student_list.count(user_info.username) >= 1: # user_info.username 이 final_student_list에 없어야 되기때문
        all_student_list.remove(user_info.username)
    for f in all_student_list:
        final_student_list.append(User.objects.get(username=f))
    print('all_student_list is ', all_student_list)
    return render(request, 'invite.html',{
        'students' : final_student_list,
        'user_id' : user_info,
        'user_info' : user_info.username
    })

def room_exit(request, pk):
    print('---------------------room_exit-----------------------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id) # 학번
    room = Room.objects.get(pk=pk) #parameter pk, "나갈 방"
    room_name = room.room_name
    joined_room_list = user_info.joined_room.split('/')
    joined_room_list.remove(room_name)
    final_room_list = '/'.join(joined_room_list)
    user_info.joined_room = final_room_list
    user_info.save()

    room_student_list = room.student.split(',')
    index = room_student_list.index(user_info.username) # room.page를 수정하기 위해 필요한 index
    room_student_list.remove(user_info.username)
    final_student_list = ','.join(room_student_list)
    room.student = final_student_list

    room_page_list = room.page.split('/')
    room_page_list.pop(index) # 해당원소의 page 삭제
    final_room_page_list = '/'.join(room_page_list)
    room.page = final_room_page_list
    room.save()
    # 파일을 지우자
    all_file = File.objects.all()
    for f in all_file:
        if f.name == user_info.username and f.entered_room == room.room_name:
            f.delete()
    return redirect('index')

def room_join(request, pk): # pk 는 room.id
    print('---------------------room_join-----------------------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id) #학번
    room = Room.objects.get(pk=pk)
    if user_info.joined_room :
        if room.student:
            user_info.joined_room = user_info.joined_room + '/' + room.room_name
            room.student = room.student + ',' + user_info.username
        else :
            user_info.joined_room = user_info.joined_room + '/' + room.room_name
            room.student = user_info.username
    else : 
        if room.student:
            user_info.joined_room = room.room_name    
            room.student = room.student + ',' +user_info.username
        else :
            user_info.joined_room = user_info.joined_room + room.room_name
            room.student = user_info.username
    user_info.save()
    if room.page : # 0/0/1
        print('---------if/room.page------------')
        room_page_list = room.page.split('/')
        print('Before room_page_list : ', room_page_list)
        room_page_list.append(str(0))
        final_room_page_list = '/'.join(room_page_list)
        print('After room_page_list : ', final_room_page_list)
        room.page = final_room_page_list
    else : # None
        print('---------------else/room.page------------')
        room.page = str(0)
    room.save()
    return redirect('index')

def student_invite(request, pk): # pk는 student.id
    print('---------------------student_invite-----------------------------')
    user_info = User.objects.get(pk=pk) # 초대당한 학생 학번
    print('student_invite/user_info is ', user_info)
    room_name = request.session.get('invite_room')
    room = Room.objects.get(room_name=room_name)
    print('student_invite/room_name is ', room_name)

    if room.student:
        if user_info.joined_room:
            room.student = room.student + ',' + user_info.username
            user_info.joined_room = user_info.joined_room + '/' + room.room_name
        else :
            room.student = room.student + ',' + user_info.username
            user_info.joined_room = room.room_name
    else :
        if user_info.joined_room:
            room.student = user_info.username
            user_info.joined_room = user_info.joined_room + '/' + room.room_name
        else :
            room.student = user_info.username
            user_info.joined_room = room.room_name
    if room.page : # 0/0/1
        print('---------if/room.page------------')
        room_page_list = room.page.split('/')
        print('Before room_page_list : ', room_page_list)
        room_page_list.append(str(0))
        final_room_page_list = '/'.join(room_page_list)
        print('After room_page_list : ', final_room_page_list)
        room.page = final_room_page_list
    else : # None
        print('---------------else/room.page------------')
        room.page = str(0)
    room.save()
    user_info.save()
    return redirect('index')

def room_choice(request, pk): #room pk
    print('---------------------room_choice-----------------------------')
    user_id = request.session.get('user')
    user_info = User.objects.get(pk=user_id)
    room = Room.objects.get(pk=pk)
    room_name = room.room_name
    request.session['room'] = room_name
    getFiles = File.objects.filter(number=user_info , entered_room=room_name)
    return render(request, 'room_enter.html', {
        'room' : room,
        'user_id' : user_info,
        'user_info' : user_info.username,
        'getFiles' : getFiles,
    })

def upload_file(request):
    print('---------------------upload_file-----------------------------')
    print('upload_file/request is', request)
    user_id = request.session.get('user') 
    room_name = request.session.get('room') #방이름(ex. 정통개)
    room = Room.objects.get(room_name=room_name) #방이름 동일한 Room 객체 생성
    user_info = User.objects.get(pk=user_id) #학번(ex. 201700000)
    getFiles = File.objects.filter(number=user_info)
    room_professor_name = User.objects.get(userid=room.professor).username
    if request.method == 'POST':
        print('--------------------upload_file POST------------------')
        form = FileForm(request.POST, request.FILES)
        comment = request.POST.get('comment',None)
        ppt = request.FILES.get('ppt', None)
        # room 의 page를  file 의 page로 줄때는 int로 줘야댐
        joined_student_list = room.student.split(',')
        room_page_list = room.page.split('/')
        print('Before room_page_list : ', room_page_list)
        print('joined_student_list : ', joined_student_list) # ['a', 'b', 'c']
        index = joined_student_list.index(user_info.username)
        print('index is ', index)
        temp = int(room_page_list[index])
        temp += 1
        room_page_list[index] = str(temp)
        print('After room_page_list : ', room_page_list)
        final_room_page_list = '/'.join(room_page_list)
        room.page = final_room_page_list
        files = File(number=user_info, name=user_info.username, comment=comment, ppt=ppt, entered_room=room_name, page=temp)
        if form.is_valid():
            files.save()
            room.save()
            return redirect('room_choice', pk=room.id)
    else :
        form = FileForm()
    return render(request, 'upload_file.html', {
        'form' : form,
        'user_id' : user_info,
        'user_info' : user_info.username,
        'room_name' : room.room_name,
        'room_professor' : room_professor_name,
    })

def test(request):
    print('-----------------------TEST----------------------')
    form = TestForm()
    if request.method == 'POST':
        print(os.getcwd())
        print("POST method")
        form = TestForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            for count, x in enumerate(request.FILES.getlist("files")):
                def handle_uploaded_file(f):
                    with open(os.path.join(os.getcwd(),"media", f.name),'wb+') as destination:
                        print('os.path is ', os.path.join(os.getcwd(), "media", f.name)) # 파일 저장경로 나옴
                        for chunk in f.chunks():
                            destination.write(chunk)
                handle_uploaded_file(x)
                print(x.name)
            context = {'form':form,}
            return render(request, 'test.html', context)
        
    else:
        form = TestForm()

    return render(request, 'test.html', {'form': form})

class FileUpdateView(UpdateView):
    model = File
    fields = ['comment','ppt']
    success_url = reverse_lazy('user:test')

class FileDeleteView(DeleteView):
    model = File
    success_url = reverse_lazy('user:test')

class FileLV(ListView):
    model = File

class FileDV(DetailView):
    model = File

def modal(request):
    return render(request, 'modal.html')