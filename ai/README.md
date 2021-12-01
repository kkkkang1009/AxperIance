# How to start
1. Python 설치 : v3.8.X
2. 필요한 모듈 설치 : pip install -r requirements.txt
3. run_server.cmd 스크립트 실행 또는 python manage.py runserver 명령어 실행
4. [http://127.0.0.1:8000]로 서버 실행 확인

# Descriptions
1. 구현할 python 코드 위치 (경로 변경될 수 있음)
    - %GIT_REPO%\ai\AxperIance\service\*.py
2. API 정보
	2-1. POST http://127.0.0.1:8000/filmrate/learning (Content-Type: application/json)
		- sample : {"url": "", "user_id": "", "user_pw": ""}
	2-2. POST http://127.0.0.1:8000/filmrate/predict (Content-Type: application/json)
		- sample : {"content": "이 영화 진짜 존잼이다 하하하하핳"}
