"""03. 기초(Basics) - 07) 툴바 만들기"""

'''
URL from : https://wikidocs.net/21932
메뉴가 앱에서 사용된느 모든 명령의 모음이라면, 툴바(toolbar)는 자주 사용하는 명령들을 더 편리하게 사용할 수 있도록 한다.
본 스크립트에서는 앱을 종료하는 'exitAction'이 하나 포함된 툴바를 만들어보자
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
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q') 
        exitAction.setStatusTip('Exit application') 
        exitAction.triggered.connect(qApp.quit)
        '''
        QAction 객체를 하나 생성한다. 이 객체는 아이콘(exit.png), 라벨('Exit')을 포함하고, 단축키(Ctrl+Q)를 통해 실행 가능하다.
        상태바에 메세지('Exit application')를 보여주고, 클릭 시 생성되는 시그널은 quit() 메소드에 연결되어 있다.
        '''

        self.statusBar()

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        # addToolbar()를 이용해서 툴바를 만들고, addAction()을 이용해서 툴바에 exitAction 동작을 추가한다 

        self.setWindowTitle('Toolbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())