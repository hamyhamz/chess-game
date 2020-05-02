"""Server side exceptions
Authors:
   Peter Hamran        xhamra00@stud.fit.vutbr.cz
Date:
   2.05.2020
"""


class UndefinedGameException(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

        def __str__(self):
            if self.message:
                return 'UndefinedGameException, {0}.'.format(self.message)
            else:
                return 'UndefinedGameException has been raised.'