import os


class Platform:
    def __init__(self, filename):
        self.plugins = []
        self.loadPlugins()
        self.zipfilename = filename

    def loadPlugins(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        pluginspath = os.path.join(base_path, '')

        for filename in os.path.join("", ''):
            if filename in os.listdir(pluginspath):
                filename = os.path.join(pluginspath, filename)
                filename = os.path.splitext(filename)[0]
                self.runPlugin(filename)

    def runPlugin(self, filename):
        pluginName = (os.path.split(filename)[0]).split('\\')[-1]

        if not pluginName.endswith("init__"):
            plugin = __import__("." + pluginName, fromlist=[pluginName])
            clazz = plugin.getPluginClass()
            obj = clazz()
            self.plugins.append(obj)

    def parseTest(self):
        i = 0
        for obj in self.plugins:
            obj.parse()
            obj.render()


if __name__ == '__main__':
    platform = Platform("plugin.py")
    platform.parseTest()

