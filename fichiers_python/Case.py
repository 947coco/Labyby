

class Case: 
    def __init__(self):  
        self.murN, self.murS, self.murE, self.murW, self.vue = True, True, True, True, False
    def assigner_coordonnees(self, x1, y1, x2, y2): 
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.milieu_x, self.milieu_y = x1+(x2-x1)/2, y1+(y2-y1)/2
