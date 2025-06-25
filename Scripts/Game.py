import pygame
import math
import numpy
import random
from .birds import Bird
import Scripts.utils as utils
from .blocks import Block

RC=1
def changeResolutionConstant(newRC):
    global RC
    RC=newRC

def game(playerNames,settingVals):

    print("Player 1:",playerNames[0])
    print("Player 2:",playerNames[1])
    blockRows=int(settingVals[0])
    blockColumns=int(settingVals[1])
    numberBirdQueue=int(settingVals[2])
    hasBlockGravity=settingVals[3]
    shouldPredictProjectile=settingVals[4]
    hasVelocityDamage=True

    ####### VARIABLE DECLARATION #######
    screenSize=(1250*RC,700*RC)  # Set screen size

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    slingSize=(100*RC,100*RC)   #Size of the sling
    slingDist=100*RC   #Distance of the sling from the side wall

    playerSize=(50*RC,50*RC)  #Size of the player

    iconSize=(45*RC,45*RC)   #Size of bird icon
    iconHolderSize=(50*RC,50*RC)   #size of icon holder
    iconHolderBorderWidth=2*RC   #Width of the icon holder border

    distQueue=(50*RC,56*RC)   #Distance of queue from side wall
    padding = 10*RC   #Padding between consecutive icons

    draggingDist = 60*RC   #Maximum dragging distance
    slingCenteringDist = (42*RC,15*RC)  #Vector used for calcutating center of the sling image
    maxPredictionDist=450*RC
    projectilePointsRadius=5*RC

    g = 220*RC     #Gravitational acceleration
    frictionRetardation = 250*RC
    maxSpeed=600*RC    #Maximum speed of the projectile

    pointDist = 25*RC    #Minimun distance between succesive projectile points to be displayed

    blockSize=(60*RC,60*RC)
    topLeftBlock1Pos=(800*RC,500*RC-(blockRows*blockSize[1]))
    topRightBlock2Pos=(450*RC-blockSize[0],500*RC-(blockRows*blockSize[1]))

    birdCollisionDetectionDist = 20*RC
    topCollisionEscapeVelocity=20*RC
    e = 0.5     #elasticity value

    playerDamageStrength=50
    playerDamageStrengthMultiplier=0.1
    pierceRetardationConst=0.5

    ChuckVelocityMultiplier=1.2*RC
    bombT=0
    BombTimer=2
    startBomb=False
    blueVerticalVelocityExcess=40*RC

    fontSize = int(25*RC)
    fontStyle = "Media/Fonts/Rubik_Mono_One/RubikMonoOne-Regular.ttf"
    Color1=(0, 144, 184)    #Player1 Color
    Color2=(184, 0, 0)    #Player2 Color
    Color=[Color1,Color2,"Black"] 
    PlayerNamePosition=[(50*RC,20*RC),(1200*RC,20*RC)]

    gameOverPanelSize=[600*RC,210*RC]
    gameOverPanelBorderWidth=3*RC
    gameOverPadding=10*RC
    winnerFontSize=int(30*RC)
    testColor=(255, 255, 255)
    buttonColorPlayAgain=(15, 219, 131)
    buttonColorMainMenu=(15, 219, 131)
    textPadding = 10*RC
    textBorderWidth=2*RC
    buttonGap=60*RC

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()

    buttonFont = pygame.font.Font("Media/Fonts/Boogaloo/Boogaloo-Regular.ttf", int(30*RC))

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Angry Bird")

    # Game Clock
    clock = pygame.time.Clock()
    
    sling1Pos=(slingDist,screenSize[1]-slingSize[1])  #Position of the first sling
    sling2Pos=(screenSize[0]-slingDist-slingSize[0],screenSize[1]-slingSize[1])   #Position of the second sling
    slingPos=sling1Pos   #Postion of active sling
    pathImgSling = "Media/Sprites/Sling/"
    sling = utils.scaleImg(utils.loadImg(pathImgSling+"Slingshot.png"), slingSize)
    slingStretchedImg = [utils.scaleImg(utils.loadImg(pathImgSling+"SlingshotStretched.png"), slingSize),utils.flipImg(utils.scaleImg(utils.loadImg(pathImgSling+"SlingshotStretched.png"), slingSize))]
    slingStretched = slingStretchedImg[0]

    #Bird queue
    queue1Birds=[]
    queue1Pos=[]  #Position of queue1 bird icons
    queue2Birds=[]
    queue2Pos=[]  #Position of queue2 bird icons
    birdImg=[[],[]]  #List of all bird images
    birdIconImg = [[],[]]   #List of icon images

    #Initializing the bird sprites
    for j in range(0,4):
        birdImg[0].append(utils.scaleImg(utils.loadImg(Bird.getImage(Bird(j))),playerSize))
    for j in range(0,4):
        birdImg[1].append(utils.flipImg(utils.scaleImg(utils.loadImg(Bird.getImage(Bird(j))),playerSize)))
    for j in range(0,4):
        birdIconImg[0].append(utils.scaleImg(utils.loadImg(Bird.getImage(Bird(j))),iconSize))
    for j in range(0,4):
        birdIconImg[1].append(utils.flipImg(utils.scaleImg(utils.loadImg(Bird.getImage(Bird(j))),iconSize)))

    #Function for creating random queue of birds of size n
    def createBirdQueue(length):
        for i in range(0,length):
            n = random.randint(0,3)
            queue1Birds.append(Bird(n))
        for i in range(0,length):
            n = random.randint(0,3)
            queue2Birds.append(Bird(n))

    #Function for creating the position of the respective birds in queue
    def createBirdQueuePosition(length):
        dist1 = list(distQueue)
        dist2 = list((screenSize[0]-distQueue[0]-iconHolderSize[0],distQueue[1]))
        for i in range(0,length):
            queue1Pos.append(tuple(dist1))
            dist1[0] += iconHolderSize[0] + padding
        for i in range(0,length):
            queue2Pos.append(tuple(dist2))
            dist2[0] -= iconHolderSize[0] + padding

    dragging = False  #Boolean for dragging

    project=False  #Boolean for projecting
    projectilePoints=[]    #Stores the points in the trajectory
    predictedProjectilePoints=[]
    canPredictProjectile=False

    #Projectile Generating
    def projecting(player_x,player_y,vx,vy,dt):
        vy = vy - g * dt
        player_x = player_x + vx * dt
        player_y = player_y - vy * dt
        projectilePoints.append((player_x + playerSize[0]/2 ,player_y + playerSize[1]/2 ,vx,vy,dt))
        return (player_x,player_y,vx,vy)
    
    #Blocks initialization
    block1=numpy.empty((blockRows,blockColumns),dtype=Block)
    block2=numpy.empty((blockRows,blockColumns),dtype=Block)
    blocks=[block1,block2]
    block0Img = []
    block1Img = []
    block2Img = []
    block3Img = []
    for i in range(0,3):
        block0Img.append(utils.scaleImg(utils.loadImg(Block.getImage(Block(i,100))),blockSize).convert_alpha())
        block1Img.append(utils.scaleImg(utils.loadImg(Block.getImage(Block(i,74))),blockSize))
        block2Img.append(utils.scaleImg(utils.loadImg(Block.getImage(Block(i,49))),blockSize))
        block3Img.append(utils.scaleImg(utils.loadImg(Block.getImage(Block(i,24))),blockSize))
    blockImg=[block3Img,block2Img,block1Img,block0Img]

    for i in range(0,blockRows):
        pos1=list(topLeftBlock1Pos)
        pos1[1]+=blockSize[1]*i
        pos2=list(topRightBlock2Pos)
        pos2[1]+=blockSize[1]*i
        for j in range(0,blockColumns):
            n = random.randint(0,2)
            block1[i][j] = Block(n)
            Block.updatePosition(block1[i][j],pos1)
            pos1[0]+=blockSize[0]

            block2[i][blockColumns-j-1] = Block(n)
            Block.updatePosition(block2[i][blockColumns-j-1],pos2)
            pos2[0]-=blockSize[0]

    #Platform initialization
    platformLeftImg = utils.scaleImg(utils.loadImg("Media/Sprites/Platform/PlatformLeft.png"),blockSize)
    platformMiddleImg = utils.scaleImg(utils.loadImg("Media/Sprites/Platform/PlatformMiddle.png"),blockSize)
    platformRightImg = utils.scaleImg(utils.loadImg("Media/Sprites/Platform/PlatformRight.png"),blockSize)
    platform1Pos=numpy.empty(blockColumns+2,dtype=list)
    platform2Pos=numpy.empty(blockColumns+2,dtype=list)
    platformPos=[platform1Pos,platform2Pos]
    platform1BlockPos=numpy.array(Block.getPosition(blocks[0][-1][0])) + numpy.array([-blockSize[0],blockSize[1]])
    platform2BlockPos=numpy.array(Block.getPosition(blocks[1][-1][0])) + numpy.array([-blockSize[0],blockSize[1]])
    for i in range(0,blockColumns+2):
        platform1Pos[i]=numpy.array(platform1BlockPos)
        platform2Pos[i]=numpy.array(platform2BlockPos)
        platform1BlockPos+=numpy.array([blockSize[0],0])
        platform2BlockPos+=numpy.array([blockSize[0],0])

    #Active Player
    activePlayer=1
    createBirdQueue(numberBirdQueue)
    createBirdQueuePosition(numberBirdQueue)
    player = [{'Bird':queue1Birds[len(queue1Birds) - 1], 'Position':list(slingPos), 'Velocity':[0,0]},{},{}]
    player[0]['Image']=birdImg[0][Bird.getId(player[0]["Bird"])]
    player_x=player[0]["Position"][0]
    player_y=player[0]["Position"][1]
    playerCenter=[[],[],[]]
    score=[0,0]
    playerSwitchTimer=1
    inactiveTime=0

    canActivatePowerUp=True
    hasactivatedPowerUp=False

    def distance(x1,y1,x2,y2):
        return math.sqrt(((x1-x2)**2)+((y1-y2)**2))

    #Functions for collision
    def reinitialiseBlockCollision():
        for i in range(0,blockRows):
            for j in range(0,blockColumns):
                block = blocks[activePlayer-1][i][j]
                Block.collided(block,False)
    def topCollision(b_x,b_y,p_x,p_y):
        return b_x<=p_x<=(b_x+blockSize[0]) and (b_y-birdCollisionDetectionDist)<=p_y<=b_y
    def leftCollision(b_x,b_y,p_x,p_y):
        return b_y<=p_y<=(b_y+blockSize[1]) and (b_x-birdCollisionDetectionDist)<=p_x<=b_x
    def rightCollision(b_x,b_y,p_x,p_y):
        return b_y<=p_y<=(b_y+blockSize[1]) and (b_x+blockSize[0])<=p_x<=(b_x+blockSize[0]+birdCollisionDetectionDist)
    def bottomCollision(b_x,b_y,p_x,p_y):
        return b_x<=p_x<=(b_x+blockSize[0]) and (b_y+blockSize[1])<=p_y<=(b_y+blockSize[1]+birdCollisionDetectionDist)
    def topLeftCollision(b_x,b_y,p_x,p_y):
        return (b_x-birdCollisionDetectionDist)<=p_x<=b_x and (b_y-birdCollisionDetectionDist)<=p_y<=b_y and distance(b_x,b_y,p_x,p_y)<=birdCollisionDetectionDist
    def topRightCollision(b_x,b_y,p_x,p_y):
        b1 = b_x + blockSize[0]
        return (b_x+blockSize[0])<=p_x<=(b_x+blockSize[0]+birdCollisionDetectionDist) and (b_y-birdCollisionDetectionDist)<=p_y<=b_y and distance(b1,b_y,p_x,p_y)<=birdCollisionDetectionDist
    def bottomLeftCollision(b_x,b_y,p_x,p_y):
        b2 = b_y + blockSize[1]
        return (b_x-birdCollisionDetectionDist)<=p_x<=b_x and (b_y+blockSize[1])<=p_y<=(b_y+blockSize[1]+birdCollisionDetectionDist) and distance(b_x,b2,p_x,p_y)<=birdCollisionDetectionDist
    def bottomRightCollision(b_x,b_y,p_x,p_y):
        b1 = b_x + blockSize[0]
        b2 = b_y + blockSize[1]
        return (b_x+blockSize[0])<=p_x<=(b_x+blockSize[0]+birdCollisionDetectionDist) and (b_y+blockSize[1])<=p_y<=(b_y+blockSize[1]+birdCollisionDetectionDist) and distance(b1,b2,p_x,p_y)<=birdCollisionDetectionDist
    def boxCollision(b_x,b_y,p_x,p_y):
        bool1 = topCollision(b_x,b_y,p_x,p_y) or leftCollision(b_x,b_y,p_x,p_y) or rightCollision(b_x,b_y,p_x,p_y) or bottomCollision(b_x,b_y,p_x,p_y)
        bool2 = topLeftCollision(b_x,b_y,p_x,p_y) or topRightCollision(b_x,b_y,p_x,p_y) or bottomLeftCollision(b_x,b_y,p_x,p_y) or bottomRightCollision(b_x,b_y,p_x,p_y)
        return bool1 or bool2
    def cornerCollision(b_x,b_y,p_x,p_y,Vx,Vy):
        return (topLeftCollision(b_x,b_y,p_x,p_y) and Vx>=0 and Vy<=0) or (topRightCollision(b_x,b_y,p_x,p_y) and Vx<=0 and Vy>=0) or (bottomLeftCollision(b_x,b_y,p_x,p_y) and Vx>=0 and Vy<=0) or (bottomRightCollision(b_x,b_y,p_x,p_y) and Vx<=0 and Vy<=0)

    def resetBounce(block,playerPos):
        block_Pos = Block.getPosition(block)
        b_x = block_Pos[0]
        b_y = block_Pos[1]
        p_x = playerPos[0]
        p_y = playerPos[1]
        return not boxCollision(b_x,b_y,p_x,p_y)
    
    #Function to bounce player
    def bouncePlayer(block_Pos,playerCenterPos,Vx,Vy,dt,Corner=(False,False,False,False)):
        b_x = block_Pos[0]
        b_y = block_Pos[1]
        p_x = playerCenterPos[0]
        p_y = playerCenterPos[1]
        if(leftCollision(b_x,b_y,p_x,p_y)):
            if(Vx>0):
                Vx = (-1)*abs(Vx)*e
        elif(rightCollision(b_x,b_y,p_x,p_y)):
            if(Vx<0):
                Vx = abs(Vx)*e 
        elif(topCollision(b_x,b_y,p_x,p_y)):
            if(Vy<0):
                Vy = abs(Vy)*e
            if(abs(Vy) < topCollisionEscapeVelocity):
                Vy=0
                if(Vx>0):
                    Vx-= frictionRetardation * dt
                if(Vx<0):
                    Vx+= frictionRetardation * dt
                if(abs(Vx)<frictionRetardation * dt):
                    Vx=0
                player[0]["Position"][1]=b_y-(playerSize[1])/2-birdCollisionDetectionDist
        elif(bottomCollision(b_x,b_y,p_x,p_y)):
            if(Vy>0):
                Vy = (-1)*abs(Vy)*e
        elif(topLeftCollision(b_x,b_y,p_x,p_y) and Corner[0]):
            if(Vx>0 and Vy<0):
                Vx = (-1)*abs(Vx)*e
                Vy = abs(Vy)*e
        elif(topRightCollision(b_x,b_y,p_x,p_y) and Corner[1]):
            if(Vx<0 and Vy>0):
                Vx = abs(Vx)*e
                Vy = abs(Vy)*e
        elif(bottomRightCollision(b_x,b_y,p_x,p_y) and Corner[2]):
            if(Vx<0 and Vy<0):
                Vx = abs(Vx)*e
                Vy = abs(Vy)*e
        elif(bottomLeftCollision(b_x,b_y,p_x,p_y) and Corner[3]):
            if(Vx>0 and Vy<0):
                Vx = (-1)*abs(Vx)*e
                Vy = abs(Vy)*e
        return Vx,Vy

    #Function for gravity to blocks
    def fallHangingBlock(blocks,rows,cols,playerSide):
        activeBlocks=blocks[playerSide]
        for i in range(1,rows):
            for j in range(0,cols):
                if(Block.getHealth(activeBlocks[i][j])<=0 and Block.getHealth(activeBlocks[i-1][j])>0):
                    hangingBlock=activeBlocks[i][j]
                    for k in range(0,i):    
                        blocks[playerSide][i-k][j] = blocks[playerSide][i-k-1][j]
                        PrevPos=Block.getPosition(blocks[playerSide][i-k-1][j])
                        Block.updatePosition(blocks[playerSide][i-k][j],(PrevPos[0],PrevPos[1]+blockSize[1]))
                    PrevPos=Block.getPosition(blocks[playerSide][0][j])
                    blocks[playerSide][0][j]=hangingBlock
                    Block.updatePosition(blocks[playerSide][0][j],(PrevPos[0],PrevPos[1]-blockSize[1]))

    #Function for collision detection
    def detectCollision(playerCenter,Vx,Vy,playerDamageStrength):
        firstHit=False
        for i in range(0,blockRows):
            for j in range(0,blockColumns):
                block = blocks[activePlayer-1][i][j]
                health = Block.getHealth(block)

                #Assigning corner values
                Block.resetCorner(block)
                if(i==0):
                    if((j==0 and health>0) or (j!=0 and Block.getHealth(blocks[activePlayer-1][i][j-1])<=0)):
                        Block.updateCorner(block,0,True)
                        if(Block.getHealth(blocks[activePlayer-1][i+1][j])<=0):
                            Block.updateCorner(block,3,True)
                    if((j==blockColumns-1 and health>0) or (j!=blockColumns-1 and Block.getHealth(blocks[activePlayer-1][i][j+1])<=0)):
                        Block.updateCorner(block,1,True)
                        if(Block.getHealth(blocks[activePlayer-1][i+1][j])<=0):
                            Block.updateCorner(block,2,True)
                elif(i==blockRows-1):
                    if((j==0 and health>0) or (j!=0 and Block.getHealth(blocks[activePlayer-1][i][j-1])<=0)):
                        if(Block.getHealth(blocks[activePlayer-1][i-1][j])<=0):
                            Block.updateCorner(block,0,True)
                    if((j==blockColumns-1 and health>0) or (j!=blockColumns-1 and Block.getHealth(blocks[activePlayer-1][i][j+1])<=0)):
                        if(Block.getHealth(blocks[activePlayer-1][i-1][j])<=0):
                            Block.updateCorner(block,1,True)
                else:
                    if((j==0 and health>0) or (j!=0 and Block.getHealth(blocks[activePlayer-1][i][j-1])<=0)):
                        if(Block.getHealth(blocks[activePlayer-1][i-1][j])<=0):
                            Block.updateCorner(block,0,True)
                        if(Block.getHealth(blocks[activePlayer-1][i+1][j])<=0):
                            Block.updateCorner(block,3,True)
                    if((j==blockColumns-1 and health>0) or (j!=blockColumns-1 and Block.getHealth(blocks[activePlayer-1][i][j+1])<=0)):
                        if(Block.getHealth(blocks[activePlayer-1][i-1][j])<=0):
                            Block.updateCorner(block,1,True)
                        if(Block.getHealth(blocks[activePlayer-1][i+1][j])<=0):
                            Block.updateCorner(block,2,True)

                if(Block.hasCollided(block)==False and Block.getHealth(block)>0):
                    pos = Block.getPosition(block)
                    x1 = pos[0]
                    y1 = pos[1]
                    px = playerCenter[0]
                    py = playerCenter[1]
                    if(boxCollision(x1,y1,px,py)):
                        damage=0
                        Block.collided(block,True)
                        if(hasVelocityDamage):
                            if((rightCollision(x1,y1,px,py) and Vx<=0) or (leftCollision(x1,y1,px,py) and Vx>=0)):
                                damage = abs(Vx) * playerDamageStrengthMultiplier
                            elif((topCollision(x1,y1,px,py) and Vy<=0) or (bottomCollision(x1,y1,px,py) and Vy>=0)):
                                damage = abs(Vy) * playerDamageStrengthMultiplier
                            elif(cornerCollision(x1,y1,px,py,Vx,Vy)):
                                damage = math.sqrt(Vx**2 + Vy**2)* playerDamageStrengthMultiplier
                        else:
                            damage = playerDamageStrength
                            if playerDamageStrength>=10:
                                playerDamageStrength-=10
                        if(Bird.getStrength(player[0]["Bird"])%Block.getCategory(block) == 0):
                            damage*=2
                        damage/=RC
                        score[activePlayer-1]+=int(((damage*health)//1000)+(3 if (Bird.getStrength(player[0]["Bird"])%Block.getCategory(block) == 0 and Bird.getId(player[0]["Bird"])!=0 and not firstHit) else 0))   #Score
                        firstHit=True
                        canActivatePowerUp=False
                        Block.damageBlock(block,damage)
                        if(Block.getHealth(block)<=0):
                            if(rightCollision(x1,y1,px,py) or leftCollision(x1,y1,px,py)):
                                Vx = Vx*pierceRetardationConst
                            elif(topCollision(x1,y1,px,py) or bottomCollision(x1,y1,px,py)):
                                Vy = Vy*pierceRetardationConst
                            elif(cornerCollision(x1,y1,px,py,Vx,Vy)):
                                Vx = Vx*pierceRetardationConst/math.sqrt(2)
                                Vy = Vy*pierceRetardationConst/math.sqrt(2)
                if(Block.getHealth(block)>0):  #To add bounceback
                    Vx,Vy = bouncePlayer(Block.getPosition(block),playerCenter,Vx,Vy,dt,Block.getCorner(block))
                if(resetBounce(block,playerCenter)):
                    Block.collided(block,False)
        return Vx,Vy
    
    backgroundImage = utils.scaleImg(utils.loadImg("Media/Sprites/BackGround/Background1.png"),screenSize)

    # Main Game Loop
    gameOver=False
    extraChance=False
    winner=0
    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta Time (seconds)
        slingCenter = (slingPos[0] + slingCenteringDist[0],slingPos[1] + slingCenteringDist[1])
        for i in range(0,len(player)):
            if(hasactivatedPowerUp==True and Bird.getId(player[0]["Bird"])==3) or i==0:
                playerCenter[i] = utils.imageCenter(player[i]["Position"],playerSize)
        playerPrevPos=player[0]["Position"]
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if(not gameOver):
                # Start Dragging
                if event.type == pygame.MOUSEBUTTONDOWN and project == False:
                    mouse_x, mouse_y = event.pos
                    radius = math.sqrt((mouse_x-slingCenter[0])**2 + (mouse_y-slingCenter[1])**2)
                    if(radius <= draggingDist+10):
                        if player_x <= mouse_x <= player_x + playerSize[0]  and player_y <= mouse_y <= player_y + playerSize[1]:
                            dragging = True        

                # Stop Dragging
                if event.type == pygame.MOUSEBUTTONUP:
                    if(project == False and dragging):
                        project = True  
                        mouse_x, mouse_y = event.pos
                        radius = math.sqrt(((mouse_x-slingCenter[0])**2) + ((mouse_y-slingCenter[1])**2))
                        angle = math.atan2(mouse_y-slingCenter[1],mouse_x-slingCenter[0])
                        if(radius>draggingDist):
                            radius=draggingDist
                        speed = (maxSpeed/draggingDist)*radius
                        player[0]["Velocity"][0]=-1 * speed * math.cos(angle)
                        player[0]["Velocity"][1]=speed * math.sin(angle)
                    dragging = False

                # While Dragging
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    radius = math.sqrt(((mouse_x-slingCenter[0])**2) + ((mouse_y-slingCenter[1])**2))
                    angle = math.atan2(mouse_y-slingCenter[1],mouse_x-slingCenter[0])
                    if dragging:
                        if radius <= draggingDist: 
                            mouse_x, mouse_y = event.pos
                            player_x = mouse_x - playerSize[0]/2 - numpy.sign(mouse_x - slingCenter[0])
                            player_y = mouse_y - playerSize[1]/2 - numpy.sign(mouse_y - slingCenter[1]) 
                        if radius > draggingDist:
                            angle = math.atan2(mouse_y-slingCenter[1],mouse_x-slingCenter[0]) 
                            player_x = slingCenter[0] + draggingDist * math.cos(angle) - playerSize[0]/2
                            player_y = slingCenter[1] + draggingDist * math.sin(angle) - playerSize[1]/2
                            radius=draggingDist
                        canPredictProjectile=True
                        predictedProjectilePoints=[]                  
                
                if event.type == pygame.MOUSEBUTTONDOWN and project==True:
                    hasactivatedPowerUp=True
            else:
                #For PlayAgain
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if(button_xPlayAgain<mouse_x<button_xPlayAgain+widthPlayAgain+2*textPadding and button_yPlayAgain<mouse_y<button_yPlayAgain+heightPlayAgain+textPadding):
                        return playerNames,score,winner,True
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if(button_xPlayAgain<mouse_x<button_xPlayAgain+widthPlayAgain+2*textPadding and button_yPlayAgain<mouse_y<button_yPlayAgain+heightPlayAgain+textPadding):
                        buttonColorPlayAgain=(207, 230, 64)
                    else:
                        buttonColorPlayAgain=(15, 219, 131)
                #For MainMenu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if(button_xMainMenu<mouse_x<button_xMainMenu+widthMainMenu+2*textPadding and button_yMainMenu<mouse_y<button_yMainMenu+heightMainMenu+textPadding):
                        return playerNames,score,winner,False
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if(button_xMainMenu<mouse_x<button_xMainMenu+widthMainMenu+2*textPadding and button_yMainMenu<mouse_y<button_yMainMenu+heightMainMenu+textPadding):
                        buttonColorMainMenu=(207, 230, 64)
                    else:
                        buttonColorMainMenu=(15, 219, 131)

        #PowerUp
        if(hasactivatedPowerUp and canActivatePowerUp):
            canActivatePowerUp=False
            hasactivatedPowerUp=False
            if(Bird.getId(player[0]["Bird"])==1):
                player[0]["Velocity"][0]*=ChuckVelocityMultiplier
                player[0]["Velocity"][1]*=ChuckVelocityMultiplier
            if(Bird.getId(player[0]["Bird"])==2):
                startBomb=True
                bombT=0
            if(Bird.getId(player[0]["Bird"])==3):
                player[1] = {'Bird':Bird(3), 'Position':player[0]['Position'], 'Velocity':[player[0]["Velocity"][0],player[0]["Velocity"][1]+blueVerticalVelocityExcess], 'Image':birdImg[0][3]}
                player[2] = {'Bird':Bird(3), 'Position':player[0]['Position'], 'Velocity':[player[0]["Velocity"][0],player[0]["Velocity"][1]-blueVerticalVelocityExcess], 'Image':birdImg[0][3]}
            
        if(startBomb):
            if(bombT<=BombTimer):
                bombT+=dt
            if(bombT>BombTimer):
                bombT=0
                startBomb=False
                birdCollisionDetectionDist=100*RC

        #print(birdCollisionDetectionDist)
            
        #For predicted projectile
        if(dragging and canPredictProjectile and shouldPredictProjectile):
            if(radius>draggingDist):
                radius=draggingDist
            speed = (maxSpeed/draggingDist)*radius
            predictionVx=-1 * speed * math.cos(angle)
            predictionVy=speed * math.sin(angle)
            timeGap=0.15
            totalTime=2
            x,y,t=player_x+playerSize[0]/2,player_y+playerSize[1]/2,0
            for i in numpy.linspace(0,totalTime,int(totalTime*60)):
                x += predictionVx * dt
                predictionVy -= g * dt
                y -= predictionVy * dt
                speed = math.sqrt((predictionVx**2 + predictionVy**2))
                if(t>timeGap):
                    predictedProjectilePoints.append([x,y])
                    t=0
                t+=dt
            canPredictProjectile=False

        #Alternating activePlayer between two players
        if((player_y > screenSize[1] or inactiveTime>=playerSwitchTimer)and not dragging and project): 
            activePlayer = 3 - activePlayer
            inactiveTime=0
            if(activePlayer ==  2):
                slingPos=sling2Pos
                queue1Birds.pop()
                if(queue1Birds==[] and queue2Birds==[]):
                    createBirdQueue(numberBirdQueue)
                player[0]["Bird"] = queue2Birds[len(queue2Birds)-1]
                player[0]['Image']=birdImg[1][Bird.getId(player[0]["Bird"])]
                player[0]["Position"]=list(slingPos)
                player_x=player[0]["Position"][0]+playerSize[0]
                player_y=player[0]["Position"][1]
                slingStretched=slingStretchedImg[1]
            else:
                if(extraChance):    #For extra chance
                    gameOver=True
                elif(not gameOver):
                    slingPos=sling1Pos
                    queue2Birds.pop()
                    if(queue1Birds==[] and queue2Birds==[]):
                        createBirdQueue(numberBirdQueue)
                    player[0]["Bird"] = queue1Birds[len(queue1Birds)-1]
                    player[0]['Image']=birdImg[0][Bird.getId(player[0]["Bird"])]
                    player[0]["Position"]=list(slingPos)
                    player_x=player[0]["Position"][0]
                    player_y=player[0]["Position"][1]
                    slingStretched=slingStretchedImg[1]
            sling = pygame.transform.flip(sling,True,False)
            projectilePoints=[]
            project = False
            canActivatePowerUp=True
            birdCollisionDetectionDist=20*RC
            if(hasBlockGravity):
                fallHangingBlock(blocks,blockRows,blockColumns,activePlayer%2)

        #Projecting bird
        if(project == True):
            result=projecting(player_x,player_y,player[0]["Velocity"][0],player[0]["Velocity"][1],dt)
            player_x=result[0]
            player_y=result[1]
            player[0]["Velocity"][0]=result[2]
            player[0]["Velocity"][1]=result[3]
            prevPoint=[projectilePoints[0][0],projectilePoints[0][1]]
        if(project==False):
            reinitialiseBlockCollision()
            playerDamageStrength=50
        player[0]["Position"]=[player_x,player_y]

        #Collision Detection with blocks
        player[0]["Velocity"][0],player[0]["Velocity"][1]=detectCollision(playerCenter[0],player[0]["Velocity"][0],player[0]["Velocity"][1],playerDamageStrength)

        #Collision Detection with platform
        for i in range(0,blockColumns+2):
            pos=platformPos[activePlayer-1][i]
            leftCorner=True if(i==0) else False
            rightCorner=True if(i==blockColumns+1) else False
            player[0]["Velocity"][0],player[0]["Velocity"][1] = bouncePlayer(pos,playerCenter[0],player[0]["Velocity"][0],player[0]["Velocity"][1],dt,(leftCorner,rightCorner,rightCorner,leftCorner))

        #Detecting halt of bird
        if((player[0]["Position"]==playerPrevPos and project and not dragging) or (player[0]["Position"][0]>screenSize[0] or player[0]["Position"][0]<0)):
            inactiveTime+=dt
        else:
            inactiveTime=0
        
        ####Drawing sprites####
        screen.blit(backgroundImage, (0,0))

        #Platform
        for i in range(0,blockColumns+2):
            if(i==0):
                platBlockImg = platformLeftImg
            elif(i==blockColumns+1):
                platBlockImg = platformRightImg
            else:
                platBlockImg = platformMiddleImg
            activeImgPos = platformPos[activePlayer-1][i]
            inactiveImagePos = platformPos[2-activePlayer][i]
            screen.blit(platBlockImg,activeImgPos)
            temp = pygame.Surface(platBlockImg.get_size(), pygame.SRCALPHA)
            temp.blit(platBlockImg, (0, 0))
            temp.set_alpha(100)
            screen.blit(temp,inactiveImagePos)

        #Blocks
        for i in range(0,blockRows):
            for j in range(blockColumns):
                block=blocks[activePlayer-1][i][j]
                if(Block.getHealth(block)>0):
                    screen.blit(blockImg[Block.updateImage(block)][Block.getId(block)],Block.getPosition(block))
                inactiveBlock=blocks[2-activePlayer][i][j]
                if(Block.getHealth(inactiveBlock)>0):
                    inactiveimg=blockImg[Block.updateImage(inactiveBlock)][Block.getId(inactiveBlock)]
                    temp = pygame.Surface(inactiveimg.get_size(), pygame.SRCALPHA)
                    temp.blit(inactiveimg, (0, 0))
                    temp.set_alpha(100)
                    screen.blit(temp,Block.getPosition(inactiveBlock))
        
        #Projectile Points
        for value in projectilePoints:
            dist = math.sqrt((prevPoint[0]-value[0])**2 + (prevPoint[1]-value[1])**2)
            if(dist>pointDist):
                pygame.draw.circle(screen, Bird.getColor(player[0]["Bird"]), (value[0],value[1]), projectilePointsRadius)
                prevPoint=[value[0],value[1]]

        #Predicted Projectile Points
        if(dragging):
            pygame.draw.line(screen, WHITE, playerCenter[0], slingCenter, int(projectilePointsRadius))
            radius=7*RC
            for value in predictedProjectilePoints:
                dist = math.sqrt((slingCenter[0]-value[0])**2 + (slingCenter[1]-value[1])**2)
                if(dist<maxPredictionDist):
                    pygame.draw.circle(screen, WHITE, (value[0],value[1]),radius)
                    radius/=1.08
                else:
                    break
        #Checking for bird image flip
        if(bombT<=BombTimer and startBomb):
                pygame.draw.circle(screen, "Red", player[0]["Position"], birdCollisionDetectionDist)

        if(project==True):
            if((activePlayer-1.5)*player[0]["Velocity"][0]<0):
                player[0]["Image"] = birdImg[0][Bird.getId(player[0]["Bird"])] if(activePlayer==1) else birdImg[1][Bird.getId(player[0]["Bird"])]
            if((activePlayer-1.5)*player[0]["Velocity"][0]>0):
                player[0]["Image"] = birdImg[1][Bird.getId(player[0]["Bird"])] if(activePlayer==1) else birdImg[0][Bird.getId(player[0]["Bird"])]
        if(dragging):
            if(activePlayer==1):
                if(player[0]["Position"][0]+playerSize[0]/2<=slingCenter[0]):
                    player[0]["Image"] = birdImg[0][Bird.getId(player[0]["Bird"])]
                    slingStretched = slingStretchedImg[0]
                else:
                    player[0]["Image"] = birdImg[1][Bird.getId(player[0]["Bird"])]
                    slingStretched = slingStretchedImg[1]
            if(activePlayer==2):
                if(player[0]["Position"][0]+playerSize[0]/2>=slingCenter[0]):
                    player[0]["Image"] = birdImg[1][Bird.getId(player[0]["Bird"])]
                    slingStretched = slingStretchedImg[1]
                else:
                    player[0]["Image"] = birdImg[0][Bird.getId(player[0]["Bird"])]
                    slingStretched = slingStretchedImg[0]

        if(player_x + playerSize[0]/2 > slingCenter[0]):
            screen.blit(sling, slingPos) if(not dragging) else screen.blit(slingStretched, slingPos)
        screen.blit(player[0]["Image"],player[0]["Position"]) 
        if(player_x + playerSize[0]/2 <= slingCenter[0]):
            screen.blit(sling, slingPos) if(not dragging) else screen.blit(slingStretched, slingPos)

        #Queue of birds
        for i in range(0,len(queue1Birds)):
            borderColor=BLACK
            if(i==len(queue1Birds)-1 and activePlayer==1):
                borderColor=(13, 207, 0)
            pygame.draw.rect(screen, borderColor, (queue1Pos[i][0],queue1Pos[i][1],iconHolderSize[0],iconHolderSize[1]))
            pygame.draw.rect(screen, (135, 195, 212), (queue1Pos[i][0]+iconHolderBorderWidth,queue1Pos[i][1]+iconHolderBorderWidth,iconHolderSize[0]-iconHolderBorderWidth*2,iconHolderSize[1]-iconHolderBorderWidth*2))
            img = birdIconImg[0][Bird.getId((queue1Birds[i]))]
            screen.blit(img,(queue1Pos[i][0]+(iconHolderSize[0]-iconSize[0])/2,queue1Pos[i][1]+(iconHolderSize[1]-iconSize[1])/2))

        for i in range(0,len(queue2Birds)):
            borderColor=BLACK
            if(i==len(queue2Birds)-1 and activePlayer==2):
                borderColor=(13, 207, 0)
            pygame.draw.rect(screen, borderColor, (queue2Pos[i][0],queue2Pos[i][1],iconHolderSize[0],iconHolderSize[1]))
            pygame.draw.rect(screen, (232, 160, 160), (queue2Pos[i][0]+iconHolderBorderWidth,queue2Pos[i][1]+iconHolderBorderWidth,iconHolderSize[0]-iconHolderBorderWidth*2,iconHolderSize[1]-iconHolderBorderWidth*2))
            img = birdIconImg[0][Bird.getId((queue2Birds[i]))]
            screen.blit(img,(queue2Pos[i][0]+(iconHolderSize[0]-iconSize[0])/2,queue2Pos[i][1]+(iconHolderSize[1]-iconSize[1])/2))

        #Player Names and Scores
        player1TextSurface= utils.getTextSurface(playerNames[0] + " - ",Color[0],fontSize,fontStyle)
        screen.blit(player1TextSurface, (PlayerNamePosition[0][0],PlayerNamePosition[0][1]))
        player2TextSurface = utils.getTextSurface(" - " + playerNames[1],Color[1],fontSize,fontStyle)
        screen.blit(player2TextSurface, (PlayerNamePosition[1][0] - player2TextSurface.get_width(),PlayerNamePosition[1][1]))
        pygame.draw.line(screen,Color[0],(distQueue[0],distQueue[1] - 6*RC),(distQueue[0]+numberBirdQueue*iconHolderSize[0]+(numberBirdQueue-1)*padding,distQueue[1] - 6*RC),width=3)
        pygame.draw.line(screen,Color[1],(screenSize[0]-distQueue[0],distQueue[1] - 6*RC),(screenSize[0]-(distQueue[0]+numberBirdQueue*iconHolderSize[0]+(numberBirdQueue-1)*padding),distQueue[1] - 6*RC),width=3)

        score1TextSurface=utils.getTextSurface(str(score[0]),Color[0],fontSize,fontStyle)
        screen.blit(score1TextSurface, (PlayerNamePosition[0][0] + player1TextSurface.get_width(),PlayerNamePosition[0][1]))
        score2TextSurface = utils.getTextSurface(str(score[1]),Color[1],fontSize,fontStyle)
        screen.blit(score2TextSurface, (PlayerNamePosition[1][0] - player2TextSurface.get_width() - score2TextSurface.get_width(),PlayerNamePosition[1][1]))        

        #Checking for destruction of all the blocks
        aliveBlockCount=[0,0]
        for a in range(0,2):
            for i in range(0,blockRows):
                for j in range(blockColumns):
                    block=blocks[a][i][j]
                    health=Block.getHealth(block)
                    if(health>0):
                        aliveBlockCount[a]+=1
        if(aliveBlockCount[0]==0):
            if(not extraChance):
                extraChance=True
                score[0]+=20
        if(aliveBlockCount[1]==0):
            if(not gameOver):
                gameOver=True   
                score[1]+=20
        if(gameOver):
            if(score[0]>score[1]):
                print("Congratulations!! ",playerNames[0],"won!")
                winner=1
            elif(score[0]<score[1]):
                print("Congratulations!! ",playerNames[1],"won!")
                winner=2
            else:
                print("Draw!")
                winner=0

            #Game Over Panel
            if(winner!=0):
                resultTextSurface = utils.getTextSurface(playerNames[winner-1] + " won!!",Color[winner-1],winnerFontSize,fontStyle)
            else:
                resultTextSurface = utils.getTextSurface("Draw!",Color[winner-1],winnerFontSize,fontStyle)
            
            finalScore1TextSurface = utils.getTextSurface(playerNames[0] + " - " + str(score[0]),"Black",fontSize,fontStyle)
            finalScore2TextSurface = utils.getTextSurface(playerNames[1] + " - " + str(score[1]),"Black",fontSize,fontStyle)
            gameOverPanelPos=((screenSize[0]-gameOverPanelSize[0])/2,(screenSize[1]-gameOverPanelSize[1])/2)

            if((resultTextSurface.get_width()+(2*gameOverPadding))>gameOverPanelSize[0]):
                gameOverPanelSize[0]=resultTextSurface.get_width()+(2*gameOverPadding)
            if((finalScore1TextSurface.get_width()+(2*gameOverPadding))>gameOverPanelSize[0]):
                gameOverPanelSize[0]=finalScore1TextSurface.get_width()+(2*gameOverPadding)
            if((finalScore2TextSurface.get_width()+(2*gameOverPadding))>gameOverPanelSize[0]):
                gameOverPanelSize[0]=finalScore2TextSurface.get_width()+(2*gameOverPadding)
            if((resultTextSurface.get_height()+finalScore1TextSurface.get_height()+finalScore2TextSurface.get_height()+45*RC+(2*gameOverPadding))>gameOverPanelSize[1]):
                gameOverPanelSize[1]=resultTextSurface.get_height()+finalScore1TextSurface.get_height()+finalScore2TextSurface.get_height()+45*RC+(2*gameOverPadding)
            
            pygame.draw.rect(screen, "Black", (gameOverPanelPos[0]-gameOverPanelBorderWidth,gameOverPanelPos[1]-gameOverPanelBorderWidth,gameOverPanelSize[0]+2*gameOverPanelBorderWidth,gameOverPanelSize[1]+2*gameOverPanelBorderWidth),border_radius=int(10*RC))
            pygame.draw.rect(screen, "White", (gameOverPanelPos[0],gameOverPanelPos[1],gameOverPanelSize[0],gameOverPanelSize[1]),border_radius=int(10*RC))
                
            screen.blit(resultTextSurface, ((screenSize[0]-resultTextSurface.get_width())/2,gameOverPanelPos[1]+15*RC))
            screen.blit(finalScore1TextSurface, ((screenSize[0]-resultTextSurface.get_width())/2,gameOverPanelPos[1]+resultTextSurface.get_height()+35*RC))
            screen.blit(finalScore2TextSurface, ((screenSize[0]-resultTextSurface.get_width())/2,gameOverPanelPos[1]+resultTextSurface.get_height()+finalScore1TextSurface.get_height()+45*RC))

            txt_surfacePlayAgain = buttonFont.render("Play Again", True, testColor)
            widthPlayAgain=txt_surfacePlayAgain.get_width()
            heightPlayAgain=txt_surfacePlayAgain.get_height()
            button_xPlayAgain=screenSize[0]/2-widthPlayAgain/2-textPadding -((buttonGap+widthPlayAgain)/2)
            button_yPlayAgain=gameOverPanelPos[1]+gameOverPanelSize[1]-heightPlayAgain-gameOverPadding

            pygame.draw.rect(screen, BLACK, (button_xPlayAgain-textBorderWidth,button_yPlayAgain-textBorderWidth,widthPlayAgain+2*textPadding+2*textBorderWidth,heightPlayAgain+2*textBorderWidth), border_radius=int(10*RC))
            pygame.draw.rect(screen, buttonColorPlayAgain, (button_xPlayAgain,button_yPlayAgain,widthPlayAgain+2*textPadding,heightPlayAgain), border_radius=int(10*RC))
            screen.blit(txt_surfacePlayAgain, (button_xPlayAgain+textPadding,button_yPlayAgain))

            txt_surfaceMainMenu = buttonFont.render("Main Menu", True, testColor)
            widthMainMenu=txt_surfaceMainMenu.get_width()
            heightMainMenu=txt_surfaceMainMenu.get_height()
            button_xMainMenu=screenSize[0]/2-widthMainMenu/2-textPadding +((buttonGap+widthPlayAgain)/2)
            button_yMainMenu=gameOverPanelPos[1]+gameOverPanelSize[1]-heightMainMenu-gameOverPadding

            pygame.draw.rect(screen, BLACK, (button_xMainMenu-textBorderWidth,button_yMainMenu-textBorderWidth,widthMainMenu+2*textPadding+2*textBorderWidth,heightMainMenu+2*textBorderWidth), border_radius=int(10*RC))
            pygame.draw.rect(screen, buttonColorMainMenu, (button_xMainMenu,button_yMainMenu,widthMainMenu+2*textPadding,heightMainMenu), border_radius=int(10*RC))
            screen.blit(txt_surfaceMainMenu, (button_xMainMenu+textPadding,button_yMainMenu))

        pygame.display.flip()  # Update the screen


    pygame.quit()