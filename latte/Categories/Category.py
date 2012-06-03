"""

Base abstract class for Category

"""

class Category(object):
    """

    Base abstract Category class

    """

    def get_title(self):
        """

        Returns category title

        """
        raise NotImplementedError

    def belongs(self, window):
        """

        Checks if window belongs to this category.
        Returns True if it belongs, false otherwise

        """
        raise NotImplementedError
