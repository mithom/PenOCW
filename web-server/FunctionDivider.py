"""
deze module neemt de functie die momenteel uitgevoerd wordt, en splitst deze
op in kleinere functies om zo te kunnen zorgen dat ze ter plekke afgebroken
kunnen worden
"""

class functionDivider:
    """
    transforms commands into functions that the Car can execute. Also allows interuption of these commands.
    """
    commandLib={"goForward": [], "goBackward":[]} #the list contains the functions that should be executed in order to drive the car

    def __init__(self, firstCommand = None):
        self.currentCommand = None
        if firstCommand is not None:
            self.executeCommand(firstCommand)

    def executeCommand(self,command):
        pass

    def interuptCurrentCommand(self):
        """
        stops executing current command
        :return: the command with extra params to see how far it is already executed
        """
        pass
