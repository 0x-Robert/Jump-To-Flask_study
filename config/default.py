import os


'''
default.py 파일 기준으로 C:/project/myproject/config/default.py 에서 os.path.dirname을 2번 사용했으므로
BASE_DIR에는 C:/projects/myproject가 대입된다.

'''

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
