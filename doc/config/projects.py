from latte.Projects.Project import Project # Import base Project class

class ProjectDoingNothing(Project): # Must inherit from Project base class

    def getTitle(self):
        """ User friendly project title """
        return 'Doing nothing'

    def belongs(self, window, category):
        """

        Checks if window belongs to this project

        Returns:
            True if window belongs to this project
            False otherwise

        """
        return 'Youtube' in window and 'Chrome' in category.getTitle()

class ProjectLatte(Project):

    def getTitle(self):
        return 'Latte'

    def belongs(self, window, category):
        return 'Latte' in window
