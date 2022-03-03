# ForPresentation_Django

## 시연영상

[**2020ESWContest_자유공모_1023_FORPT_시연동영상(임베디드SW경진대회)**](https://www.youtube.com/watch?v=RYwH7PK3ZA0)

## 영상 설명

자신이 발표하고자 하는 과목명으로된 방에서 초대를 받은 상태라면 “참여중”에 해당 과목명으로 된 방이 보이게됩니다. 그리고 그 방에 들어가서 사용자는 간단한 설명과 함께 발표자료를 업로드를 할 수 있습니다 이때 사용자가 업로드한 파일을 Unity측에서 접근하여 발표자료를 순서대로 읽어서 가져와야하는데 사용자가 업로드한 파일명이 규칙적이지 않기 때문에 Unity측에서 발표자료를 접근하기가 어려웠습니다. 그래서 이를 해결하기 위해 사용자의 발표자료가 서버에 업로드될 때 “~/media/files/ppts/{학번} __ {과목명} __ {발표자료순서}. {확장자}”  과 같이 정해진 규칙으로 서버내에서 자체적으로 파일명을 바꾸어 업로드함으로써 Unity에서 파일을 접근할때 훨씬 편하게 접근해서 발표자료를 순서대로 가져올 수 있게 구현하였습니다.

## 함수별 기능명세

### Django)

- **register( ):**  HTTP Request가 “GET”일 경우 사용자의 정보를 입력할 수 있는 register.html을 보여준다. 만약 “POST”일 경우 입력된 정보를 데이터베이스에 반영한다.
사용자가 입력한 정보가 회원가입 형식과 일치하지 않을 경우 오류 메세지를 통해   알맞은 형식으로 회원 가입할 수 있도록 유도한다.
- **login( ):** HTTP Request가 “GET”일 경우 사용자가 정보를 입력할 login.html을 보여준다.
만약 “POST”일 경우 사용자가 입력한 정보와 데이터 베이스에 있는 정보와 비교하여 일치할 경우에만 해당 유저의 데이터 베이스 정보를 index.html에 반영하여 보여준다.
- **logout():** HTTP Request의 세션에서 ‘user’을 삭제한 이후 home.html을 보여준다.
file_list() – 로그인 한 ‘user’의 파일정보를 데이터 베이스로부터 가져와서 file_list.html에 반영하여 보여준다.
- **room_list():** Room객체의 데이터 베이스로부터 모든 교실 정보를 가져와서 사용자가 이미 참여한 교실이 있다면 해당 교실들을 제외하고 나머지 선택가능한 교실목록을 보여준다. 만약 사용자가 참여한 교실이 없다면 Room객체의 모든 교실정보가 있는 교실목록을 보여준다.
- **make_room():** HTTP Request가 “GET”일 경우 사용자가 교실정보를 입력할 수 있는 make_room.html을 보여준다. 만약 “POST”일 경우 새로운 Room객체를 생성하여 사용자가 입력한 교실 정보(제한인원, 교실이름)를 Room객체에 저장한다.
- **Index():** 로그인 한 ‘user’가 관리중인 방, 참여중인 방, 학번 등의 정보를 index.html여 반영하여 보여준다.
- **Room_delete(pk):** parameter로 전달받은 pk와 같은 pk를 가진 Room객체를 삭제한 후 변경 내용을 데이터 베이스에 반영한다.
- **File_delete(pk):** parameter로 전달받은 pk와 같은 pk를 가진 File객체를 삭제한 후 변경내용을 데이터 베이스에 반영한다.
- **Invite(pk):** parameter로 전달받은 pk와 같은 pk를 가진 Room객체에 invite.html에서 초대된 user를 추가한 후 변경내용을 데이터 베이스에 반영한다.
- **Room_exit(pk):** parameter로 전달받은 pk와 같은 pk를 가진 Room객체를 데이터베이스에서 삭제한 후 index.html에 반영하여 보여준다.
- **Room_join(pk):** parameter로 전달받은 pk와 같은 pk를 가진 Room객체의 student(참여학생) 속성에 로그인한 ‘user’을 추가한 후 변경내용을 데이터 베이스에 반영한다.
- **Student_invite(pk):** index.html에서 ‘초대’버튼을 누른 Room객체의 student(참여학생) 속성에 함수의 parameter로 전달받은 pk와 같은 pk를 가진 User객체를 추가한 다음 변경내용을 데이터 베이스에 반영한다.
- **Room_choice(pk):** parameter로 전달받은 pk와 같은 pk를 가진 Room객체에서 ‘user’의 파일정보를 room_enter.html에 반영한다.
- **Upload_file():** HTTP Request가 “GET”인 경우 파일정보(comment, 파일경로)를 업로드할 수 있는 upload_file.html로 연결한다. 만약 “POST”인 경우 사용자가 업로드한 파일정보를 데이터 베이스에 반영한다.
