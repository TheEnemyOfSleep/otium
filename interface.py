from PySide2 import QtWidgets, QtCore, QtGui
from source import timeline


class CustomMenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent, app):
        super(CustomMenuBar, self).__init__(parent)
        self.master = parent
        self.app = app


class MainInterface(QtWidgets.QWidget):
    def __init__(self, parent, app):
        super(MainInterface, self).__init__(parent)
        self.master = parent
        self.app = app

        self.set_style()
        self.create_menubar()
        self.create_graphics_widgets()

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

        fast_save_project_act = QtWidgets.QAction('Save', self)
        fast_save_project_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/SaveIco(LightTheme).svg'))
        fast_save_project_act.setShortcut('Ctrl+S')
        full_save_project_act = QtWidgets.QAction('Save As...', self)
        full_save_project_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/SaveAsIco(LightTheme).svg'))
        full_save_project_act.setShortcut('Ctrl+Shift+S')

        pref_act = QtWidgets.QAction('Preferences...', self)
        pref_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/SettingsIco(LightTheme).svg'))

        quit_act = QtWidgets.QAction('Quit', self)
        quit_act.setIcon(QtGui.QIcon('source/style/icons/light_theme/ExitIco(LightTheme).svg'))
        quit_act.setShortcut('Ctrl+Q')

        # Add actions to menus
        file.addAction(new_project_act)
        file.addAction(open_project_act)

        file.addSeparator()

        file.addAction(fast_save_project_act)
        file.addAction(full_save_project_act)

        file.addSeparator()

        file.addAction(pref_act)

        file.addSeparator()

        file.addAction(quit_act)

    def create_graphics_widgets(self):
        main_layout = QtWidgets.QGridLayout()

        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 30, 0, 0)

        timeline_obj = timeline.TimeObject(self.master)

        buffer_task_frame = TaskFrame()

        buffer_settings_frame = QtWidgets.QFrame()
        buffer_settings_frame.setObjectName('BufferSet')
        buffer_settings_frame.setMaximumWidth(450)

        main_layout.addWidget(buffer_task_frame, 0, 0)
        main_layout.addWidget(buffer_settings_frame, 0, 1)
        main_layout.addWidget(timeline_obj, 1, 0, 1, 2)
        self.setLayout(main_layout)


class TaskFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('Task')

        # Make view task boards
        self.view = TaskBoardsView(self)

        # Make scene task boards
        self.scene = TaskBoardsScene()
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())

        self.view.setScene(self.scene)

        # Code for create task boards
        fm = QtGui.QFontMetrics(QtGui.QFont("Ubuntu", 22, QtGui.QFont.Bold))
        text = 'Worktime(Python)'
        fm.width(text)
        task_item = TaskItem(QtCore.QRectF(10, 10, fm.width(text) + 10, 65), color=QtGui.QColor('#A33CDE'), text=text)
        self.scene.addItem(task_item)

    def resizeEvent(self, *args, **kwargs):
        self.view.setGeometry(0, 0, self.width(), self.height())


class TaskItem(QtWidgets.QGraphicsRectItem):
    # Set default parameters
    color = QtGui.QColor(QtCore.Qt.red)
    inactive_color = QtGui.QColor()
    text = 'Name'
    state = True

    def __init__(self, rect, **kwargs):
        super().__init__(rect)
        self.rect = rect

        # Set flags
        # self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        # self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        # self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

        # Parameters for ActionItem
        for key, value in kwargs.items():
            if str(key) == 'color' or key == 'background':
                self.color = value

            if str(key) == 'name' or str(key) == 'text':
                self.text = value

        # print('x:{}, y:{}, width:{}, height:{}'.format(rect.x(), rect.y(), rect.width(), rect.height()))

    def paint(self, painter=QtGui.QPainter(), option=QtWidgets.QStyleOptionGraphicsItem(),
              widget=None):
        # Set color for active and non-active element
        if self.state is False:
            self.inactive_color.setHsv(self.color.hue(), self.color.saturation()-50, self.color.value()-50, 255)
            brush = QtGui.QBrush(self.inactive_color)
        else:
            brush = QtGui.QBrush(self.color)
        # Draw item element for graphics item
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        padding = 10

        # Draw main block
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect, 24.0, 24.0)

        # Draw text for task item
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont("Ubuntu", 22))
        painter.drawText(self.rect.x() + padding, self.rect.y(),
                         self.rect.width() - padding, self.rect.height(),
                         QtCore.Qt.AlignCenter, self.text)

    def mousePressEvent(self, *args, **kwargs):
        self.state = False
        self.update()
        print('Press')

    def mouseMoveEvent(self, *args, **kwargs):
        print('Move')

    def mouseReleaseEvent(self, *args, **kwargs):
        self.state = True
        self.update()
        print('Release')


class TaskBoardsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)

        self.showFullScreen()

    def drawBackground(self, painter, rect):
        brush = QtGui.QBrush(QtGui.QColor('#a5a5a5'))

        painter.fillRect(rect, brush)


class TaskBoardsScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ActWidget(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('Act')

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setStretch(0, 0)
        self.main_layout.setSpacing(0)

        self.task_name_lbl = QtWidgets.QLabel('Name')
        self.task_name_lbl.setObjectName('ActName')
        self.task_name_lbl.setToolTip('Name of action')

        self.task_lbl = QtWidgets.QLabel('Task: Lorem ipsum dolor sit amet')
        self.task_lbl.setObjectName('ActLbl')

        # Commentary block
        self.commentary_widget = QtWidgets.QWidget()
        self.commentary_widget.setContentsMargins(0, 0, 0, 0)
        self.child_layout = QtWidgets.QHBoxLayout()
        self.child_layout.setStretch(0, 0)
        self.child_layout.setSpacing(0)
        self.child_layout.setMargin(0)

        self.addparams_widget = QtWidgets.QWidget()
        self.additional_layout = QtWidgets.QVBoxLayout()
        self.additional_layout.setStretch(0, 0)
        self.additional_layout.setSpacing(0)
        self.additional_layout.setMargin(0)
        self.additional_layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.status_lbl = QtWidgets.QLabel('Active')
        self.status_lbl.setObjectName('Status')

        self.pass_time_lbl = QtWidgets.QLabel('Passed: 2:20')
        self.pass_time_lbl.setObjectName('Status')

        self.commentary_lbl = QtWidgets.QLabel('Commentary: bla bla bla')
        self.commentary_lbl.setObjectName('CommentLbl')

        self.main_layout.addWidget(self.task_name_lbl)
        self.main_layout.addWidget(self.task_lbl)
        self.main_layout.addWidget(self.commentary_widget)

        self.child_layout.addWidget(self.commentary_lbl)
        self.child_layout.addWidget(self.addparams_widget)

        self.additional_layout.addWidget(self.status_lbl)
        self.additional_layout.addWidget(self.pass_time_lbl)

        self.setLayout(self.main_layout)
        self.commentary_widget.setLayout(self.child_layout)
        self.addparams_widget.setLayout(self.additional_layout)

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
