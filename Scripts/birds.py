#Script for defining the class of birds
#Bird IDs: Red-0, Chuck-1, Bomb-2, Blue-3
#Block ID: Wood-2, Stone-3, Ice-5

strength = (30,2,3,5)
color = ((222, 63, 42),"yellow","black",(61, 171, 235))
pathImg = "Media/Sprites/Birds/"
image = (pathImg+"Red.png",pathImg+"Chuck.png",pathImg+"Bomb.png",pathImg+"Blue.png")

class Bird:
    def __init__(self,id_bird):
        self.id=id_bird
        self.strength = strength[self.id]
        self.image = image[self.id]
        self.color = color[self.id]
    def getId(self):
        return self.id
    def getStrength(self):
        return self.strength
    def getImage(self):
        return self.image
    def getColor(self):
        return self.color