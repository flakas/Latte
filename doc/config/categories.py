from Categories.Category import Category # Import base Category class

class CategoryBrowsing(Category): # Must inherit from Category class
    
    def getTitle(self): # Must be defined.
        """ User friendly category title """
        return 'Browsing'

    def belongs(self, window):
        """ 
        
        Categorization method. 
        
        Returns:
            True if window belongs to this category
            False otherwise
        
        """
        return 'Google Chrome' in window

class CategoryTextEditing(Category):

    def getTitle(self):
        return 'Text editing'

    def belongs(self, window):
        return 'VIM' in window or 'Emacs' in window
