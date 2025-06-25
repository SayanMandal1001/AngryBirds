#Script for defining the class of blocks
#Block ID: Wood-0, Stone-1, Ice-2
#Block Category: Wood-2, Stone-3, Ice-5

category = (2,3,5)
pathImg="Media/Sprites/Blocks/"
image0 = (pathImg+"Wood.png",pathImg+"Stone.png",pathImg+"Ice.png")
image1 = (pathImg+"Wood1.png",pathImg+"Stone1.png",pathImg+"Ice1.png")
image2 = (pathImg+"Wood2.png",pathImg+"Stone2.png",pathImg+"Ice2.png")
image3 = (pathImg+"Wood3.png",pathImg+"Stone3.png",pathImg+"Ice3.png")
image = (image3,image2,image1,image0)

class Block:
    def __init__(self,id_block,health=100):
        self.id = id_block
        self.category = category[self.id]
        self.health = health
        if(self.health!=0):
            self.image = image[(self.health-1)//25][self.id]
        self.position=[0,0]
        self.collide=False
        self.bounce=False
        self.corners=[False,False,False,False]  #[TopLeft,TopRight,BottomRight,BottomLeft]
    def getId(self):
        return self.id
    def getCategory(self):
        return self.category
    def getHealth(self):
        return self.health
    def getImage(self):
        return self.image
    def getPosition(self):
        return self.position
    def getCorner(self):
        return self.corners
    def hasCollided(self):
        return self.collide
    def collided(self,tf):
        self.collide = tf
    def hasBounced(self):
        return self.bounce
    def bounced(self,tf):
        self.bounce = tf
    def damageBlock(self,damage):
        self.health-=damage
    def updateHealth(self,h):
        if(self.health!=0):
            self.health = h
        else:
            del self
    def updateImage(self):
        if(self.health!=0):
            return (int(self.health-1))//25
        else:
            del self
    def updatePosition(self,pos):
        self.position[0]=pos[0]
        self.position[1]=pos[1]
    def updateCorner(self,corner,value):
        self.corners[corner]=value
    def resetCorner(self):
        self.corners=[False,False,False,False]