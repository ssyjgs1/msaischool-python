"""03. 기초(Basics) - 01) 창 띄우기"""
"""URL from : https://wikidocs.net/21920"""

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QWidget # pip install PyQt5
# 기본적인 UI 구성요소를 제공하는 위젯(클래스)들은 PyQt5.QtWidgets 모듈에 포함되어 있다.


class MyApp(QWidget) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.setWindowTitle('My First Application') # 타이틀바에 나타나는 창의 제목을 설정함
        self.move(300, 300) # 위젯을 스크린의 x=300px, y=300px의 위치로 이동시킴
        self.resize(400, 200) # 위젯의 크기를 너비 400px, 높이 200px로 조절함
        self.show() # 위젯을 화면에 띄워줌


# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())