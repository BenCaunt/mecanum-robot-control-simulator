class pathRenderer:
    '''
    class constructs taking in a path which is represented by a list of tuples containing x, y coordiantes
    '''
    def __init__(self,path):
        self.path = path
    def renderPath(self, canvas):
        for point in range(len(self.path) - 1):
            canvas.draw_line(self.path[point], self.path[point + 1], 12, 'Red')