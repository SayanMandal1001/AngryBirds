import pygame

#Scaling image
def scaleImg(img,size):
    return pygame.transform.scale(img,size)

#Flp Image
def flipImg(img):
    return pygame.transform.flip(img,True,False)

def loadImg(imgSrc):
    return pygame.image.load(imgSrc).convert_alpha()

def getTextSurface(text,color,fontSize,fontStyle):
    font = pygame.font.Font(fontStyle, fontSize)
    return font.render(text, True, color)

def imageCenter(position,size):
    return [position[0]+(size[0]/2),position[1]+(size[1]/2)]