# coding:utf-8
import sys

from PyQt5.QtCore import QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QPainter, QPixmap, QWheelEvent
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                           QGraphicsScene, QGraphicsView)


class Imager(QGraphicsView):
  """ 图片查看器 """
  def __init__(self, parent=None):
      super().__init__(parent=parent)
      self.zoom_in_times = 0
      self.max_zoom_in_times = 22
      # 创建场景
      self.graphics_scene = QGraphicsScene()
      # 图片
      self.pixmap = QPixmap('')
      self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
      self.displayed_im_size = QSize(0, 0)
      # 初始化小部件
      self.widgetInit()

  def widgetInit(self):
      """ 初始化小部件 """
      self.resize(1200, 900)

      # 隐藏滚动条
      self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
      self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

      # 以鼠标所在位置为锚点进行缩放
      self.setTransformationAnchor(self.AnchorUnderMouse)

      # 平滑缩放
      self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)
      self.setRenderHints(QPainter.Antialiasing |
                          QPainter.SmoothPixmapTransform)

      # 设置场景
      self.graphics_scene.addItem(self.pixmap_item)
      self.setScene(self.graphics_scene)

  def wheelEvent(self, e: QWheelEvent):
      """ 滚动鼠标滚轮缩放图片 """
      if e.angleDelta().y() > 0:
          self.zoomIn()
      else:
          self.zoomOut()

  def resizeEvent(self, e):
      """ 缩放图片 """
      super().resizeEvent(e)

      if self.zoom_in_times > 0:
          return

      # 调整图片大小
      ratio = self.getScaleRatio()
      self.displayed_im_size = self.pixmap.size()*ratio
      if ratio < 1:
          self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
      else:
          self.resetTransform()

  def setImage(self, imagePath: str):
      """ 设置显示的图片 """
      self.resetTransform()
      # 刷新图片
      self.pixmap = QPixmap(imagePath)
      self.pixmap_item.setPixmap(self.pixmap)
      # 调整图片大小
      self.setSceneRect(QRectF(self.pixmap.rect()))
      ratio = self.getScaleRatio()
      self.displayed_im_size = self.pixmap.size()*ratio
      if ratio < 1:
          self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

  def resetTransform(self):
      """ 重置变换 """
      super().resetTransform()
      self.zoom_in_times = 0
      self.setDragEnabled(False)

  def isEnableDrag(self):
      """ 根据图片的尺寸决定是否启动拖拽功能 """
      v = self.verticalScrollBar().maximum() > 0
      h = self.horizontalScrollBar().maximum() > 0
      return v or h

  def setDragEnabled(self, isEnabled: bool):
      """ 设置拖拽是否启动 """
      self.setDragMode(
          self.ScrollHandDrag if isEnabled else self.NoDrag)

  def getScaleRatio(self):
      """ 获取显示的图像和原始图像的缩放比例 """
      if self.pixmap.isNull():
          return 1

      pw = self.pixmap.width()
      ph = self.pixmap.height()
      rw = min(1, self.width()/pw)
      rh = min(1, self.height()/ph)
      return min(rw, rh)

  def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
      """ 缩放场景使其适应窗口大小 """
      super().fitInView(item, mode)
      self.displayed_im_size = self.getScaleRatio() * self.pixmap.size()
      self.zoom_in_times = 0

  def zoomIn(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
      """ 放大图像 """
      if self.zoom_in_times == self.max_zoom_in_times:
          return

      self.setTransformationAnchor(viewAnchor)

      self.zoom_in_times += 1
      self.scale(1.05, 1.05)
      self.setDragEnabled(self.isEnableDrag())

      # 还原 anchor
      self.setTransformationAnchor(self.AnchorUnderMouse)

  def zoomOut(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
      """ 缩小图像 """
      if self.zoom_in_times == 0 and not self.isEnableDrag():
          return

      self.setTransformationAnchor(viewAnchor)

      self.zoom_in_times -= 1

      # 原始图像的大小
      pw = self.pixmap.width()
      ph = self.pixmap.height()

      # 实际显示的图像宽度
      w = self.displayed_im_size.width()*1.1**self.zoom_in_times
      h = self.displayed_im_size.height()*1.1**self.zoom_in_times

      if pw > self.width() or ph > self.height():
          # 在窗口尺寸小于原始图像时禁止继续缩小图像比窗口还小
          if w <= self.width() and h <= self.height():
              self.fitInView(self.pixmap_item)
          else:
              self.scale(1/1.05, 1/1.05)
      else:
          # 在窗口尺寸大于图像时不允许缩小的比原始图像小
          if w <= pw:
              self.resetTransform()
          else:
              self.scale(1/1.05, 1/1.05)

      self.setDragEnabled(self.isEnableDrag())

      # 还原 anchor
      self.setTransformationAnchor(self.AnchorUnderMouse)

