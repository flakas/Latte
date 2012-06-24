from latte.Projects.Project import Project # Import base Project class

class ProjectDoingNothing(Project): # Must inherit from Project base class

    def get_title(self):
        """ User friendly project title """
        return 'Doing nothing'

    def belongs(self, window, categories):
        """

        Checks if window belongs to this project

        Returns:
            True if window belongs to this project
            False otherwise

        """
        return 'Youtube' in window

class ProjectLatte(Project):

    def get_title(self):
        """ User friendly project title """
        return 'Latte'

    def belongs(self, window, categories):
        """

        Checks if window belongs to this project

        Returns:
            True if window belongs to this project
            False otherwise

        """
        return 'Latte' in window
