"""03. 기초(Basics) - 04) 툴팁 나타내기"""

'''
URL from : https://wikidocs.net/21860
툴팁은 어떤 위젯의 기능을 설명하는 등의 역할을 하는 말풍선 형태의 도움말이다.
위젯에 있는 모든 구성 요소에 대해서 툴팁이 나타나도록 할 수 있는데, setToolTip() 메소드를 이용해서 위젯에 툴팁을 만들어보자!
본 예제에서는 두 개의 PyQt5 위젯에 대한 툴팁을 보여줄건데, 푸시 버튼(btn)과 창(MyApp) 위젯에 마우스를 올리면 설정한 텍스트가 툴팁으로 나타난다
'''

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtGui import QFont

class MyApp(QWidget) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        QToolTip.setFont(QFont('D2Coding', 10)) # 툴팁에 사용할 글꼴, 크기 설정
        self.setToolTip('This is a <b>QWidget</b> widget') # 툴팁에 표시될 텍스트 입력

        btn = QPushButton('Button', self) # 푸시 버튼을 하나 만들어주자
        btn.setToolTip('This is a <b>QPushButton</b> widget') # 툴팁 텍스트를 달아주자
        btn.move(50, 50) # 버튼의 위치와 크기를 설정한다
        btn.resize(btn.sizeHint()) # 버튼을 적절한 크기로 설정하도록 도와준다

        self.setWindowTitle('Tooltips')
        self.setGeometry(300, 300, 300, 200)
        self.show()


# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())