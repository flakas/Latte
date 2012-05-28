class Category(object):

    @property
    def title(self):
        raise NotImplementedError

    def belongs(self, window):
        raise NotImplementedError
