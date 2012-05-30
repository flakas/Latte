class Project(object):

    def getTitle(self):
        raise NotImplementedError

    def belongs(self, window, category):
        raise NotImplementedError
