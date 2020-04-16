# -*- coding: utf-8 -*-

# Nicolas, 2020-03-20

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys


# (row,col)
# (x,y)
    
#A FAIRE
#NEAREST GOAL A REFAIRE
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def manhattan(x1,y1,x2,y2): 
    #calcul la distance de manhattan 
    #prend 4 int en paramettre
    #renvoie 1 int
    return abs(x1-x2)+abs(y1-y2)

class Node:
    #class noeud pour calculer le meilleur chemin en utilisant l'algo A*
    #prend en parametre la position via deux int, x et y, ainsi que deux autres int donnant la distance deja parcourue et la distance de manhattan jusqu a le goal
    #renvoie une class Node
    def __init__(self,x,y,dParcourue,dMan,parent=None):
        self.parent = parent #parent est un noeud ou None
        self.dParcourue = dParcourue #distance deja parcourue
        self.dMan = dMan #distance de manhattan
        self.x = x
        self.y = y

def ajouteFront(noeud,wallStates,xResto,yResto):
    #ajoute les 4 positions adjacentes a une case si elles sont atteignables
    #prend en argument un noeud, une liste des etats non atteignables, et deux int pour calculer la distance de manh jusqu'au goal
    #renvoie une liste de noeud
    l=[]
    if(((noeud.x+1,noeud.y) not in wallStates) and (noeud.x+1 >= 0) and (noeud.y >= 0) and (noeud.x+1 <= 19) and (noeud.y <= 19)):
        dMan = manhattan(noeud.x+1,noeud.y,xResto,yResto)
        l.append(Node(noeud.x+1,noeud.y,noeud.dParcourue+1,dMan,noeud))
    if(((noeud.x-1,noeud.y) not in wallStates) and (noeud.x-1 >= 0) and (noeud.y >= 0) and (noeud.x-1 <= 19) and (noeud.y <= 19)):
        dMan = manhattan(noeud.x-1,noeud.y,xResto,yResto)
        l.append(Node(noeud.x-1,noeud.y,noeud.dParcourue+1,dMan,noeud))
    if(((noeud.x,noeud.y+1) not in wallStates) and (noeud.x >= 0) and (noeud.y+1 >= 0) and (noeud.x <= 19) and (noeud.y+1 <= 19)):
        dMan = manhattan(noeud.x,noeud.y+1,xResto,yResto)
        l.append(Node(noeud.x,noeud.y+1,noeud.dParcourue+1,dMan,noeud))   
    if(((noeud.x,noeud.y-1) not in wallStates) and (noeud.x >= 0) and (noeud.y-1 >= 0) and (noeud.x <= 19) and (noeud.y-1 <= 19)):
        dMan = manhattan(noeud.x,noeud.y-1,xResto,yResto)
        l.append(Node(noeud.x,noeud.y-1,noeud.dParcourue+1,dMan,noeud))
    return l

def minMan(listNoeud):
    #renvoie le noeud avec la plus courte distance de manhattan
    #prend en argument une liste de noeud
    #renvoie un noeud
    mini = listNoeud[0].dMan
    n = listNoeud[0]
    for i in listNoeud:
        if i.dMan < mini:
            n = i
            mini = i.dMan
    return n

def minParcourue(listNoeud,xResto,yResto):
    #renvoie le deuxieme noeud le plus ancien, qui nous donnera la case adjacente vers le chemin le plus court pour atteindre l objectif
    #prend en argument une liste de noeud et deux int pour la position du goal
    #renvoie un noeud
    if listNoeud == []:
        return -1
    n = None
    for i in listNoeud:
        if ((i.x == xResto) and (i.y == yResto)):
            n = i
    if n == None:
        return -1
    if n.parent == None:
        return n
    nNext = n.parent
    while nNext.parent != None:
        n = nNext
        nNext = n.parent
    return n

def minPar(listNoeud):
    #renvoie le noeud avec la plus courte distance parcourue
    #prend en argument une liste de noeud
    #renvoie un noeud
    mini = listNoeud[0].dParcourue
    n = listNoeud[0]
    for i in listNoeud:
        if i.dParcourue < mini:
            n = i
            mini = i.dParcourue
    return n
    
def bestRowCol(posPlayer,posResto,wallStates):
    #algorythme de la strategie A*
    #prend en argument la position (x,y) du joueur, du resto et une liste des obstacles
    #rends deux int donnant les positions de la case suivante a atteindre
    xPlayer = posPlayer[0]
    yPlayer = posPlayer[1]
    xResto = posResto[0]
    yResto = posResto[1]
    front = []
    res = []
    res.append(Node(xPlayer,yPlayer,0,manhattan(xPlayer,yPlayer,xResto,yResto)))
    for i in ajouteFront(res[0],wallStates,xResto,yResto):
        front.append(i)
    test = True
    while front != []: #tant que le front n'est pas vide ie nous n avons pas exploree tous les chemins
        noeudMin = minPar(front)
        res.append(noeudMin)
        front.remove(noeudMin)
        for i in ajouteFront(noeudMin,wallStates,xResto,yResto):
            for j in front:
                if test:
                    if((i.x == j.x) and (i.y == j.y)):
                        if i.dParcourue < j.dParcourue:
                            front.append(i)
                            front.remove(j)
                        test = False
            for j in res:
                if test:
                    if((i.x == j.x) and (i.y == j.y)):
                        if i.dParcourue < j.dParcourue:
                            res.append(i)
                            res.remove(j)
                        test = False
            if test:
                front.append(i)
            test = True
    n = minParcourue(res,xResto,yResto)
    if n == -1:
        return xPlayer,yPlayer
    return n.x,n.y

def nearestGoal(posPlayer,wallStates,goalStates):
    #calcul le chemin pour aller au resto le plus proche
    #prend en argument la position (x,y) du joueur, une liste des obstacles et la liste des objectifs
    #renvoie un int qui est l indice du goalStates le plus proche
    xPlayer = posPlayer[0]
    yPlayer = posPlayer[1]
    dist = 10000
    x=-1
    for e in range(0,len(goalStates)): #on boucle sur tous les objectifs
        xResto = goalStates[e][0]
        yResto = goalStates[e][1]
        front = []
        res = []
        res.append(Node(xPlayer,yPlayer,0,manhattan(xPlayer,yPlayer,xResto,yResto)))
        for i in ajouteFront(res[0],wallStates,xResto,yResto):
            front.append(i)
        test = True
        while front != []: #tant que le front n'est pas vide ie nous n avons pas exploree tous les chemins
            noeudMin = minPar(front)
            res.append(noeudMin)
            front.remove(noeudMin)
            for i in ajouteFront(noeudMin,wallStates,xResto,yResto):
                for j in front:
                    if test:
                        if((i.x == j.x) and (i.y == j.y)):
                            if i.dParcourue < j.dParcourue:
                                front.append(i)
                                front.remove(j)
                            test = False
                for j in res:
                    if test:
                        if((i.x == j.x) and (i.y == j.y)):
                            if i.dParcourue < j.dParcourue:
                                res.append(i)
                                res.remove(j)
                            test = False
                if test:
                    front.append(i)
                test = True
        for k in res:
            if k.x == xResto and k.y == yResto:
                if k.dParcourue < dist:
                    dist = k.dParcourue
                    x = e
    return x

def no_goal_no_wall(goalStates,wallStates):
    #calcul toutes les cases non atteignables
    #prend en argument deux listes, les objectifs et les murs
    #renvoie une liste
    allowed = []
    for i in range(20):
        for j in range(20):
            if((i,j) not in wallStates):
                if((i,j) not in goalStates):
                    allowed.append((i,j))
    return allowed

def alea_player(nbPlayers,allowedStates,players,posPlayers):
    #place aleatoirement les joueurs sur les cases autorisees
    #prend en argument un int, nombre de joueur, une liste des cases atteignables, une liste des joueurs avec leur emplacement pour python et une liste des joueurs pour nous
    #modifie directement les listes via les pointeurs
    for j in range(nbPlayers):
        x,y = random.choice(allowedStates)
        players[j].set_rowcol(x,y)
        game.mainiteration()
        posPlayers[j]=(x,y)
        
def alea_resto_all(nbPlayers,nbResto,resto):
    #choisis aleatoirement les resto pour les joueurs
    #prend en argument deux int et une liste, respectivement le nombre de joueur, le nombre de resto et une liste des resto choisis pour chaque joueur
    #modifie directement la liste resto via son pointeur
    for j in range(nbPlayers):
        c = random.randint(0,nbResto-1)
        resto[j]=c

def copy_list(liste):
    #prend une liste et la copie
    #prend en argument une liste
    #renvoie une liste
    new = []
    for i in range(len(liste)):
        new.append(liste[i])
    return new

def min_list(list1,list2):
    #prend deux listes et renvoie leur min
    #prend en argument deux listes
    #renvoie une liste
    min_list = []
    for i in range(len(list1)):
        min_list.append(min(list1[i],list2[i]))
    return min_list

def dif_list(list1,list2): 
    #prend deux listes et renvoie la difference
    #prend en argument deux listes
    #renvoie une liste
    dif_list = []
    for i in range(len(list1)):
        dif_list.append(abs(list1[i]-list2[i]))
    return dif_list

def best_frequency(nbResto,min_frequency):
    max_list = max(min_frequency)
    proba_list = [0] * nbResto
    proba_list_below_one = [0] * nbResto
    actuel = 0
    indice = 0
    alea = random.random()
    for i in range(nbResto):
        proba_list[i] = (max_list - min_frequency[i])
    if(sum(proba_list) == 0):
        return random.randint(0,nbResto-1)
    somme = max(sum(proba_list),1)
    for i in range(nbResto):
        proba_list_below_one[i] = proba_list[i]/somme
    while(actuel < alea):
        actuel+=proba_list_below_one[indice]
        indice+=1
    return indice - 1
    
def strategie(nbPlayers,player_strat,nbResto,resto,posPlayers,wallStates,goalStates,min_frequency):
    new_resto = [0] * nbPlayers
    for i in range(nbPlayers):
        if(player_strat[i] == 0): #tetus
            new_resto[i] = resto[i]
        elif(player_strat[i] == 1): #aleatoire uniforme
            new_resto[i] = random.randint(0,nbResto-1)
        elif(player_strat[i] == 2 or player_strat[i] == 4): #au plus proche
            new_resto[i] = nearestGoal(posPlayers[i],wallStates,goalStates)
        elif(player_strat[i] == 3): #en fonction des tetus
            new_resto[i]= best_frequency(nbResto,min_frequency)
    return new_resto

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'kolkata_6_10'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 50000  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 500
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    nbLignes = game.spriteBuilder.rowsize
    nbColonnes = game.spriteBuilder.colsize
    print("lignes", nbLignes)
    print("colonnes", nbColonnes)
    
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
    # on localise tous les états initiaux (loc des joueurs)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets  ramassables (les restaurants)
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
    nbResto = len(goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    print ("Wall states:", wallStates)
    
    # on liste toutes les positions permises
    allowedStates = no_goal_no_wall(goalStates,wallStates)
    
    #-------------------------------
    # Placement aleatoire des joueurs, en évitant les obstacles
    #-------------------------------
        
    posPlayers = initStates

    
    alea_player(nbPlayers,allowedStates,players,posPlayers)


        
        
    
    #-------------------------------
    # chaque joueur choisit un restaurant
    #-------------------------------

    resto=[0]*nbPlayers
    alea_resto_all(nbPlayers,nbResto,resto)
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
        
    player_goal = [0]* nbPlayers #liste des joueurs qui ont atteint leur objectif, 0 non atteint, numero du resto sinon
    score = [0]* nbPlayers #liste du score des joueurs
    frequency = [0]* nbResto #frequence totale des resto
    min_frequency = [nbPlayers] * nbResto #frequence minimale de chaque resto
    last_frequency = [0] * nbResto
    indices = False
    nbTour = 0
    
    #-------------------------------
    # Affectation des stratégies aux joueurs
    #-------------------------------
    
    #Strategie 0 : tetu
    #Strategie 1 : aleatoire uniforme
    #Strategie 2 : au plus proche
    #Strategie 3 : en fonction des autres
    #Strategie 4 : au plus proche puis tetu
    
    player_strat = [0] * nbPlayers
    player_strat[0] = 4
    player_strat[1] = 4
    player_strat[2] = 4
    player_strat[3] = 4
    player_strat[4] = 4
    player_strat[5] = 4
    player_strat[6] = 4
    player_strat[7] = 4
    player_strat[8] = 4
    player_strat[9] = 4
    
    for k in posPlayers: #on ajoute aux obstacles les positions des joueurs
        wallStates.append(k)
    
    for i in range(iterations):
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            if(player_goal[j] == 0):
                row,col = posPlayers[j]
                next_row,next_col = bestRowCol(posPlayers[j],goalStates[resto[j]],wallStates) #algorythme A*
                if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19: #on regarde si on est bien dans une case accessible
                    players[j].set_rowcol(next_row,next_col)
                    game.mainiteration()
                    if((row,col) in wallStates): #si notre emplacement precedant est dans les obstacles, ce qui doit etre le cas, nous le supprimons
                        wallStates.remove((row,col))
                    row=next_row
                    col=next_col
                    if((row,col) not in goalStates): #si notre prochain emplacement n est pas dans les objectifs, nous le rajoutons aux obstacles, ce qui nous permet d etre plusieurs dans un meme resto
                        wallStates.append((row,col))
                    else: #si nous avons atteins un resto, nous actualisons des listes de frenquence et d atteinte d objectifs
                        num_resto = goalStates.index((row,col))
                        player_goal[j] = num_resto + 1
                        frequency[num_resto]+=1
                    posPlayers[j]=(row,col)
                if(0 not in player_goal): #si tout le monde a atteint son resto
                    resto_vide = []
                    for k in range(nbResto): #on boucle sur le nombre de resto
                        indices = [l+1 for l, x in enumerate(player_goal) if x == k+1] #on cherche les indices des joueurs dans ce resto
                        if indices: #si il y a au moins un joueur dans ce resto
                            if(len(indices) == 1):
                                if (player_strat[indices[0]-1] == 4):
                                    player_strat[indices[0]-1] = 0       
                            add_score = indices[random.randrange(len(indices))] #on choisis aleatoirement un des joueurs de ce resto
                            score[add_score-1]+=1 #et on lui ajoute 1 a son score ie il a ete servi
                        else: #on cherche le premier joueur avec la strat 4 pour lui attribuer en tetu un resto qui est vide
                            resto_vide.append(k)
                        indices = False
                    for k in range(len(resto_vide)):
                        first_quatre = player_strat.index(4)
                        resto[first_quatre] = resto_vide[k]
                        player_strat[first_quatre] = 0
                    dif_frequency = dif_list(frequency,last_frequency) #frequence au dernier tour
                    min_frequency = min_list(min_frequency,dif_frequency)  #on précise notre calcul du nombre de têtus
                    last_frequency = copy_list(frequency) #on copie la liste pour ne pas avoir de problemes de pointeurs
                    alea_player(nbPlayers,allowedStates,players,posPlayers) #on replace aleatoirement tous les joueurs sur la map
                    nbTour+=1
                    old_resto = copy_list(resto) #on copie la liste pour ne pas avoir de problemes de pointeurs
                    resto = strategie(nbPlayers,player_strat,nbResto,old_resto,posPlayers,wallStates,goalStates,min_frequency) #on choisis le nouveau resto goal pour chaque joueur en fonction de sa strategie
                    
                    
                    player_goal = [0]*nbPlayers #on reinitialise la liste des joueurs qui ont atteint leur objectif
                    

                    game.mainiteration()
            
    print("Score final : ",score)
    print("Moyenne par tour : ",sum(score)/nbTour)
    print("Moyenne par itération : ",sum(score)/iterations)
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()