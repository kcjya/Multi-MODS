import sys
from PyQt5.QtCore import Qt, QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QFont,QColor,QTextFormat
from PyQt5.QtWidgets import QTextEdit, QApplication
from PyQt5.QtWidgets import QWidget,QPushButton


class Editor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("微软雅黑", 9, 2))
        self.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        self.lineNumberArea = lineNumPaint(self)
        self.document().blockCountChanged.connect(self.updateWidth)
        self.verticalScrollBar().valueChanged.connect(self.lineNumberArea.update)
        self.textChanged.connect(self.lineNumberArea.update)
        self.cursorPositionChanged.connect(self.lineNumberArea.update)
        self.updateWidth()


    def lightCurrentRow(self, line, color=Qt.lightGray):
        """ 通过找到鼠标区域高亮指定行 :return: """
        extraSelections = []
        if not self.isReadOnly():
            # 创建选中块
            selection = self.ExtraSelection()
            # 设置块的高亮颜色,格式
            selection.format.setBackground(QColor(color))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            # 移动光标到textedit中的指定行
            position = self.document().findBlockByLineNumber(line).position()
            selection.cursor = self.textCursor()
            selection.cursor.setPosition(position)
            # 将高亮底块添加至textedit中
            extraSelections.append(selection)
            self.setExtraSelections(extraSelections)

    def numberWidth(self):
        block_count = self.document().blockCount()
        max_value = max(1, block_count)
        d_count = len(str(max_value))
        _width = self.fontMetrics().width('0') * d_count + 10
        return _width

    def updateWidth(self):
        self.setViewportMargins(self.numberWidth(), 0, 0, 0)


    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.numberWidth(), cr.height()))

    def numberAreaPaint(self, event):

        tc = self.textCursor()
        rowNum = tc.blockNumber()
        self.lightCurrentRow(rowNum)

        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        # 获取首个可见文本块
        first_block_number = self.cursorForPosition(QPoint(0, 1)).blockNumber()
        # 从首个文本块开始处理
        block_number = first_block_number
        block = self.document().findBlockByNumber(block_number)
        top = self.viewport().geometry().top()
        if block_number == 0:
            additional_margin = int(self.document().documentMargin() - 1 - self.verticalScrollBar().sliderPosition())
        else:
            prev_block = self.document().findBlockByNumber(block_number - 1)
            additional_margin = int(self.document().documentLayout().blockBoundingRect(
                prev_block).bottom()) - self.verticalScrollBar().sliderPosition()
        top += additional_margin
        bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
        last_block_number = self.cursorForPosition(QPoint(0, self.height() - 1)).blockNumber()
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()) and block_number <= last_block_number:
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignCenter, number)
                painter.fillRect(QRect(self.lineNumberArea.width()-3, top,
                                           self.lineNumberArea.width(), height), QColor("#00CD66"))

            block = block.next()
            top = bottom
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            block_number += 1


class lineNumPaint(QWidget):
    def __init__(self, q_edit):
        super().__init__(q_edit)
        self.edit_num = q_edit

    def sizeHint(self):
        return QSize(self.edit_num.numberWidth(), 0)

    def paintEvent(self, event):
        self.edit_num.numberAreaPaint(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    codeEditor = Editor()
    codeEditor.setGeometry(100, 100, 800, 600)
    codeEditor.show()
    sys.exit(app.exec_())

