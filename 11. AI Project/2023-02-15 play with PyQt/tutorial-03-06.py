"""03. 기초(Basics) - 06) 메뉴바 만들기"""

'''
URL from : https://wikidocs.net/21866
다양한 명령들의 모음이 메뉴바(menu bar)에 위치한다
한 개의 메뉴를 갖는 메뉴바를 만들고, 해당 메뉴를 클릭했을 때 앱을 종료하는 기능을 갖도록, 단축키(Ctrl+Q)로도 실행하도록 만들어보자
'''

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import  QIcon

class MyApp(QMainWindow) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        exitAction = QAction(QIcon('exit.png'), 'Exit', self) # 아이콘과 'Exit' 라벨을 갖는 하나의 동작(action)을 만들어주자
        exitAction.setShortcut('Ctrl+Q') # 위의 동작에 대해 단축키를 정의해주자
        exitAction.setStatusTip('Exit application') # 메뉴바에 마우스를 올렸을 때, 상태바에 나타날 상태팁을 setStatuTip() 메소드를 사용해 설정하자
        exitAction.triggered.connect(qApp.quit) # 동작을 선택했을 때, 생성된(triggered) 시그널이 QApplication 위젯의 quit() 메소드에 연결되고, 앱을 종료시킨다

        self.statusBar()

        menubar = self.menuBar() # menuBar() 메소드는 메뉴바를 생성한다
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File') # 'File' 메뉴를 하나 만들어주자.
        # 'F' 앞에 앰퍼샌드(&)가 있으므로 'Alt+F'가 File 메뉴의 단축키가 된다. 만약 'i'의 앞에 앰퍼샌드를 넣으면 'Alt+I'가 단축키가 된다
        filemenu.addAction(exitAction) # 만든 메뉴에 'exitAction' 동작을 추가해주자

        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())