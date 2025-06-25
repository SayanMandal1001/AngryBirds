import pygame
import Scripts.utils as utils

RC=1
quit=False
mainMenu=False
def changeResolutionConstant(newRC):
    global RC
    RC=newRC

def titleScreen():
    screenSize=(1250*RC, 700*RC)
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Title Screen")
    clock = pygame.time.Clock()

    # Fonts and colors
    font = pygame.font.Font("Media/Fonts/Boogaloo/Boogaloo-Regular.ttf", int(40*RC))
    testColor=(255, 255, 255)
    buttonColor=[(15, 219, 131)]*3
    buttonGap=120*RC
    BLACK=(0,0,0)
    #Color="White"
    textCenterPosition=(625*RC,550*RC)
    textPadding = 10*RC
    textBorderWidth=2*RC

    titleScreenImg=utils.scaleImg(utils.loadImg("Media/Sprites/Title/TitleScreen1.png"),screenSize)

    running = True
    while running:
        clock.tick(30) / 1000

        txt_surfaceStart = font.render("PLAY", True, testColor)
        widthStart=txt_surfaceStart.get_width()
        heightStart=txt_surfaceStart.get_height()
        button_xStart=textCenterPosition[0]-widthStart/2-textPadding
        button_yStart=textCenterPosition[1]-heightStart/2

        txt_surfaceHistory = font.render("HISTORY", True, testColor)
        widthHistory=txt_surfaceHistory.get_width()
        heightHistory=txt_surfaceHistory.get_height()
        button_xHistory=textCenterPosition[0]-widthHistory/2-textPadding - (widthHistory+widthStart+buttonGap)/2
        button_yHistory=textCenterPosition[1]-heightHistory/2

        txt_surfaceQuit = font.render("QUIT", True, testColor)
        widthQuit=txt_surfaceQuit.get_width()
        heightQuit=txt_surfaceQuit.get_height()
        button_xQuit=textCenterPosition[0]-widthQuit/2-textPadding + (widthQuit+widthStart+buttonGap)/2
        button_yQuit=textCenterPosition[1]-heightQuit/2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                global quit
                quit=True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if(button_xStart<mouse_x<button_xStart+widthStart+2*textPadding and button_yStart<mouse_y<button_yStart+heightStart+textPadding):
                    return 1
                if(button_xHistory<mouse_x<button_xHistory+widthHistory+2*textPadding and button_yHistory<mouse_y<button_yHistory+heightHistory+textPadding):
                    return 2
                if(button_xQuit<mouse_x<button_xQuit+widthQuit+2*textPadding and button_yQuit<mouse_y<button_yQuit+heightQuit+textPadding):
                    return 0
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if(button_xStart<mouse_x<button_xStart+widthStart+2*textPadding and button_yStart<mouse_y<button_yStart+heightStart+textPadding):
                    buttonColor[0]=(207, 230, 64)
                else:
                    buttonColor[0]=(15, 219, 131)
                if(button_xHistory<mouse_x<button_xHistory+widthHistory+2*textPadding and button_yHistory<mouse_y<button_yHistory+heightHistory+textPadding):
                    buttonColor[1]=(207, 230, 64)
                else:
                    buttonColor[1]=(15, 219, 131)
                if(button_xQuit<mouse_x<button_xQuit+widthQuit+2*textPadding and button_yQuit<mouse_y<button_yQuit+heightQuit+textPadding):
                    buttonColor[2]=(207, 230, 64)
                else:
                    buttonColor[2]=(15, 219, 131)

        # Drawing
        screen.blit(titleScreenImg,(0,0))
        pygame.draw.rect(screen, BLACK, (button_xStart-textBorderWidth,button_yStart-textBorderWidth,widthStart+2*textPadding+2*textBorderWidth,heightStart+2*textBorderWidth), border_radius=int(10*RC))
        pygame.draw.rect(screen, buttonColor[0], (button_xStart,button_yStart,widthStart+2*textPadding,heightStart), border_radius=int(10*RC))
        screen.blit(txt_surfaceStart, (button_xStart+textPadding,button_yStart))

        pygame.draw.rect(screen, BLACK, (button_xHistory-textBorderWidth,button_yHistory-textBorderWidth,widthHistory+2*textPadding+2*textBorderWidth,heightHistory+2*textBorderWidth), border_radius=int(10*RC))
        pygame.draw.rect(screen, buttonColor[1], (button_xHistory,button_yHistory,widthHistory+2*textPadding,heightHistory), border_radius=int(10*RC))
        screen.blit(txt_surfaceHistory, (button_xHistory+textPadding,button_yHistory))

        pygame.draw.rect(screen, BLACK, (button_xQuit-textBorderWidth,button_yQuit-textBorderWidth,widthQuit+2*textPadding+2*textBorderWidth,heightQuit+2*textBorderWidth), border_radius=int(10*RC))
        pygame.draw.rect(screen, buttonColor[2], (button_xQuit,button_yQuit,widthQuit+2*textPadding,heightQuit), border_radius=int(10*RC))
        screen.blit(txt_surfaceQuit, (button_xQuit+textPadding,button_yQuit))
        

        pygame.display.flip()
        

    pygame.quit()

def loadingScreen():
    pygame.init()
    screenSize=(1250*RC, 700*RC)
    # Screen setup
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Loading Screen")
    clock = pygame.time.Clock()
    textColor="White"
    Boogaloo = "Media/Fonts/Boogaloo/Boogaloo-Regular.ttf"

    loadingScreenImg=utils.scaleImg(utils.loadImg("Media/Sprites/Loading/LoadingScreen.png"),screenSize)

    # Text input state
    Timer=3
    t=0
    running = True
    while running:
        dt = clock.tick(30) / 1000
        t += dt
        if(t>Timer):
            running = False
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                global quit
                quit=True
        # Drawing
        screen.blit(loadingScreenImg,(0,0))
        timerText = utils.getTextSurface(str(3-int(t)),textColor,int(90*RC),Boogaloo)
        x=screenSize[0]/2-timerText.get_width()/2
        y=screenSize[1]-timerText.get_height()-80*RC
        pygame.draw.circle(screen, (16, 145, 12), (x+timerText.get_width()/2,y+timerText.get_height()/2), 45*RC)
        screen.blit(timerText, (x,y))

        pygame.display.flip()

    pygame.quit()

def gameSettings():
    pygame.init()
    screenSize=(1250*RC, 700*RC)
    # Screen setup
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Game Settings")
    clock = pygame.time.Clock()

    # Fonts and colors
    fontSize = int(25*RC)
    Rubik_Mono_One = "Media/Fonts/Rubik_Mono_One/RubikMonoOne-Regular.ttf"

    font = pygame.font.Font(Rubik_Mono_One, int(25*RC))
    Color1=(0, 144, 184)
    Color2=(184, 0, 0)
    Color=[Color1,Color2]
    Player1Position=(150*RC,80*RC)
    Player2Position=(1100*RC,80*RC)

    minInputBoxWidth=200*RC
    input_box = [pygame.Rect(Player1Position[0], Player1Position[1], minInputBoxWidth, 30*RC),pygame.Rect(Player2Position[0], Player2Position[1], minInputBoxWidth, 30*RC)]
    active = [False,False]
    playerName = ["",""]
    color_inactive = [(111, 169, 201),(255, 112, 112)]
    color_active = [(28, 134, 238),(255, 0, 0)]
    color = [color_inactive[0],color_inactive[1]]
    textBoxColor = [(158, 206, 219),(232, 160, 160)]


    BoogalooFont = pygame.font.Font("Media/Fonts/Boogaloo/Boogaloo-Regular.ttf", int(40*RC))
    textColor=(255, 255, 255)
    buttonColor=[(15, 219, 131)]*2
    BLACK=(0,0,0)
    textCenterPosition=(625*RC,550*RC)
    textPadding = 10*RC
    textBorderWidth=2*RC
    buttonGap=60*RC

    gameSettingsTextColor=(181, 56, 31)

    settingsTextPadding=25*RC
    settingsInputBox=[pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0)]
    settingsInputBoxColor=["White","White","White"]
    settingsInputBoxActiveColor=(0,0,0)
    settingsInputBoxInactiveColor=(100,100,100)
    settingsInputBoxBorderColor=[settingsInputBoxInactiveColor]*3
    settingsInputBoxActive=[False,False,False]
    
    settingsCheckBox=[pygame.Rect(0,0,0,0),pygame.Rect(0,0,0,0)]
    settingsCheckBoxBorderColor="Black"
    settingsCheckBoxInactiveColor="Red"
    settingsCheckBoxActiveColor="Green"
    settingsCheckBoxColor=[settingsCheckBoxActiveColor]*2

    settingVals=["5","5","8",True,True]
    settingValsLimits=[(3,6),(3,6),(1,8)]

    titleScreen=utils.scaleImg(utils.loadImg("Media/Sprites/GameSettings/GameSettingsScreen1.png"),screenSize)

    # Text input state
    running = True
    while running:
        clock.tick(30)

        txt_surface_Enter = BoogalooFont.render("CONFIRM", True, textColor)
        width_Enter=txt_surface_Enter.get_width()
        height_Enter=txt_surface_Enter.get_height()
        button_xEnter=textCenterPosition[0]-width_Enter/2-textPadding + (width_Enter + buttonGap)/2
        button_yEnter=textCenterPosition[1]-height_Enter/2

        txt_surface_Back = BoogalooFont.render("BACK", True, textColor)
        width_Back=txt_surface_Back.get_width()
        height_Back=txt_surface_Back.get_height()
        button_xBack=textCenterPosition[0]-width_Back/2-textPadding - (width_Enter + buttonGap)/2
        button_yBack=textCenterPosition[1]-height_Back/2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                global quit
                quit=True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Toggle input box active state
                for i in range(0,2):
                    if input_box[i].collidepoint(event.pos):
                        active[i] = True
                        color[i] = color_active[i]
                    else:
                        active[i] = False
                        color[i] = color_inactive[i]
                for i in range(0,3):
                    if settingsInputBox[i].collidepoint(event.pos):
                        settingsInputBoxActive[i] = True
                        settingsInputBoxBorderColor[i] = settingsInputBoxActiveColor
                    else:
                        settingsInputBoxActive[i] = False
                        settingsInputBoxBorderColor[i] = settingsInputBoxInactiveColor
                for i in range(0,2):
                    if settingsCheckBox[i].collidepoint(event.pos):
                        if(settingVals[3+i] == True):
                            settingVals[3+i] = False
                            settingsCheckBoxColor[i] = settingsCheckBoxInactiveColor
                        else:
                            settingVals[3+i] = True
                            settingsCheckBoxColor[i] = settingsCheckBoxActiveColor
                mouse_x, mouse_y = event.pos
                if(button_xEnter<mouse_x<button_xEnter+width_Enter+2*textPadding and button_yEnter<mouse_y<button_yEnter+height_Enter+textPadding):
                    running = False
                    if(playerName[0]==""):
                        playerName[0]="Player1"
                    if(playerName[1]==""):
                        playerName[1]="Player2"
                    global mainMenu
                    mainMenu=False
                    return playerName,settingVals
                if(button_xBack<mouse_x<button_xBack+width_Back+2*textPadding and button_yBack<mouse_y<button_yBack+height_Back+textPadding):
                    running = False
                    mainMenu=True
                    return playerName,settingVals
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if(button_xEnter<mouse_x<button_xEnter+width_Enter+2*textPadding and button_yEnter<mouse_y<button_yEnter+height_Enter+textPadding):
                    buttonColor[0]=(207, 230, 64)
                else:
                    buttonColor[0]=(15, 219, 131)
                if(button_xBack<mouse_x<button_xBack+width_Back+2*textPadding and button_yBack<mouse_y<button_yBack+height_Back+textPadding):
                    buttonColor[1]=(207, 230, 64)
                else:
                    buttonColor[1]=(15, 219, 131)

            elif event.type == pygame.KEYDOWN:
                for i in range(0,2):
                    if active[i]:
                        if event.key == pygame.K_BACKSPACE:
                            playerName[i] = playerName[i][:-1]
                        elif(len(playerName[i])<=20):
                            playerName[i] += event.unicode
                for i in range(0,3):
                    if settingsInputBoxActive[i]:
                        if event.key == pygame.K_BACKSPACE:
                            settingVals[i] = settingVals[i][:-1]
                        else:
                            try:
                                val=int(event.unicode)
                                if(settingValsLimits[i][0]<=val<=settingValsLimits[i][1]):
                                    settingVals[i] = event.unicode    
                            except:
                                pass        
        # Drawing
        screen.blit(titleScreen,(0,0))
        for i in range(0,2):
            pygame.draw.rect(screen, textBoxColor[i], input_box[i])
            pygame.draw.rect(screen, color[i], input_box[i], int(2*RC))
            txt_surface = font.render(playerName[i], True, Color[i])
            width = max(minInputBoxWidth, txt_surface.get_width()+10)
            input_box[i].w = width 
            if(i==1):
                input_box[i].x = Player2Position[0]-input_box[1].w
            screen.blit(txt_surface, (input_box[i].x, input_box[i].y))
        
        if(playerName[0]==""):
            player1TextSurface=utils.getTextSurface("Player1",Color[0],fontSize,Rubik_Mono_One)
            player1TextSurface=player1TextSurface.convert_alpha()
            player1TextSurface.set_alpha(120)
            screen.blit(player1TextSurface, (Player1Position[0],Player1Position[1]))
        if(playerName[1]==""):
            player2TextSurface = utils.getTextSurface("Player2",Color[1],fontSize,Rubik_Mono_One)
            player2TextSurface=player2TextSurface.convert_alpha()
            player2TextSurface.set_alpha(120)
            screen.blit(player2TextSurface, (Player2Position[0]-input_box[1].w,Player2Position[1]))

        yDist=150*RC
        gameSettingsText = utils.getTextSurface("GAME SETTINGS",gameSettingsTextColor,int(30*RC),Rubik_Mono_One)
        screen.blit(gameSettingsText, (625*RC-gameSettingsText.get_width()/2,yDist))

        yDist+=gameSettingsText.get_height()+settingsTextPadding+25*RC
        gameSettingsText = utils.getTextSurface("Number of Block Rows (3-6)",gameSettingsTextColor,int(20*RC),Rubik_Mono_One)
        screen.blit(gameSettingsText, (100*RC,yDist))

        settingsInputBox[0]=pygame.Rect(100*RC+gameSettingsText.get_width()+30*RC,yDist,30*RC,30*RC)
        pygame.draw.rect(screen, settingsInputBoxColor[0], settingsInputBox[0])
        pygame.draw.rect(screen, settingsInputBoxBorderColor[0], settingsInputBox[0], int(2*RC))
        txt_surface = font.render(settingVals[0], True, gameSettingsTextColor)
        screen.blit(txt_surface, (settingsInputBox[0].x+5*RC, settingsInputBox[0].y))

        yDist+=gameSettingsText.get_height()+settingsTextPadding
        gameSettingsText = utils.getTextSurface("Number of Block Columns (3-6)",gameSettingsTextColor,int(20*RC),Rubik_Mono_One)
        screen.blit(gameSettingsText, (100*RC,yDist))

        settingsInputBox[1]=pygame.Rect(100*RC+gameSettingsText.get_width()+30*RC,yDist,30*RC,30*RC)
        pygame.draw.rect(screen, settingsInputBoxColor[1], settingsInputBox[1])
        pygame.draw.rect(screen, settingsInputBoxBorderColor[1], settingsInputBox[1], int(2*RC))
        txt_surface = font.render(settingVals[1], True, gameSettingsTextColor)
        screen.blit(txt_surface, (settingsInputBox[1].x+5*RC, settingsInputBox[1].y))

        yDist+=gameSettingsText.get_height()+settingsTextPadding
        gameSettingsText = utils.getTextSurface("Number of Birds in Queue(1-8)",gameSettingsTextColor,int(20*RC),Rubik_Mono_One)
        screen.blit(gameSettingsText, (100*RC,yDist)) 

        settingsInputBox[2]=pygame.Rect(100*RC+gameSettingsText.get_width()+30*RC,yDist,30*RC,30*RC)
        pygame.draw.rect(screen, settingsInputBoxColor[2], settingsInputBox[2])
        pygame.draw.rect(screen, settingsInputBoxBorderColor[2], settingsInputBox[2], int(2*RC))
        txt_surface = font.render(settingVals[2], True, gameSettingsTextColor)
        screen.blit(txt_surface, (settingsInputBox[2].x+5*RC, settingsInputBox[2].y))

        yDist+=gameSettingsText.get_height()+settingsTextPadding
        gameSettingsText = utils.getTextSurface("Include Block Gravity",gameSettingsTextColor,int(20*RC),Rubik_Mono_One)
        screen.blit(gameSettingsText, (125*RC,yDist))

        settingsCheckBox[0]=pygame.Rect(100*RC,yDist+1*RC,20*RC,20*RC)
        pygame.draw.rect(screen, settingsCheckBoxColor[0], settingsCheckBox[0],border_radius=int(5*RC))
        pygame.draw.rect(screen, settingsCheckBoxBorderColor, settingsCheckBox[0], int(3*RC),border_radius=int(5*RC))

        yDist+=gameSettingsText.get_height()+settingsTextPadding
        gameSettingsText = utils.getTextSurface("Include Predicted Projectile",gameSettingsTextColor,int(20*RC),Rubik_Mono_One)
        screen.blit(gameSettingsText, (125*RC,yDist))

        settingsCheckBox[1]=pygame.Rect(100*RC,yDist+1*RC,20*RC,20*RC)
        pygame.draw.rect(screen, settingsCheckBoxColor[1], settingsCheckBox[1],border_radius=int(5*RC))
        pygame.draw.rect(screen, settingsCheckBoxBorderColor, settingsCheckBox[1], int(3*RC),border_radius=int(5*RC))


        pygame.draw.rect(screen, BLACK, (button_xEnter-textBorderWidth,button_yEnter-textBorderWidth,width_Enter+2*textPadding+2*textBorderWidth,height_Enter+2*textBorderWidth), border_radius=int(10*RC))
        pygame.draw.rect(screen, buttonColor[0], (button_xEnter,button_yEnter,width_Enter+2*textPadding,height_Enter), border_radius=int(10*RC))
        screen.blit(txt_surface_Enter, (button_xEnter+textPadding,button_yEnter))

        pygame.draw.rect(screen, BLACK, (button_xBack-textBorderWidth,button_yBack-textBorderWidth,width_Back+2*textPadding+2*textBorderWidth,height_Back+2*textBorderWidth), border_radius=int(10*RC))
        pygame.draw.rect(screen, buttonColor[1], (button_xBack,button_yBack,width_Back+2*textPadding,height_Back), border_radius=int(10*RC))
        screen.blit(txt_surface_Back, (button_xBack+textPadding,button_yBack))


        pygame.display.flip()
        
    pygame.quit()

def gameHistory():
    pygame.init()
    screenSize=(1250*RC, 700*RC)
    # Screen setup
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Game History")
    clock = pygame.time.Clock()

    Rubik_Mono_One = "Media/Fonts/Rubik_Mono_One/RubikMonoOne-Regular.ttf"
    BoogalooFont = pygame.font.Font("Media/Fonts/Boogaloo/Boogaloo-Regular.ttf", int(40*RC))
    textColor=(255, 255, 255)
    buttonColor=(15, 219, 131)
    BLACK=(0,0,0)
    #Color="White"
    textCenterPosition=(625*RC,630*RC)
    textPadding = 10*RC
    textBorderWidth=2*RC
    historyDataPadding=15
    Color1=(0, 144, 184)
    Color2=(184, 0, 0)
    Color=[Color1,Color2]
    textMargin=100*RC

    loadingScreenImg=utils.scaleImg(utils.loadImg("Media/Sprites/GameSettings/GameSettingsScreen1.png"),screenSize)

    history=[]
    with open("Data/GameHistory.csv",'r') as file:
        data=file.read().strip().split()
        for d in data:
            history.append(d.split(','))

    running = True
    while running:
        clock.tick(30) / 1000

        txt_surface_Back = BoogalooFont.render("BACK", True, textColor)
        width_Back=txt_surface_Back.get_width()
        height_Back=txt_surface_Back.get_height()
        button_xBack=textCenterPosition[0]-width_Back/2-textPadding 
        button_yBack=textCenterPosition[1]-height_Back/2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                global quit
                quit=True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if(button_xBack<mouse_x<button_xBack+width_Back+2*textPadding and button_yBack<mouse_y<button_yBack+height_Back+textPadding):
                    running = False
                    return True
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                if(button_xBack<mouse_x<button_xBack+width_Back+2*textPadding and button_yBack<mouse_y<button_yBack+height_Back+textPadding):
                    buttonColor=(207, 230, 64)
                else:
                    buttonColor=(15, 219, 131)
        # Drawing
        screen.blit(loadingScreenImg,(0,0))

        yDist=40*RC
        HistoryText = utils.getTextSurface("GAME HISTORY","Black",int(35*RC),Rubik_Mono_One)
        screen.blit(HistoryText, (625*RC-HistoryText.get_width()/2,yDist))
        yDist+=HistoryText.get_height()+historyDataPadding+25*RC
        for h in history:
            x=textMargin
            pygame.draw.line(screen, "Black", (textMargin,yDist-historyDataPadding/2), (screenSize[0]-textMargin,yDist-historyDataPadding/2), int(2*RC))

            text = h[0] + "\t" + h[1] 
            HistoryText = utils.getTextSurface(text,Color[0],int(25*RC),Rubik_Mono_One)
            screen.blit(HistoryText, (x,yDist))

            HistoryText = utils.getTextSurface("V/S","Black",int(25*RC),Rubik_Mono_One)
            screen.blit(HistoryText, (625*RC-HistoryText.get_width()/2,yDist))

            text = h[3] + "\t" + h[2]
            HistoryText = utils.getTextSurface(text,Color[1],int(25*RC),Rubik_Mono_One)
            x=screenSize[0]-HistoryText.get_width()-textMargin
            screen.blit(HistoryText, (x,yDist))
            yDist+=HistoryText.get_height()+historyDataPadding

            pygame.draw.line(screen, "Black", (textMargin,yDist-historyDataPadding/2), (screenSize[0]-textMargin,yDist-historyDataPadding/2), int(2*RC))

        pygame.draw.rect(screen, BLACK, (button_xBack-textBorderWidth,button_yBack-textBorderWidth,width_Back+2*textPadding+2*textBorderWidth,height_Back+2*textBorderWidth), border_radius=int(10*RC))
        pygame.draw.rect(screen, buttonColor, (button_xBack,button_yBack,width_Back+2*textPadding,height_Back), border_radius=int(10*RC))
        screen.blit(txt_surface_Back, (button_xBack+textPadding,button_yBack))

        pygame.display.flip()

    pygame.quit()