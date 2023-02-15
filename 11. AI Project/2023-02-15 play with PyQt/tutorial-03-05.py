"""03. 기초(Basics) - 05) 상태바 만들기"""

'''
URL from : https://wikidocs.net/21928
메인 창(main window)은 메뉴바, 툴바, 상태바를 갖는 전형적인 앱 창이다.
우선 QStatusBar를 이용해서 메인 창에 상태바를 하나 만들어보자!
상태바는 앱의 상태를 알려주기 위해 앱 하단에 위치하는 위젯이다.
'''

# 필요한 라이브러리 import
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MyApp(QMainWindow) :
    # self는 MyApp 객체를 뜻한다
    def __init__(self) :
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.statusBar().showMessage('Ready')
        # 상태바는 QMainWindow 클래스의 statusBar() 메소드를 이용해서 만드는데, 이 메소드를 최초로 호출하면 만들어진다.
        # 그 다음 호출부터는 상태바 객체를 반환한다.
        # showMessage() 메소드를 통해 상태바에 보일 메세지를 작성할 수 있다.

        self.setWindowTitle('Statusbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()


# 실행문
if __name__ == '__main__' : # 현재 모듈의 이름이 저장되는 내장 변수
    app = QApplication(sys.argv) # 모든 PyQt5 앱은 앱의 객체를 생성해야 한다.
    ex = MyApp()
    sys.exit(app.exec_())