from PySide2 import QtWidgets, QtCore, QtGui


class TimeObject(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setMargin(0)

        self.setMinimumHeight(80)
        self.setMaximumHeight(180)

        timeline_frame = TimelineWidget()

        timeline_param = QtWidgets.QFrame()
        timeline_param.setObjectName('BufferParam')
        timeline_param.setFixedHeight(30)

        main_layout.addWidget(timeline_frame)
        main_layout.addWidget(timeline_param)
        self.setLayout(main_layout)


class TimelineWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(50)
        self.setMaximumHeight(150)

        self.setObjectName('Timeline')
        # Scenes and viewers
        self.scene = TimelineScene()

        self.view = TimelineView(self.scene, self)
        self.view.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.view.setScene(self.scene)

        # Pens and brushes
        blackPen = QtGui.QPen(QtGui.QColor('#424242'))
        blackPen.setWidth(2)

        rect_item = ActItem(QtCore.QRectF(0, 30, 300, 115), color=QtGui.QColor('#A33CDE'))

        self.scene.addItem(rect_item)

        timeline_line = self.scene.addLine(345, 0, 345, 145, blackPen)
        timeline_line.setZValue(100)

    def resizeEvent(self, *args, **kwargs):
        # print('width:{}, height:{}'.format(self.width(), self.height()))
        self.view.setGeometry(0, 0, self.width(), self.height())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Backspace:
            print(self.height())


class ActItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, rect, **kwargs):
        super().__init__(rect)
        self.rect = rect

        # Set flags
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

        # Action item parameters
        self.color = QtGui.QColor(QtCore.Qt.red)

        # Parameters for ActionItem
        for key, value in kwargs.items():
            if str(key) == 'color' or key == 'background':
                self.color = value

        # Set flag for itemChange function;
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        # print('x:{}, y:{}, width:{}, height:{}'.format(rect.x(), rect.y(), rect.width(), rect.height()))

    def paint(self, painter=QtGui.QPainter(), option=QtWidgets.QStyleOptionGraphicsItem(), widget=None):
        # Draw item element for graphics item
        brush = QtGui.QBrush(self.color)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)

        padding = 10
        # Draw main block
        painter.setBrush(brush)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(self.rect, float(12), float(12.0))



        # Draw action name lbl
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont("Ubuntu", 22))
        painter.drawText(self.rect.x() + padding, self.rect.y() + padding,
                         self.rect.width() - padding, self.rect.height(),
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, 'Worktime(Python)')

        # Draw task lbl
        painter.setFont(QtGui.QFont("Ubuntu", 14))
        painter.drawText(self.rect.x() + padding, self.rect.y() + 12.5,
                         self.rect.width() - padding, self.rect.height() - 10,
                         QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                         "Task: Lorem ipsum dolor sit amet")

        # # Draw commentary lbl
        # painter.drawText(self.rect.x() + padding, self.rect.y() - 10,
        #                  self.rect.width()- padding, self.rect.height(),
        #                  QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom,
        #                  "Commentary: bla bla bla")

        painter.setBrush(QtCore.Qt.green)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(self.rect.bottomRight().x() - 20, self.rect.bottomRight().y() - 34, 10, 10)

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtCore.Qt.white)
        painter.setFont(QtGui.QFont("Ubuntu", 12))
        painter.drawText(self.rect.x() - 25, self.rect.y() - 20,
                         self.rect.width(), self.rect.height(),
                         QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom,
                         "Active")

        painter.drawText(self.rect.x() - padding, self.rect.y() - 1,
                         self.rect.width(), self.rect.height(),
                         QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom,
                         "Passed: 1:15")

        del(padding)

    def itemChange(self, change, value):
        new_val = QtCore.QPointF()
        past_time_zone = 0
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            if value.x() > past_time_zone:
                if value.x() % 5 != 0:
                    new_val.setX(value.x() + (5 - (value.x() % 5)))
                else:
                    new_val.setX(value.x())
                # return QtCore.QPointF(value.x(), - 0)
                return new_val
            else:
                new_val.setX(0)
                return new_val
        # Accept value for item
        return super().itemChange(change, value)  # Call super


class TimelineView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameStyle(QtWidgets.QFrame.NoFrame)

        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        self.showFullScreen()

    def drawBackground(self, painter, rect):
        background_brush = QtGui.QBrush(QtGui.QColor('#d1d1d1'), QtCore.Qt.SolidPattern)

        painter.fillRect(rect, background_brush)


class TimelineScene(QtWidgets.QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_pattern()

    def create_pattern(self):
        self.clear()
        pen = QtGui.QPen(QtGui.QColor('#424242'))
        pen.setCosmetic(True)

        for x in range(0, 7201, 5):
            line = self.addLine(x, 0, x, 10, pen)
            line.setZValue(-10)
            line.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        i = 0
        for x in range(0, 7201, 300):
            line = self.addLine(x, 0, x, 20, pen)
            line.setZValue(-10)
            text = self.addText('{}:00'.format(i))
            text.setPos(x, 10)
            i += 1

        # test = self.addLine(0, 0, 100, 0, self.pen)
