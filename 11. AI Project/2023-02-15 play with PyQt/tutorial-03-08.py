"""03. 기초(Basics) - 08) 창을 화면의 가운데로"""

'''
URL from : https://wikidocs.net/26684
창을 모니터 화면의 가운데에 띄워보자
'''

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class MyApp(QWidget) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.setWindowTitle('Centering')
        self.resize(500, 350)
        self.center() # center() 메소드를 통해 창이 화면의 가운데에 위치하게 된다
        self.show()

    def center(self) :
        qr = self.frameGeometry() # frameGeometry() 메소드를 이용해 창의 위치와 크기 정보를 가져온다
        cp = QDesktopWidget().availableGeometry().center() # 사용하는 모니터 화면의 가운데 위치를 파악한다
        qr.moveCenter(cp) # 창의 직사각형 위치를 화면의 중심 위치로 이동한다
        
        self.move(qr.topLeft())
        # 현재 창을 화면의 중심으로 이동했던 직사각형(qr)의 위치로 이동시킨다.
        # 결과적으로 현재 창의 중심이 화면의 중심과 일치하게 되어 창이 가운데에 나타나게 된다.

# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())