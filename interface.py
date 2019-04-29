from PySide2 import QtWidgets, QtCore, QtGui


class CustomMenuBar(QtWidgets.QMenuBar):

    def __init__(self, parent, app):
        super(CustomMenuBar, self).__init__(parent)
        self.master = parent
        self.app = app

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        if int(self.app.mouseButtons()) == 1:
            print('1')

class MainInterface(QtWidgets.QWidget):

    def __init__(self, parent, app):
        super(MainInterface, self).__init__(parent)
        self.master = parent
        self.app = app

        self.set_style()
        self.create_menubar()

    def set_style(self):
        QtGui.QFontDatabase.addApplicationFont('source/style/fonts/Ubuntu-B.ttf')
        with open('source/style/night_theme_def.qss', 'r') as ssh:
            self.master.setStyleSheet(ssh.read())

    def test(self):
        print('dsadsada')

    def create_menubar(self):
        self.bar = CustomMenuBar(self.master, self.app)

        # Create root menus
        file = self.bar.addMenu('File')
        file.mousePressEvent = self.test

        # Create action to menus
        new_project_act = QtWidgets.QAction('New Project', self)
        new_project_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/CreateIco(LightTheme).svg'))
        # new_project_act.triggered.connect(self.test)
        new_project_act.setShortcut('Ctrl+N')
        open_project_act = QtWidgets.QAction('Open...', self)
        open_project_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/OpenIco(LightTheme).svg'))

        fast_save_projcet_act = QtWidgets.QAction('Save', self)
        fast_save_projcet_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/SaveIco(LightTheme).svg'))
        fast_save_projcet_act.setShortcut('Ctrl+S')
        full_save_project_act = QtWidgets.QAction('Save As...', self)
        full_save_project_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/SaveAsIco(LightTheme).svg'))
        full_save_project_act.setShortcut('Ctrl+Shift+S')

        pref_act = QtWidgets.QAction('Preferences...', self)
        pref_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/SettingsIco(LightTheme).svg'))
        load_factory_act = QtWidgets.QAction('Load Factory Settings', self)

        quit_act = QtWidgets.QAction('Quit', self)
        quit_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/ExitIco(LightTheme).svg'))
        quit_act.setShortcut('Ctrl+Q')

        # Add actions to menus
        file.addAction(new_project_act)
        file.addAction(open_project_act)

        file.addSeparator()

        file.addAction(fast_save_projcet_act)
        file.addAction(full_save_project_act)

        file.addSeparator()

        file.addAction(pref_act)
        file.addAction(load_factory_act)

        file.addSeparator()

        file.addAction(quit_act)
