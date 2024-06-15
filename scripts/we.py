from abc import ABCMeta, abstractmethod
utils = importlib.import_module('model.utils.utils')              # 绝对导入

class Base():
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get(self):
        print("Base.get()")
        pass


class Derive1(Base):
    pass



if __name__ == '__main__':
    b = Derive1()
    b.get()