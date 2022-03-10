# GRANDI Mathieu
# FERNANDES Baptiste
# TDE

import fltk
from random import randint
fond_menu = 'images/fond_menu.png'
slitherlink = 'images/slitherlink.png'
bouton_jouer = 'images/bouton_jouer.png'
bouton_choix = 'images/bouton_choix.png'
fond = 'images/fond.png'

# -----------------------------FONCTIONS--------------------------------------


def charge_grille(grille):
    """
    Fonction qui permet d'ouvrir un ficher texte qui contient une grille,
    puis la 'convertit' en une liste d'indinces afin d'être utilisable par
    le reste du programme.
    """

    grilleFichier = open(grille, 'r')
    longueur_ligne = None
    carac_admis = ["_", "0", "1", "2", "3", ""]
    for ligne in grilleFichier:
        lst_ligne = []
        if longueur_ligne is None:
            longueur_ligne = len(ligne.strip())
        else:
            if longueur_ligne != len(ligne.strip()):
                print("Erreur, grille non valide (longueur des lignes\
                      différentes)")
                break
        for carac in ligne.strip():
            if carac.strip() not in carac_admis:
                print("Erreur, grille non valide (caractère non valide")
                break
            if carac == '_':
                lst_ligne.append(None)
            else:
                lst_ligne.append(int(carac))
        indices.append(lst_ligne)
    grilleFichier.close()


def est_trace(etat, segment):
    """
    Fonction qui permet d'indiquer si le segment est tracé ou non.

    Parameters
    ----------
    etat : dictionary
        Contient l'état des segment, si le segment est vide, il n'est pas dans
        etat, sinon il vaut 1 si le segment est tracé et -1 si il est interdit.
    segment : couple of  int couple
        Coordonnées des deux points extrêmes du segments.

    Returns
    -------
    True si segment est tracé.
    False sinon.
    """
    return True if segment in etat and etat[segment] == 1 else False


def est_interdit(etat, segment):
    """Fonction qui permet d'indiquer si le segment est interdit ou non."""
    return True if segment in etat and etat[segment] == -1 else False


def est_vierge(etat, segment):
    """Fonction qui permet d'indiquer si le segment est vierge ou non."""
    return True if segment not in etat else False


def tracer_segment(etat, segment):
    """
    Fonction permettant de modifier etat afin de représenter que\
    segment est tracé.

    Parameters
    ----------
    etat : dictionary
        Contient l'état des segment, si le segment est vide, il n'est pas dans
        etat, sinon il vaut 1 si le segment est tracé et -1 si il est interdit.
    segment : couple of int couple
        Coordonnées des deux points extrêmes du segments.

    Returns
    -------
    dictionary
        etat mis à jour.
    """
    etat[segment] = 1


def interdire_segment(etat, segment):
    """Fonction permettant de modifier etat afin de représenter que\
    segment est interdit."""
    etat[segment] = -1


def effacer_segment(etat, segment):
    """Fonction permettant de modifier etat afin de représenter que\
    segment est vierge."""
    del etat[segment]


def segments_traces(etat, sommet):
    """
    Fonction permettant d'avoir une liste qui contient les segments tracés\
    adjacents à sommet dans etat.

    Parameters
    ----------
    etat : dictionary
        Contient l'état des segment, si le segment est vide, il n'est pas dans
        etat, sinon il vaut 1 si le segment est tracé et -1 si il est interdit.
    sommet : int couple
        Coordonnées d'un sommet.

    Returns
    -------
    list
        Liste contenant les segments tracés adjacents à sommet.
    """
    coord = list(etat.keys())
    seg_adj = []
    for segment in coord:
        if sommet in segment and est_trace(etat, segment):
            seg_adj.append(segment)
    return seg_adj


def segments_interdits(etat, sommet):
    """Fonction permettant d'avoir une liste qui contient les segments\
    interdits adjacents à sommet dans etat."""
    coord = list(etat.keys())
    seg_adj = []
    for segment in coord:
        if sommet in segment and est_interdit(etat, segment):
            seg_adj.append(segment)
    return seg_adj


def segments_vierges(etat, sommet):
    """Fonction permettant d'avoir une liste qui contient les segments\
    vierges adjacents à sommet dans etat."""
    i, j = sommet
    seg_adj = []
    voisins = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    for voisin in voisins:
        if voisin[0] >= 0 and voisin[1] >= 0:
            if voisin[0] <= len(indices) and voisin[1] <= len(indices[0]):
                if sommet > voisin:
                    sommet, voisin = voisin, sommet
                if est_vierge(etat, (sommet, voisin)):
                    seg_adj.append((sommet, voisin))
            sommet = i, j
    return seg_adj


def statut_case(indices, etat, case):
    """
    Fonction permettant de déterminer l'indince d'une case est satisfait,
    est encore possible à satisfaire ou est dépassé.

    Parameters
    ----------
    indinces : list
        Contient les listes d'indices de la grille.
    etat : dictionary
        Contient l'état des segment, si le segment est vide, il n'est pas dans
        etat, sinon il vaut 1 si le segment est tracé et -1 si il est interdit.
    case : int couple
        Coordonnées d'un sommet.

    Returns
    -------
    int
        0 si indice satisfait
        1 si indice encore possible
        -1 si indice dépassé
    """
    indice = indices[case[0]][case[1]]
    if indice is None:
        return None
    else:
        nb_cotes_traces = 0
        nb_cotes_interdits = 0
        cotes_interdits = {}
        cotes_traces = {}

        # SEGMENTS TRACE
        for sommet in case_vers_Sommet(case):
            for segment in segments_traces(etat, sommet):
                if segment not in cotes_traces:
                    cotes_traces[segment] = 1
                else:
                    cotes_traces[segment] += 1
        for segment, nombre in cotes_traces.items():
            if nombre > 1:
                nb_cotes_traces += 1

        # SEGMENTS INTERDITS
        for sommet in case_vers_Sommet(case):
            for segment in segments_interdits(etat, sommet):
                if segment not in cotes_interdits:
                    cotes_interdits[segment] = 1
                else:
                    cotes_interdits[segment] += 1
        for segment, nombre in cotes_interdits.items():
            if nombre > 1:
                nb_cotes_interdits += 1

        if nb_cotes_traces == indice:
            return 0
        elif nb_cotes_traces < indice\
                and (4-nb_cotes_interdits) >= indice:
            return 1
        else:
            return -1


def case_vers_Sommet(case):
    """
    Fonction permettant d'obtenir les quatres sommets d'une case.

    Parameters
    ----------
    case : int couple
        Coordonnées d'un sommet.

    Returns
    -------
    list
        Liste des quatres sommets de case.
    """
    i, j = case
    return [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]


def tous_satisfait():
    """
    Fonction permettant de savoir si tous les indices sont satisfaits ou non.

    Returns
    -------
    bool
    """
    for i in range(len(indices)):
        for j in range(len(indices[0])):
            statut = statut_case(indices, etat, (i, j))
            if statut is not None and statut != 0:
                return False
    return True


def longueur_boucle(etat, segment):
    """
    Parameters
    ----------
    etat : dictionary
        Contient l'état des segment, si le segment est vide, il n'est pas dans
        etat, sinon il vaut 1 si le segment est tracé et -1 si il est interdit.
    segment : couple of int couple
        Coordonnées des 2 sommets d'un segment.

    Returns
    -------
    int
        Nombre de segments parcourus
    """
    if segment is None:
        return
    depart = segment[0]
    precedent = depart
    courant = segment[1]
    nb_parcouru = 1
    while courant != depart:
        segment_t = segments_traces(etat, courant)
        if len(segment_t) != 2:
            return None
        else:
            nb_parcouru += 1
            i, j = courant
            if ((i-1, j) in segment_t[0] or (i-1, j) in segment_t[1]) and (i-1, j) != precedent:
                nouv = (i-1, j)
            elif ((i+1, j) in segment_t[0] or (i+1, j) in segment_t[1]) and (i+1, j) != precedent:
                nouv = (i+1, j)
            elif ((i, j-1) in segment_t[0] or (i, j-1) in segment_t[1]) and (i, j-1) != precedent:
                nouv = (i, j-1)
            elif ((i, j+1) in segment_t[0] or (i, j+1) in segment_t[1]) and (i, j+1) != precedent:
                nouv = (i, j+1)
            precedent = courant
            courant = nouv
    return nb_parcouru


# -----------------------------INTERFACE GRAPHIQUE-----------------------------


def clic(onScreen):
    """
    Fonction permettant de détecter les cliques de l'utilsateur, et d'envoyer
    les instructions correspondantes.
    
    Parameters
    ----------
    onScreen: str
        Contient le mot qui correspond à ce qu'il y a affiché.

    Returns
    -------
    str
        Mise à jour de onScreen
    
    """
    ev = fltk.attend_ev()
    ty = fltk.type_ev(ev)
    while ty != 'ClicGauche' and ty != 'ClicDroit' and ty != 'Quitte':
        ev = fltk.attend_ev()
        ty = fltk.type_ev(ev)
    if ty == 'Quitte':
        return 'stop'

    if onScreen == 'menu':          # MENU
        if ty == 'ClicGauche':
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if x > x1_bouton and x < x2_bouton:
                if y > y1_bouton1 and y < y2_bouton1:
                    return 'play'
                if y > y1_bouton2 and y < y2_bouton2:
                    return 'choise'

    if onScreen == 'choise':
        if ty == 'ClicGauche':
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if 120 < x < 290 and 120 < y < 290:
                return 'grille1.txt'
            if 120 < x < 290 and 340 < y < 510:
                return 'grille-vide.txt'
            if 510 < x < 680 and 120 < y < 290:
                return 'grille2.txt'
            if 510 < x < 680 and 340 < y < 510:
                return 'grille-triviale.txt'
            if 310 < x < 490 and 230 < y < 400:
                return 'random'
            if 10 < x < 110 and 20 < y < 60:
                return 'menu'

    if onScreen == 'play':      # PARTIE
        global nb_segments
        if ty == 'ClicGauche' or ty == 'ClicDroit':
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if taille_marge-10 < x < nb_colonne*taille_case+40\
                    and taille_marge-10 < y < nb_ligne*taille_case+40:
                dx = (x - taille_marge) / taille_case
                dy = (y - taille_marge) / taille_case
                # VERTICAL
                if -0.1 < dx - round(dx) < 0.1:
                    if not -0.1 < dy - round(dy) < 0.1:
                        dx = round(dx)
                        dy = int(dy)
                        if ty == 'ClicGauche':
                            if est_trace(etat, ((dy, dx), (dy+1, dx))):
                                effacer_segment(etat, ((dy, dx), (dy+1, dx)))
                                nb_segments -= 1
                            else:
                                tracer_segment(etat, ((dy, dx), (dy+1, dx)))
                                nb_segments += 1
                        else:  # Clic Droit
                            if est_interdit(etat, ((dy, dx), (dy+1, dx))):
                                effacer_segment(etat, ((dy, dx), (dy+1, dx)))
                            else:
                                if est_trace(etat, ((dy, dx), (dy+1, dx))):
                                    nb_segments -= 1
                                interdire_segment(etat, ((dy, dx), (dy+1, dx)))
                # HORIZONTAL
                if -0.1 < dy - round(dy) < 0.1:
                    if not -0.1 < dx - round(dx) < 0.1:
                        dx = int(dx)
                        dy = round(dy)
                        if ty == 'ClicGauche':
                            if est_trace(etat, ((dy, dx), (dy, dx+1))):
                                effacer_segment(etat, ((dy, dx), (dy, dx+1)))
                                nb_segments -= 1
                            else:
                                tracer_segment(etat, ((dy, dx), (dy, dx+1)))
                                nb_segments += 1
                        else:  # Clic Droit
                            if est_interdit(etat, ((dy, dx), (dy, dx+1))):
                                effacer_segment(etat, ((dy, dx), (dy, dx+1)))
                            else:
                                if est_trace(etat, ((dy, dx), (dy, dx+1))):
                                    nb_segments -= 1
                                interdire_segment(etat, ((dy, dx), (dy, dx+1)))
            else:
                if nb_colonne*taille_case + 40 + 50 < x < x_fenetre-50\
                    and nb_ligne*taille_case + taille_marge - 60 < y < \
                        nb_ligne*taille_case + 20:
                    return 'solveur'

    if onScreen == 'victoire':
        if ty == 'ClicGauche':
            x = fltk.abscisse(ev)
            y = fltk.ordonnee(ev)
            if 570 < x < 750:
                if 210 < y < 260:
                    return 'play'
                if 280 < y < 330:
                    return 'menu'

    return onScreen


def menuP():
    """
    Fonction qui permet d'afficher le menu pricipal.
    """
    fltk.image(0, 0, fond_menu, ancrage='nw', tag='supp')
    fltk.image(x_fenetre/2, 80, slitherlink, ancrage='center', tag='supp')
    # fltk.texte(400, 85, "SLITHERLINK", ancrage='center', tag='supp')
    # fltk.texte(400, 220, "JOUER", ancrage='center', tag='supp')
    # fltk.texte(400, 370, "CHOIX GRILLE", ancrage='center', tag='supp')
    fltk.image(x1_bouton, y1_bouton1, bouton_jouer, ancrage='nw', tag='supp')
    # fltk.rectangle(x1_bouton, y1_bouton1, x2_bouton, y2_bouton1, tag='supp')
    fltk.image(x1_bouton, y1_bouton2, bouton_choix, ancrage='nw', tag='supp')
    # fltk.rectangle(x1_bouton, y1_bouton2, x2_bouton, y2_bouton2, tag='supp')


def dessine_grille():
    """
    Fonction qui permet de dessiner la grille du jeu.
    """
    fltk.rectangle(20, 20, nb_colonne*taille_case+40, nb_ligne*taille_case+40,
                   remplissage='lightgrey')
    x, y = taille_marge, taille_marge
    r = 2
    for ligne in range(nb_ligne+1):
        for colonne in range(nb_colonne+1):
            fltk.cercle(x, y, r, remplissage='black')
            x += taille_case
        y += taille_case
        x = taille_marge


def NumCase_vers_pixel(NumCase):
    """
    Fonction qui permet d'obtenir les coordonnées du sommet haut gauche d'une
    case.
    """
    if NumCase <= len(indices)*len(indices[0]) - 1:
        x, y = taille_marge, taille_marge
        ligne = NumCase // len(indices)
        colonne = NumCase - ligne*len(indices)
        x += colonne*taille_case
        y += ligne*taille_case
        return x, y
    else:
        print("Erreur, la case ", NumCase, " n'existe pas.")


def sommet_vers_pixel(sommet):
    """
    Fonction qui permet de convertir un sommet en coordonées en pixel.
    """
    x = sommet[1]*taille_case + taille_marge
    y = sommet[0]*taille_case + taille_marge
    return x, y


def NumCase_vers_case(NumCase):
    """
    Fonction qui permet d'obtenir une case, avec le numéro qui la représente,
    (le numéro de O à ligne*colonne).
    """
    if NumCase <= len(indices)*len(indices[0]) - 1:
        ligne = NumCase // len(indices)
        colonne = NumCase - ligne*len(indices)
        return ligne, colonne


def affiche_indices():
    """
    Fonction qui permet d'afficher les indices sur le plateau.
    """
    cmpt = -1
    for ligne_indice in indices:
        for indice in ligne_indice:
            cmpt += 1
            if indice != "_":
                color = 'black'
                statut = statut_case(indices, etat, (NumCase_vers_case(cmpt)))
                if statut is not None:
                    if statut == 0:
                        color = 'blue'
                    elif statut > 0:
                        color = 'black'
                    else:
                        color = 'red'
                x, y = NumCase_vers_pixel(cmpt)
                x += taille_case/2
                y += taille_case/2
                fltk.texte(x, y, indice, couleur=color, ancrage='center')


def affiche_segment_croix():
    """
    Fonction qui permet d'afficher les segments et les croix posés.
    """
    for segment, valeur in etat.items():
        x1, y1 = sommet_vers_pixel(segment[0])
        x2, y2 = sommet_vers_pixel(segment[1])
        if valeur == 1:
            fltk.ligne(x1, y1, x2, y2, epaisseur=3)
        if valeur == -1:
            if x1 >= x2:
                fltk.ligne(x1-5, y1+taille_case/2+5, x1+5, y1+taille_case/2-5,
                           couleur='red', epaisseur=3)
                fltk.ligne(x1+5, y1+taille_case/2+5, x1-5, y1+taille_case/2-5,
                           couleur='red', epaisseur=3)
            else:
                fltk.ligne(x1+taille_case/2-5, y1+5, x1+taille_case/2+5, y1-5,
                           couleur='red', epaisseur=3)
                fltk.ligne(x1+taille_case/2-5, y1-5, x1+taille_case/2+5, y1+5,
                           couleur='red', epaisseur=3)


def affichage_cote():
    """
    Fonction qui permet d'afficher ce qu'il y a à côté du plateau de jeu.
    """
    x = nb_colonne*taille_case + 40 + 50
    y = nb_ligne*taille_case + 40 + taille_marge - 100
    fltk.rectangle(x, y, x_fenetre-50, y+80-taille_marge)
    fltk.texte((x+x_fenetre-50)/2, (2*y+100-taille_marge-20)/2, "SOLVEUR",
               ancrage='center')
    fltk.image(x_fenetre/2, y_fenetre-45, slitherlink, ancrage='center')


def menu_choix(grille):
    """
    Fonction qui permet d'afficher le menu de choix de la grille.
    """
    x1, y1 = 90, 90
    x2 = x_fenetre-x1
    fltk.image(0, 0, fond, ancrage='nw')
    fltk.texte(x_fenetre/2, 45, "CHOIX DE LA GRILLE", ancrage='center')
    # fltk.rectangle(x1, y1, x2, y2)

    # GRILLE 1 (HAUT/GAUCHE)
    if grille == 'grille1.txt':
        fltk.rectangle(x1+30, y1+30, x1+200, y1+200, epaisseur=4)
    img_grille1 = 'images/grille1.png'
    fltk.image(x1+30, y1+30, img_grille1, ancrage='nw')

    # GRILLE VIDE (BAS/GAUCHE)
    if grille == 'grille-vide.txt':
        fltk.rectangle(x1+30, y1+250, x1+200, y1+420, epaisseur=4)
    img_grille_vide = 'images/grille-vide.png'
    fltk.image(x1+30, y1+250, img_grille_vide, ancrage='nw')

    # GRILLE 2 (HAUT/DROITE)
    if grille == 'grille2.txt':
        fltk.rectangle(x2-30, y1+30, x2-200, y1+200, epaisseur=4)
    img_grille2 = 'images/grille2.png'
    fltk.image(x2-200, y1+30, img_grille2, ancrage='nw')

    # GRILLE TRIVIALE (BAS/DROITE)
    if grille == 'grille-triviale.txt':
        fltk.rectangle(x2-30, y1+250, x2-200, y1+420, epaisseur=4)
    img_grille_triviale = 'images/grille-triviale.png'
    fltk.image(x2-200, y1+250, img_grille_triviale, ancrage='nw')

    # GRILLE RANDOM (MILIEU)
    if grille == 'random':
        fltk.rectangle(x1+220, y1+140, x1+400, y1+310, epaisseur=4)
    fltk.rectangle(x1+220, y1+140, x1+400, y1+310)
    fltk.texte(400, 315, "?", taille=100, ancrage='center')
    fltk.texte(400, 390, "aléatoire", taille=10, ancrage='center')

    # fltk.rectangle(10, 20, 110, 60)
    fltk.rectangle(45, 32, 110, 48, remplissage='black')
    fleche = [(10, 40), (45, 20), (45, 60)]
    fltk.polygone(fleche, remplissage='black')


def menu_victoire():
    """
    Fonction qui permet d'afficher le menu de victoire.
    """
    fltk.rectangle(x_fenetre-250, 150, x_fenetre-30, y_fenetre-250)
    fltk.rectangle(570, 210, 750, 260)
    fltk.texte(608, 217, "REJOUER", police='Tw Cen MT Condensed Extra Bold')
    fltk.rectangle(570, 280, 750, 330)
    fltk.texte(622, 287, "MENU", police='Tw Cen MT Condensed Extra Bold')
    fltk.texte(x_fenetre-195, 155, "VICTOIRE", couleur='red', ancrage='nw',
               police='Tw Cen MT Condensed Extra Bold')


# ----------------------------------SOLVEUR-----------------------------------

def cases_adj_segment(segment):
    """
    Fonction qui permet d'obtenir les 2 cases adjacentes à un segment.

    Parameters
    ----------
    segment : couple of int couple
        Coordonnées des 2 sommets d'un segment.

    Returns
    -------
    couple ou int couple
        Couple des 2 cases adjacentes.
    """
    i1, j1 = segment[0]
    if i1 == len(indices):
        i1 -= 1
    if j1 == len(indices[0]):
        j1 -= 1
    case1 = (i1, j1)
    if segment[0][0] != segment[1][0]:    # Segment vertical
        i = segment[0][0]
        j = segment[0][1]-1
    else:
        i = segment[0][0]-1
        j = segment[0][1]

    if 0 <= i <= len(indices) and 0 <= j <= len(indices[0]):
        case2 = (i, j)
    else:
        case2 = None
    return case1, case2


def solveur(sommet, etat, indices):
    """
    Fonction qui permet de calculer la solution d'une grille et de l'afficher
    quand elle est trouvé.
    
    Parameters
    ----------
    sommet: int couple
        Coordonnée d'un sommet
    indinces : list
        Contient les listes d'indices de la grille.
    etat : dictionary
        Contient l'état des segment, si le segment est vide, il n'est pas dans
        etat, sinon il vaut 1 si le segment est tracé et -1 si il est interdit.

    Returns
    -------
    boolean
        Grille résolu ou non.
    """
    seg_adj = segments_traces(etat, sommet)
    if len(seg_adj) == 2:
        # Si tous les indices sont satisfaits, alors afficher la solutions
        if tous_satisfait():
            fltk.efface('supp')
            fltk.mise_a_jour()
            dessine_grille()
            affiche_indices()
            affiche_segment_croix()
            return True
        else:
            return False

    # Plus de 2 côtés adjacents, donc la figure n'est plus une boucle fermée
    if len(seg_adj) > 2:
        return False

    # 0 ou 1 segments adjacents :
    if len(seg_adj) == 0 or len(seg_adj) == 1:
        i, j = sommet
        impossible = False
        for segment in segments_vierges(etat, sommet):
            tracer_segment(etat, segment)
            case1, case2 = cases_adj_segment(segment)
            if case1 is not None:
                statut1 = statut_case(indices, etat, case1)
                if (statut1 is not None and statut1 < 0):
                    effacer_segment(etat, segment)
                    impossible = True
            if case2 is not None:
                statut2 = statut_case(indices, etat, case2)
                if (statut2 is not None and statut2 < 0):
                    effacer_segment(etat, segment)
                    impossible = True
            if not impossible:
                if segment[0] != sommet:
                    new = segment[0]
                else:
                    new = segment[1]
                if solveur(new, etat, indices):
                    return True
                else:
                    effacer_segment(etat, segment)
            impossible = False
    else:
        return False


def recherche_sommet(sommet):
    """
    Fonction qui permet d'obtenir un sommet de départ pour le solveur.
    """
    for ligne in range(len(indices)):
        for colonne in range(len(indices[ligne])):
            if 3 in indices[ligne]:
                if indices[ligne][colonne] == 3:
                    return (ligne, colonne)
            elif 2 in indices[ligne]:
                if indices[ligne][colonne] == 2:
                    if sommet is None:
                        return (ligne, colonne)
                    else:
                        return (ligne+1, colonne)
            elif 1 in indices[ligne]:
                if indices[ligne][colonne] == 1:
                    if sommet is None:
                        return (ligne, colonne)
                    else:
                        return (ligne+1, colonne+1)
    return (0, 0)


# -----------------------------BOUCLE DE JEU----------------------------------
# Variables

nb = randint(0, 1)   # grille par défaut aléatoire
if nb == 1:
    grille = 'grille1.txt'
else:
    grille = 'grille2.txt'
indices = []
etat = {}
nb_segments = 0
segment = None
sommet = None

# Taille  éléments graphiques
x_fenetre, y_fenetre = 800, 600
x1_bouton, x2_bouton = x_fenetre/2 - 130, x_fenetre/2 + 130  # Commun aux 2
y1_bouton1, y2_bouton1 = y_fenetre/2 - 130, y_fenetre/2 - 30
y1_bouton2, y2_bouton2 = y_fenetre/2 + 20, y_fenetre/2 + 120

charge_grille(grille)
nb_ligne = len(indices)
nb_colonne = len(indices[0])
taille_case = ((x_fenetre - 100) / nb_colonne)/1.5
taille_marge = 30

fltk.cree_fenetre(x_fenetre, y_fenetre)

onScreen = 'menu'       # Menu principal par défaut
while onScreen != 'stop':
    if onScreen == 'menu':
        menuP()
        onScreen = clic(onScreen)

    if onScreen == 'choise':
        fltk.efface_tout()
        menu_choix(grille)
        fltk.mise_a_jour()
        Clic = clic(onScreen)
        if Clic == 'menu' or Clic == 'stop':
            onScreen = Clic
            fltk.efface_tout()
        elif Clic != 'choise':
            if Clic == 'random':
                nb = randint(0, 1)   # grille par défaut aléatoire
                if nb == 1:
                    grille = 'grille1.txt'
                else:
                    grille = 'grille2.txt'
            else:
                grille = Clic
            indices = []
            charge_grille(grille)
            nb_ligne = len(indices)
            nb_colonne = len(indices[0])
            taille_case = ((x_fenetre - 100) / nb_colonne)/1.5

    if onScreen == 'play':          # Partie en cours
        fltk.efface('supp')
        fltk.mise_a_jour()
        fltk.image(0, 0, fond, ancrage='nw')
        dessine_grille()
        affichage_cote()
        affiche_indices()
        affiche_segment_croix()
        onScreen = clic(onScreen)
        if segment not in etat.keys():
            for s, valeur in etat.items():
                if valeur == 1:
                    segment = s
        if tous_satisfait() and longueur_boucle(etat, segment) == nb_segments:
            affiche_segment_croix()
            affiche_indices()
            fltk.mise_a_jour()
            onScreen = 'victoire'

    if onScreen == "solveur":       # Solveur en fonctionnement
        fltk.texte(x_fenetre-195, y_fenetre-100,
                   "Calcul en cours...", taille=10, tag='calcul')
        fltk.mise_a_jour()
        sommet = recherche_sommet(sommet)
        if solveur(sommet, etat, indices) is not True:
            sommet = recherche_sommet(sommet)
            solveur(sommet, etat, indices)
        fltk.efface('calcul')
        fltk.mise_a_jour()
        onScreen = 'victoire'

    if onScreen == 'victoire':
        menu_victoire()
        Clic = clic(onScreen)
        # Reset des variables
        if Clic == 'menu':
            nb = randint(0, 1)
            if nb == 1:
                grille = 'grille1.txt'
            else:
                grille = 'grille2.txt'
        indices = []
        etat = {}
        nb_segments = 0
        segment = None
        sommet = None

        # Taille  éléments graphiques
        x_fenetre, y_fenetre = 800, 600
        x1_bouton, x2_bouton = x_fenetre/2 - 130, x_fenetre/2 + 130
        y1_bouton1, y2_bouton1 = y_fenetre/2 - 130, y_fenetre/2 - 30
        y1_bouton2, y2_bouton2 = y_fenetre/2 + 20, y_fenetre/2 + 120

        charge_grille(grille)
        nb_ligne = len(indices)
        nb_colonne = len(indices[0])
        taille_case = ((x_fenetre - 100) / nb_colonne)/1.5
        taille_marge = 30

        onScreen = Clic

fltk.ferme_fenetre()
