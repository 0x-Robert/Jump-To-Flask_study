# 점프 투 플라스크 스터디
## 지속적 개발/개선 프로젝트 - 플라스크이용




#### 프로젝트 설정

* 우리나라 시간으로 동기화
```
sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
```

****


* 우분투 업데이트
```
sudo apt update
```

****


* 파이썬 가상환경을 제공하는 python3-venv 설치

```
sudo apt install python3-venv
```




****




* 가상환경 프로젝트 설정

```
mkdir projects
mkdir venvs
cd venvs
python3 -m venv myproject

cd myproject
cd bin
. activate  | source activate
```

****


* 필요한 패키지 설치

```
pip install wheel
pip install Flask
pip install Flask-Migrate
pip install Flask-WTF
pip install email_validator
pip install Flask-Markdown
```

****

#### 플라스크 환경변수 설정
* 리눅스/맥 설정
``` 
!/bin/bash
cd /Users/pahkey/projects/myproject
source /Users/pahkey/venvs/myproject/bin/activate
```


* 윈도우 사용시
```
cd myproject\venv
myproject.cmd

myproject.cmd 파일 내용
@echo off
cd C:\Users\smart\PycharmProjects\myproject\
set FLASK_APP=pybo
set FLASK_ENV=development
C:\Users\smart\PycharmProjects\myproject\venv\Scripts\activate
```
