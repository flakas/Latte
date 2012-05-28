class Category(object):

    def getTitle(self):
        raise NotImplementedError

    def belongs(self, window):
        raise NotImplementedError
