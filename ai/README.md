# How to start
1. Python 설치 : v3.8.X
2. 필요한 모듈 설치 : pip install -r requirements.txt
3. run_server.cmd 스크립트 실행 또는 python manage.py runserver 명령어 실행
4. [http://127.0.0.1:8000] 로 서버 실행 확인

# Descriptions
1. 구현할 python 코드 위치 (경로 변경될 수 있음)
    - %GIT_REPO%\ai\AxperIance\service\*.py
2. API 정보
	1. POST http://127.0.0.1:8000/filmrate/learning (Content-Type: application/json)
		- sample : {"url": "", "user_id": "", "user_pw": ""}
	2. POST http://127.0.0.1:8000/filmrate/predict (Content-Type: application/json)
		- sample : {"content": "이 영화 진짜 존잼이다 하하하하핳"}

# Crawling 환경설정
1.  필요한 모듈 설치 
    1. pip3 install selenium==3.141
    2. apt-get update
    3. apt install chromium-chromedriver정
    
# Modeling 환경설정
1.  필요한 모듈 설치
    1. pip install konlpy
    2. pip install tensorflow
