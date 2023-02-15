"""03. 기초(Basics) - 02) 어플리케이션 아이콘 넣기"""
"""URL from : https://wikidocs.net/21853"""

# 앱 아이콘은 타이틀바 왼쪽 끝에 보일 작은 이미지를 말한다

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


'''창을 하나 띄우면서, 타이틀바의 왼쪽에 작은 아이콘이 나타나도록 해보자'''
class MyApp(QWidget) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.setWindowTitle('Icon') # 타이틀바에 나타나는 창의 제목을 설정함
        self.setWindowIcon(QIcon('web.png'))
        # 앱 아이콘을 설정하는 메소드
        # QIcon 객체 생성 후 보여질 이미지 web.png를 입력(=경로 잡기) 
        self.setGeometry(300, 300, 300, 200)
        # 창의 위치와 크기 설정
        # 앞 두 숫자 = 창의 x, y 위치 결정 | 뒤 두 숫자 = 창의 너비와 높이 결정
        # tutorial-03-01에서 사용했던 move(), resize()를 하나로 합친 것과 같다
        self.show() # 위젯을 화면에 띄워줌


# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())