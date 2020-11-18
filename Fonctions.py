import pygame
from random import randint

from Class import Enemy
from Class import Bonus

# from Class import *


def images(font):
    """
    Fonction qui recupère les images dans le dossier
    """
    bank = {}

    bank["fond"] = pygame.image.load("./Images/fond.jpg")
    bank["enemys"] = []
    bank["tirs"] = pygame.image.load("./Images/Tirs/bullet_blue.png")
    bank["boss"] = []
    bank["boost"] = pygame.image.load("./Images/boost.png")

    # for i in range(1, 23):
    # 	bank["enemys"].append(pygame.image.load("./Images/Enemy/ennemi" + str(i) + ".png"))

    # ============= Menu =============
    bank['Main'] = pygame.image.load("./images/Menu/BgM.jpg").convert_alpha()
    bank['Play'] = pygame.image.load("./Images/Menu/Play.png")
    bank['Option'] = pygame.image.load("./Images/Menu/Option.png")
    bank['Exit'] = pygame.image.load("./Images/Menu/Exit.png")
    bank['Pointeur'] = pygame.image.load("./Images/Menu/Pointeur.png")

    font_menu = pygame.font.Font('Text/Kemco Pixel Bold.ttf', 70)
    bank["text_menu"] = font_menu.render('SHOOTIXEL', True, (255, 255, 255))
    # ============= Menu =============

    # ============= Life =============
    bank['Vie25'] = pygame.image.load("./Images/Life25.png").convert_alpha()
    bank['Vie50'] = pygame.image.load("./Images/Life50.png").convert_alpha()
    bank['Vie75'] = pygame.image.load("./Images/Life75.png").convert_alpha()
    bank['Vie100'] = pygame.image.load("./Images/Life100.png").convert_alpha()
    # ============= Life =============

    bank["enemys"].append(pygame.image.load(
        "./Images/Vaisseaux/Enemy02Red1.png"))
    bank["boss"].append(pygame.image.load(
        "./Images/Vaisseaux/Enemy01_Red_Frame_1_png_processed.png"))

    imgPerso = {}
    imgPerso["Right"] = []
    imgPerso["Left"] = []
    imgPerso["Standing"] = []

    for i in range(1, 3):
        imgPerso["Right"].append(pygame.image.load(
            "./Images/Vaisseaux/PlayerRight" + str(i) + ".png"))
        imgPerso["Left"].append(pygame.image.load(
            "./Images/Vaisseaux/PlayerLeft" + str(i) + ".png"))

    imgPerso["Standing"].append(pygame.image.load(
        "./Images/Vaisseaux/Standing.png"))

    bank["perso"] = imgPerso
    bank["score"] = font.render("Score :", 1, (255, 0, 0))

    return bank


def New_Enemy(img, enemys, largeur, hauteur, fenetre, i):
    """
    Fonction qui ajoute 1 ennemi à la liste d'ennemis
    """

    enemys.append(Enemy(randint(50, largeur - 50), randint(-hauteur //
                                                           2, 0), img, fenetre, 15, 2, 20, largeur, hauteur, "Enemy"))
    enemys[-1].Choix(i)


def New_Boss(img, enemys, largeur, hauteur, fenetre, i):
    """
    Fonction qui ajoute 1 boss à la liste d'ennemis

    """
    enemys.append(Enemy(largeur//2 - 15, -10, img, fenetre,
                        200, 1, 0, largeur, hauteur, "Boss"))
    enemys[-1].Choix(i)


def BossTimer(boss):
    """
    Fonction qui détermine lorsque le boss est terminé
    """
    if boss.vie >= 0 and boss.type == "Boss":
        return True
    return False
    enemys[-1].ChoixDeplacement()


def New_Bonus(time, tabBonus, bank, fenetre):
    if time % 200 == 0 and len(tabBonus) <= 1:
        tabBonus.append(Bonus(bank["boost"], fenetre, 0, 0, "speed", time))


def SupprTrucs(liste):
    """
    Fonction qui supprime les éléments des listes qui ne doivent plus yêtre
    """
    liste_keep = []
    for element in liste:
        if element.vie > 0:
            liste_keep.append(element)

    x = len(liste) - len(liste_keep)
    return x, liste_keep


def move_pointeur(selection_menu, touches, son_pointeur_menu):
    """
    Fonction qui gère le pointeur du Menu
    """

    # évitons que le pointeur se barre trop loin
    if selection_menu >= 4:
        selection_menu = 1
    if selection_menu == 0:
        selection_menu = 3

    if touches[pygame.K_DOWN]:
        son_pointeur_menu.play()
        selection_menu += 1

    if touches[pygame.K_UP]:
        son_pointeur_menu.play()
        selection_menu -= 1

    return selection_menu
