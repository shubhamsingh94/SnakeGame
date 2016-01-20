import pygame
import time
import random

x = pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')
gameDisplay.fill(white)
pygame.display.update()

block_size = 20
applethickness = 30
FPS = 20

icon = pygame.image.load('appleimage.jpg')
pygame.display.set_icon(icon)

img = pygame.image.load('snakeimage.jpg')
appleimage = pygame.image.load('appleimage.jpg')

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont(None,30)
midfont = pygame.font.SysFont(None,50)
largefont = pygame.font.SysFont("comicsansms",80)

direction = "right"

def pause():
	paused = True
	message_to_screen("Paused",black,-100,"large")
	message_to_screen("Press Space to continue or Q to quit",black, 30)
	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		#gameDisplay.fill(white)
		
	clock.tick(5)


def score(score):
	text1 = smallfont.render("Score : " + str(score), True, black)		
	f = open('max_score.txt','r')
	max_score = f.read()
	f.close()
	text2 = smallfont.render("Highest Score : " + str(max(score,max_score)), True, black)
	f = open('max_score.txt','w')
	f.write(str(max(score,int(max_score))))
	f.close()
	gameDisplay.blit(text2,(display_width-180,0))
	gameDisplay.blit(text1,(0,0))

def randApplegen():
	randAppleX = round(random.randrange(0,display_width-applethickness))#/10.0)*10.0
	randAppleY = round(random.randrange(0,display_height-applethickness))#/10.0)*10.0
	return randAppleX, randAppleY


def intro():
	intro = True
	message_to_screen("Welcome to Slither",black,-100,"large")
	message_to_screen("The objective of the game is to eat apples",green,0)
	message_to_screen("The more apples you eat, the longer you get",green,40)
	message_to_screen("If you run into yourself,or edges, you die!",green, 80)
	message_to_screen("Press C to play, Space to pause and Q to quit",red,150)
	pygame.display.update()

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		clock.tick(15)

def snake(snakelist):
	for xny in snakelist[:-1]:
		pygame.draw.rect(gameDisplay,green,[xny[0],xny[1],block_size,block_size])

	if(direction == "right"):
		head = pygame.transform.rotate(img,270)
	elif(direction == "left"):
		head = pygame.transform.rotate(img,90)
	elif(direction == "up"):
		head = img
	elif(direction == "down"):
		head = pygame.transform.rotate(img,180)

	gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))

def text_objects(text,color,size):
	if(size == "small"):
		textsurface = smallfont.render(text,True,color)
	elif(size == "middle"):
		textsurface = midfont.render(text,True,color)
	elif(size == "large"):
		textsurface = largefont.render(text,True,color)

	return textsurface, textsurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):
	# screen_text = font.render(msg, True, color)
	# gameDisplay.blit(screen_text, [display_width/2,display_height/2])
	textsurf, textsurf_rect = text_objects(msg,color,size)
	textsurf_rect.center = (display_width/2), (display_height/2) + y_displace
	gameDisplay.blit(textsurf,textsurf_rect)



def gameLoop():
	global direction
	direction = "right"

	gameExit = False
	gameOver = False

	lead_x = display_width/2
	lead_y = display_height/2
	lead_x_change = 10
	lead_y_change = 0

	randAppleX, randAppleY = randApplegen()

	snakelist = []
	snakelength = 1

	while not gameExit:

		if gameOver == True:
			message_to_screen("Game Over",red,-50,"large")
			message_to_screen("Press C to play again or Q to quit the game",black,50,"small")
			pygame.display.update()

		while gameOver == True:
			#gameDisplay.fill(white)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					if event.key == pygame.K_c:
						gameLoop()
						pygame.quit()
						quit()
				if event.type == pygame.QUIT:
					gameExit = True	
					gameOver = False
					# pygame.quit()
					# quit()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True	
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and direction != "right":
					direction = "left"
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT and direction != "left":
					direction = "right"
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP and direction != "down":
					direction = "up"
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN and direction != "up":
					direction = "down"
					lead_y_change = block_size
					lead_x_change = 0
				elif event.key == pygame.K_SPACE:
					pause()
		
		if lead_x + block_size/2 >= display_width or lead_x < 0 or lead_y + block_size/2 >= display_height or lead_y < 0:
			gameOver = True

		lead_x += lead_x_change
		lead_y += lead_y_change

		gameDisplay.fill(white)
		gameDisplay.blit(appleimage,(randAppleX,randAppleY))
		#pygame.draw.rect(gameDisplay,red,[350,350,100,10])
		# gameDisplay.fill(red, rect=[200,200,50,50])		#good method

		snakehead = []
		snakehead.append(lead_x)
		snakehead.append(lead_y)
		snakelist.append(snakehead)

		if len(snakelist) > snakelength:
			del snakelist[0]

		for each in snakelist[:-1]:
			if each == snakehead:
				gameOver = True

		snake(snakelist)
		score(snakelength-1)

		pygame.display.update()

		if lead_x >= randAppleX and lead_x <= randAppleX + applethickness or lead_x + block_size >= randAppleX and lead_x + block_size <= randAppleX + applethickness:
			if lead_y >= randAppleY and lead_y <= randAppleY + applethickness or lead_y + block_size >= randAppleY and lead_y + block_size <= randAppleY + applethickness:
				randAppleX, randAppleY = randApplegen()
				snakelength += 1;				

		clock.tick(FPS)

intro()
gameLoop()

# message_to_screen("Game Over",red)
# pygame.display.update()
# time.sleep(2)
pygame.quit()
quit()
