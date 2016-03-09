#!/usr/bin/python
#coding=utf-8

class Loader:
    def __init__(self):
        self.targets = set()

    def loadTarget(self, var):
        pass


class LoaderFromVarSpliteByNewline(Loader):
    def __init__(self):
        Loader.__init__(self)

    def loadTarget(self, var):
        try:
            line = var.split('\n')
            for target in line:
                if len(target) != 0:
                    self.targets.append(target.strip())

        except Exception as e:
            self.targets = None

        return self.targets


class LoaderFromVarSpliteByComma(Loader):
    def __init__(self):
        Loader.__init__(self)

    def loadTarget(self, var):
        try:
            line = var.split(',')
            for target in line:
                if len(target) != 0:
                    self.targets.append(target.strip())

        except Exception as e:
            self.targets = None

        return self.targets

class LoaderFromFileSpliteByNewline(Loader):
    def __init__(self):
        Loader.__init__(self)

    def loadTarget(self, var):
        file = var
        lines = open(file, 'r')
        try:
            for line in lines:
                if line.startswith('#') or len(line) == 0:#开头的line为注释
                    continue

                line = line.replace('\r','')
                line = line.replace('\n','')
                self.targets.add(line)

        except IOError as e1:
            raise e1

        except Exception as e:
            self.targets = None

        lines.close()
        return self.targets


class TargetLoader:
    def __init__(self):
        pass

    def loadTargets(self, var = None, file = None):
        loader = None
        target_list = None
        if var != None:
            loader = LoaderFromVarSpliteByNewline()
            target_list = var

        elif file != None:
            loader = LoaderFromFileSpliteByNewline()
            target_list = file
        else:
            pass

        return loader.loadTarget(target_list)

