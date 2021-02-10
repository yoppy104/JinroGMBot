
class ErrorLog:
    def __init__(self):
        pass

    def syntaxError(self, message):
        return "[Syntax Error] {}".format(message)

    
    def permissionError(self, message):
        return "[Permission Error] {}".format(message)


    def nullError(self, message):
        return "[NullReference Error] {}".format(message)
    