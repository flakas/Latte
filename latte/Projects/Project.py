"""

Assigns a project according to window title and category

"""
class Project(object):
    """

    Project assignment class based on window title and category

    """

    def get_title(self):
        """

        Returns project title string

        """
        raise NotImplementedError

    def belongs(self, window, category):
        """

        Checks if window belongs to this particular project.
        Returns True if it belongs, False otherwise

        """
        raise NotImplementedError
