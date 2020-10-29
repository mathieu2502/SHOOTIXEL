import pygame
from random import choice, randint
from math import cos, sin

class ElementGraphique:
	"""
	Tous est élément graphique
	"""
	def __init__(self, x, y, img, fenetre):
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.fenetre = fenetre

	def Afficher(self):
		self.fenetre.blit(self.image, self.rect)


class ElementGraphiqueAnimé(ElementGraphique):
	"""
	Animation des Elements Graphiques
	"""
	def __init__(self, x, y, img, fenetre):
		super().__init__(x, y, img[0], fenetre)
		self.images = img
		self.timer = 0
		self.numAnim = 0


	def Afficher(self):
		self.timer += 1
		if self.timer > 10:
			self.timer = 0
			self.numAnim += 1
			if self.numAnim >= len(self.images):
				self.numAnim = 0
			self.image = self.images[self.numAnim]
		super().Afficher()


class ElementAnimeDir(ElementGraphiqueAnimé):
	def __init__(self, x, y, images_all_dir, fenetre):
		super().__init__(x, y, images_all_dir["Standing"], fenetre)
		self.images_all_dir = images_all_dir
		print(*images_all_dir)
		self.direction ="Standing"
		self.old_direction="Standing"


	def Afficher(self) :
		print(self.numAnim, end="\r")

		if self.old_direction != self.direction:
			self.images = self.images_all_dir[self.direction]
			self.numAnim=0
			self.old_direction = self.direction

		super().Afficher()


class Perso(ElementAnimeDir):
	"""
	Personnage qu'incarne le joueur
	"""
	def __init__(self, x, y, images_all_dir, fenetre, largeur, hauteur):
		super().__init__(x, y, images_all_dir, fenetre)
		self.rect.x = largeur // 2 - self.rect.w // 2
		self.rect.y = hauteur - self.rect.h
		self.vie = 100
		self.vitesse = 4
		self.couldown = 20
		self.money = 0
		self.kill = 0

	def Deplacer(self, touches, largeur):
		if touches[pygame.K_d] and self.rect.x <= largeur - self.rect.w:
			self.rect.x += self.vitesse
			self.direction = "Right"

		if touches[pygame.K_a] and self.rect.x >= 0:
			self.rect.x -= self.vitesse
			self.direction = "Left"

	def Collisions(self, enemy, enemys):
		if enemy.rect.colliderect(self.rect):
			self.vie -= enemy.degats
			if enemy in enemys:
				enemys.remove(enemy)

	def Tir(self, tirs, img, touches, i):
		if touches[pygame.K_SPACE] and i%self.couldown == 0:
			tirs.append(Tir(self.rect.x - 12 + self.rect.w//2, self.rect.y - 30, img, self.fenetre, 5, 15))

	def Alive(self):
		if self.vie <= 0:
			print("Perdu")


class Enemy(ElementGraphiqueAnimé):
	"""
	Ennemis animés arrivant en face du personnage
	"""
	def __init__(self, x, y, img, fenetre, pv, v, d, largeur, hauteur):
		super().__init__(x, y, img, fenetre)
		self.vie = pv
		self.vitesse = v
		self.degats = d
		self.t = 0
		self.trucx = randint(10, largeur -10)
		self.trucy = randint(-10, 0)
		self.trucx2 = randint(50, 550)
		self.trucy2 = randint(50, 550)
		self.centerx = x
		self.centery = y
		self.deplacements = [self.DescenteLinéaire]
		self.deplacer = None


	def DescenteLinéaire(self):
		"""
		Les ennemis descendent en ligne droite
		"""
		self.rect.y += self.vitesse

	def DescenteEnCercles(self):
		"""
		Les ennemis descendent en faisant des cercles de tailles différentes
		"""
		self.t += 1
		self.rect.x = self.trucx2*cos(self.t/20) + self.trucx
		self.rect.y = self.trucy2*sin(self.t/20) + self.trucy + self.t

	def DescenteSinusoïdale(self):
		self.t += 1
		self.rect.x = self.trucx2*cos(self.t/20) + self.trucx2
		self.rect.y = self.t
	
	def ChoixDeplacement(self):
		self.deplacer = choice(self.deplacements)
	
	def difficulte(self, time):
		if time >= 500:
			self.deplacements.append(self.DescenteEnCercles)
		if time >= 1000:
			self.deplacements.append(self.DescenteSinusoïdale)

class Tir(ElementGraphique):
	"""
	Tirs du personnage
	"""
	def __init__(self, x, y, img, fenetre, v, d):
		super().__init__(x, y, img, fenetre)
		self.vitesse = v
		self.degats = d
		self.alive = True

	def Move(self):
		"""
		Fonction qui gère le déplacement des tirs
		"""
		self.rect.y -= self.vitesse


	def Collisions(self, enemy, enemys, tirs, perso):
		"""
		Fonction qui gère lorsqu'un tir et un ennemi se touchent
		"""
		if self.rect.colliderect(enemy.rect):
			for tir in tirs:
				if tir in tirs:
					tirs.remove(tir)
			enemy.vie -= self.degats
			if enemy in enemys and enemy.vie <= 0:
				enemys.remove(enemy)
				perso.kill += 1
				perso.money +=  randint(0, 1)

	def Alive(self,tirs, tir):
		if tir.rect.y < -20 and tir in tirs:
			tirs.remove(tir)