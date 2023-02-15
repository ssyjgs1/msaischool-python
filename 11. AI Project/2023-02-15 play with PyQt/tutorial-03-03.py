"""03. 기초(Basics) - 03) 창 닫기"""

'''
URL from : https://wikidocs.net/21927
창을 닫는 가장 간단한 방법은 타이틀바에서 제공하는 X 버튼을 클릭하는 일이다.
본 스크립트에서는 프밍을 통해 Quit 버튼을 만들고 클릭해서 창을 닫아보자
'''

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication # QtCore 모듈 - QCoreApplication 클래스 불러오기


class MyApp(QWidget) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        btn = QPushButton('Quit', self)
        # 푸시 버튼 만들기
        # 이 버튼은 QPushButton 클래스의 인스턴스이다.
        # QPushButton('ㅁㅁ', ㅇㅇ)라는 이 생성자의 첫 번째 파라미터에는 버튼에 표시될 텍스트, 두 번재 파라미터에는 버튼이 위치할 부모 위젯을 입력함

        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)
        # PyQt5에서의 이벤트 처리는 시그널과 슬롯 메카니즘으로 이루어진다
        # 버튼(btn)을 클릭하면 'clicked' 시그널이 만들어진다
        # instance() 메소드는 현재 인스턴스를 반환한다
        # clicked 시그널은 앱을 종료하는 quit() 메소드에 연결된다
        # 이렇게 발신자(sender)와 수신자(receiver)의 두 객체 간에 communication이 이루어진다
        # 본 예제에서 sender는 푸시 버튼(btn)이고, 수신자는 앱 객체(app)다

        self.setWindowTitle('Quit Button')
        self.setGeometry(300, 300, 300, 200)
        self.show()


# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())