# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 11:06:37 2020

@author: Paul
"""


import random
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def grapheAleatoire(nom,nbSommets,nbArcs):  #fonction pour créer un graphe aléatoire
    sommets=[]
    arcs=[]
    for i in range (nbSommets):
        sommets.append(ascii_uppercase[i])
    for i in range(nbArcs):
        arcs.append((sommets[random.randrange(nbSommets)],sommets[random.randrange(nbSommets)],random.randrange(10)))
    
    return (nom,sommets,arcs)

donnees=grapheAleatoire('graphe',10,25)

# donnees=('Graphe1', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
#           [('A', 'A', 2), ('A', 'B', 5), ('A', 'C', 8), ('B', 'C', 6),
#           ('B', 'D', 8), ('B', 'E', 6), ('C', 'B', 2), ('C', 'D', 1),
#           ('C', 'E', 2), ('D', 'E', 3), ('D', 'F', 1), ('E', 'A', 5),
#           ('E', 'D', 1), ('E', 'G', 5), ('F', 'D', 4), ('F', 'E', 1),
#           ('F', 'G', 3), ('F', 'H', 6), ('E', 'I', 3), ('G', 'H', 2),
#           ('H', 'B', 6), ('H', 'B', 7), ('I', 'J', 4), ('J', 'I', 5)])




import numpy as np

import subprocess
import webbrowser
import os

class Graphe():
    
    def __init__(self,donnee):
        
        if (type(donnee)==str):  #un graphe peut être défini à partir d'un nom de fichier contenant les données du graphe ou par un tuple
            import sp
            fichier=open(donnee,'r')
            texte=fichier.read()
 
            def parser():       #fonction parser permetant de lire le contenu du fichier et renvoyer un tuple
                commentaire=sp.R(r'#.*')
                blancs=sp.R(r'\s+')
                nom=sp.R(r'[a-zA-Z]\w*') /str
                poids=sp.R(r'\d+') /int
                
                with sp.Separator(blancs|commentaire):
                    
                    
                    graphe=sp.Rule()
                    nomGraphe=sp.Rule()
                    sommets=sp.Rule()
                    arcs=sp.Rule()
                    Sommet=sp.Rule()
                    arc=sp.Rule()
                    sommet=sp.Rule()
                    
                    
                    
                    graphe|='<GRAPHE Name=' & nomGraphe & '>' & sommets & arcs & '</GRAPHE>'
                    nomGraphe|='"' & nom & '"' 
                    sommets|='<SOMMETS>' & Sommet[:] & '</SOMMETS>'
                    arcs|='<ARCS>' & arc[:] & '</ARCS>'
                    Sommet|=sommet & ';'
                    arc|= sommet & ':' & sommet & ':' & poids & ';'
                    sommet|=nom
                    
                
                return graphe
            
            decoder=parser()
            try:
                
                donnee=decoder(texte)   #on récupère le tuple pour la création du graphe
                
                
            except SyntaxError as erreur:
                print(erreur)
            
                    
            fichier.close() 
        
        self.nom=donnee[0]      #attribution du nom du graphe
        self.sommets=[]     #liste contenant tous les sommets du graphe
        self.arcs=[]        #liste contenant tous les arcs du graphe
        for i in range (len(donnee[1])):        #ajout des sommets dans la liste
            self.sommets.append(Sommet(donnee[1][i]))
            self.sommets[-1].ajouterGraphe(self)        #pour chaque sommet on lui dit qu'il appartient au graphe
        for j in range (len(donnee[2])):        #ajout des arcs dans la liste
            self.arcs.append(Arc(self.sommets[self.sommets.index(Sommet(donnee[2][j][0]))],self.sommets[self.sommets.index(Sommet(donnee[2][j][1]))],donnee[2][j][2])) #permet de créer les arcs avec les sommets déjà existants
    
    def __str__(self):
        texte=f'{self.nom} :\n'
        for arc in self.arcs:
            texte+=f'{arc.__str__()}\n'
        return(texte)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.nom)
    
    def plusLongChemin(self):   ##détermine le sommet de départ et d'arrivée, la distance et le chemin du plus long chemin du graphe
        distanceChemin=0        #distance maximale du graphe
        sommetDepart=None
        sommetArrivee=None
        for sommet in self.sommets:   #on regarde l'ensemble des plus court chemins possibles
            distance=sommet.dijkstra()
            for som in distance:
                if som[1]>distanceChemin: #si on trouve un chemin plus long
                    distanceChemin=som[1]   #on actualise la distance maximale,
                    sommetDepart=sommet     #le sommet de départ
                    sommetArrivee=som       #et le sommet d'arrivée
        dijkstraSommetDepart=sommetDepart.dijkstra()     #on récupère les infos du plus long chemin
        sommetDepart.plusLongChemin=True    
        chemin=[sommetArrivee[2]]   #on ajoute l'arc permetant d'arriver au sommet d'arrivée dans le chemin
        sommetArrivee[2].plusLongChemin=True    #on indique que cet arc fait partie plus long chemin
        sommetArrivee[2].arrivee.plusLongChemin=True #de même pour le sommet d'arrivée
        while chemin[-1].depart!=sommetDepart: #on retrace le chemin à l'envers
            sommetPrecedent=chemin[-1].depart
            positionSommetPrecedent=0
            for k in range (len(dijkstraSommetDepart)):     #on cherche la position du sommet précédent dans la liste dijkstraSommetDepart
                if dijkstraSommetDepart[k][0]==sommetPrecedent:
                    positionSommetPrecedent=k
                    break
            arcPrecedent=dijkstraSommetDepart[positionSommetPrecedent][2]   #l'arc d'arrivée au sommet précédent fait partie du chemin 
            arcPrecedent.plusLongChemin=True
            arcPrecedent.arrivee.plusLongChemin=True    
            chemin.append(arcPrecedent)     #on ajoute l'arc dans le chemin
        affichage=f"""Graphe étudié : {self.nom}     
        
Plus long des plus courts chemins : entre {sommetDepart} et {sommetArrivee[0]} de distance {distanceChemin}
    
Arcs contenus dans le chemin :
            """
        
        for i in range(len(chemin)-1,-1,-1):
            message=f"""
    Origine : {chemin[i].depart}, Extrémité : {chemin[i].arrivee}, Poids : {chemin[i].poids}"""
            
            affichage+=message
        print(affichage)
        return(sommetDepart,sommetArrivee[0],distanceChemin,chemin)

    def graphviz(self):     ##création du fichier .gv puis de l'image du graphe avec grapviz
        fichier = open("data.gv", "w")
        (sommetDepart,sommetArrivee,distanceChemin,chemin)=self.plusLongChemin()
        output="""
    Digraph D { 
    rankdir="LR"; \n"""
               
        
        for arc in self.arcs:
            ajout=f'{arc.depart.nom} -> {arc.arrivee.nom} [label={str(arc.poids)}'
            if arc.plusLongChemin==True:    #affichage en rouge des arcs contenus dans le chemin
                ajout+=',color=red'
                
            ajout+=']; \n'    
            output+=ajout
        
        for sommet in self.sommets:
            if sommet.plusLongChemin==True:
                output+=(sommet.nom+' [color=red,fontcolor=red];\n')  #affichage en rouge des sommets contenus dans le chemin  
        
        output+='}'
        fichier.write(output)
        fichier.close()
        subprocess.call(["D:\\Programmes\\graphviz\\dot.exe", "-Tpng", "-ographe.png", "data.gv"])
        return (sommetDepart,sommetArrivee,distanceChemin,chemin)
    
    def html(self): #mise en forme des résultats sous forme d'une page HTML

        pageHTML = open("dijkstra.html", "w",encoding='utf-8')
        (sommetDepart,sommetArrivee,distanceChemin,chemin)=self.graphviz()

        page=f'''<html>
	<head>
        <title>Projet 104</title>
		<meta charset="utf-8">
		<link rel="stylesheet" href="style.css" >
	</head>

	<body>
		<h2>Graphe étudié : {self.nom}</h2>
		<img src="graphe.png" alt="Graphe"/>
		<p>Représentation du graphe avec en rouge le plus long des plus court chemins</p>'''
    
        page+=f'''
		<h2>Plus long des plus courts chemins : entre {sommetDepart.nom} et {sommetArrivee.nom} de distance {distanceChemin}</h2>
		<p>Arcs contenus dans le chemin :</p>
        <blockquote>'''
    
    
        for i in range(len(chemin)-1,-1,-1):
            message="""
		-Origine : <b>{}</b>, Extrémité : <b>{}</b>, Poids : <b>{}</b></br>"""
            message=message.format(chemin[i].depart,chemin[i].arrivee,chemin[i].poids)
            page+=message
        page+='''</blockquote>
		<h2>Distance minimale entre les sommets :</h2>'''
    
        page+='''
		<table>
			<tr>
				<th> </th>'''
        nombreSommets=len(self.sommets)
        dico={}     #création d'un dictionnaire pour connaitre l'ordre/emplacement des sommets dans le tableau
        for i in range (nombreSommets):
            page+=f'''
				<th>{self.sommets[i].nom}</th>'''
            dico[self.sommets[i].nom]=i
        page+='''
			</tr>'''
        
        for sommet in self.sommets:
            distances=sommet.dijkstra()
            page+=f'''
			<tr>
				<th>{sommet.nom}</th>'''
            valeurs=[]      #liste contenant l'ensemble des distances pour atteindre les sommets depuis le sommet de la ligne du tableau
            for k in range(nombreSommets):
                valeurs.append(0)
            for som in distances:
                valeurs[dico[som[0].nom]]=som[1]    #on ajoute la distance du chemin à l'emplacement du sommet concerné
    
            for s in range(nombreSommets):
                if valeurs[s]==0:
                    page+='''
				<td>-</td>'''
                
                elif valeurs[s]==distanceChemin :   #affichage du(des) couple(s) avec la plus grande distance en gras
                    page+=f'''
				<td><b>{valeurs[s]}</b></td>'''
                else :
                    page+=f'''
				<td>{valeurs[s]}</td>'''
                
            page+='''
			</tr>'''
            
        page+='''
		</table>'''
    
        page+='''
	</body>
</html>'''
    
        pageHTML.write(page)
        pageHTML.close()
        
        
        styleCSS=open("style.css", "w")     #création du fichier css
        styleCSS.write('''table{
  border-collapse: collapse;
}

th, td{
  border: 1px solid black;
  padding: 10px;
  text-align:center;
}''')
        styleCSS.close()
    
    
        webbrowser.open(os.getcwd()+"\\dijkstra.html") #ouvre directement la page html
                              
    def tableau(self): ##renvoie le tableau des distances dans la console
        nombreSommets=len(self.sommets)
        dico={}     #création d'un dictionnaire pour classer les sommets, nécéssaire car dijkstra renvoie pas forcément les sommets dans l'ordre ni tous
        tableur='''
Distance minimale entre les sommets :
   | '''
        for i in range (nombreSommets):     #création de la première ligne du tableau
            tableur+=(self.sommets[i].nom+' | ')
            dico[self.sommets[i].nom]=i
        tableur+='\n'
            
        for sommet in self.sommets:           #pour chaque sommet du graphe
            distance=sommet.dijkstra()    #on regarde la distance la plus courte pour atteindre les autres sommets
            ligne=f' {sommet.nom} |'  #sommet de départ
            valeurs=[]
            for k in range(nombreSommets): #on créé une liste des distances pour tous les sommets
                valeurs.append(0)
            for som in distance:
                valeurs[dico[som[0].nom]]=som[1] #pour chaque sommet on actualise sa distance dans la liste en respectant l'ordre grâce au dictionnaire
                
            for s in range(nombreSommets):  #création de la ligne du tableau avec les valeurs triées 
                if valeurs[s]!=0:
                    ajout='{:2d} |'
                    ajout=ajout.format(valeurs[s])
                    ligne+=ajout
                else :
                    ligne+=' - |'
            ligne+='\n'
                
            tableur+=ligne #on ajoute la ligne au tableau           
        print(tableur)
          

class Sommet():
    def __init__(self,nom):
        self.nom=nom        #nom du sommet
        self.plusLongChemin=False       #permet de savoir si le sommet est sur le plus long chemin
        self.graphe=None        #graphe auquel il appartient
    
    def __str__(self):
        return(self.nom)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.nom)
    
    def __eq__(self, other):        #définition de l'égalité entre 2 sommets, utile pour l'algorithme de Dijktstra
        if type(other)==Sommet:
            return (self.nom==other.nom)
    
    def ajouterGraphe(self,Graphe):     #permet d'attribuer le graphe d'appartenance
        self.graphe=Graphe
        
    def arcsIssusDeSc(self):           #permet d'avoir tous les arcs d'un graphe qui partent d'un sommet
        arcsIssusDeSc=set()
        for arc in self.graphe.arcs:
            if self==arc.depart:              #on regarde le sommet de départ de tous les arcs du graphe
                arcsIssusDeSc.add(arc)      #si ce sommet est Sc alors on l'ajoute à l'ensemble des arcs
        return arcsIssusDeSc 

    def dijkstra(self):        #permet de connaitre l'ensemble des sommets atteignables depuis un sommet avec la distance les séparant et le dernier arc pour y arriver
        ESdc=[]                     #ainsi que la distance entre les 2 sommets et l'arc d'arrivée
        ESdmc=[]  
        dmin=0
        Sc=self           #initialisation du sommet courant
        ESdmc.append([self,0,Arc(Sc,Sc,0)])   #la distance minimale pour aller au point de départ est forcément nulle
        while True:
            arc_a_visiter=set()     #on cherche l'ensemble des arcs issu de Sc dont le sommet d'arrivée ne fait pas parti de ESdmc
            for arc in Sc.arcsIssusDeSc():  #on regarde tous les arcs issus de Sc
                sommet_ESdmc=list(np.array(ESdmc)[:,0])    #on créer une liste de tous les sommets de ESdmc en se debarassant des distances et arcs d'arrivées
                if arc.arrivee not in sommet_ESdmc:     #si la destination de l'arc ne fait pas partie des sommets de ESdmc
                    arc_a_visiter.add(arc)          #alors c'est un arc à visiter
            
            if (arc_a_visiter==set())&(ESdc==[]): #condition d'arrêt de l'algorithme ie on connait toutes les distances minimales et il n'y a plus aucun arc à visiter 
                break
            for arc in arc_a_visiter:
                S=arc.arrivee
                d=dmin+arc.poids
                if ESdc==[]:
                    ESdc.append([S,d,arc])
                else:    
                    sommet_ESdc=list(np.array(ESdc)[:,0]) #étape impossible si ESdc est vide d'où la vérification
                    if S not in sommet_ESdc:
                        ESdc.append([S,d,arc]) #le sommet n'a pas encore été visité donc on l'ajoute dans ESdc
                    else:
                        D=ESdc[sommet_ESdc.index(S)][1]   #le sommet a déjà été visité et on récupère la distance qu'on avait calculé par un autre chemin
                        if d<D:
                            ESdc[sommet_ESdc.index(S)]=[S,d,arc] #on actualise la distance et l'arc d'arrivée si le chemin est plus court
            distance_ESdc=list(np.array(ESdc)[:,1])  #on récupère l'ensemble des distances pour chaque sommet pour identifier le sommet de ESdc le plus proche de Sd
            positionSproche=distance_ESdc.index(min(distance_ESdc)) #on récupère la position du sommet dans la liste des distances
            Sproche=ESdc[positionSproche]   #on a notre sommet le plus proche
            ESdmc.append(ESdc.pop(positionSproche)) #ce sommet passe alors de ESdc à ESdmc
            Sc=Sproche[0]  #nouveau sommet courant
            dmin=Sproche[1]     #nouvelle distance minimale
            
        return ESdmc

    
class Arc():
    
    def __init__(self,depart,arrivee,poids):
        self.poids=poids
        self.depart=depart
        self.arrivee=arrivee
        self.plusLongChemin=False       #permet de savoir si l'arc est sur le plus long chemin
        
    def __str__(self):
        return (f'{self.depart} --{self.poids}--> {self.arrivee}')
    
    def __repr__(self):
        return '{}({},{},{})'.format(self.__class__.__name__, self.depart,self.arrivee,self.poids)
            

a=Graphe('grapheProjet.txt')  #nom du fichier texte avec les données à inserer
# a=Graphe(donnees)
a.html()
a.tableau()