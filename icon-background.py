#!/usr/bin/env python3

"""
    Anthony Nelzin-Santos
    anthony@nelzin.fr
    https://anthony.nelzin.fr

    European Union Public License 1.2
"""

# @TODO
# Rendre le script plus robuste (petites icônes, couleurs étranges…)

import biplist, getopt, os, sys
from collections import Counter
from PIL import Image, ImageDraw
from random import randrange
from sklearn.cluster import KMeans

# EXTRACTION DE L'ICÔNE
# L'icône ne possède pas un chemin fixe, mais un chemin défini
# par le développeur dans le plist. Parfois, le développeur oublie
# même de spécifier l'extension. Il faut donc reconstruire le chemin
# sans oublier d'ajouter l'extension.
def extract_icon(app_path):
    plist_path = os.path.join(app_path, "Contents", "Info.plist")
    plist = biplist.readPlist(plist_path)
    icon_ref = plist["CFBundleIconFile"]
    icon_name, icon_extension = os.path.splitext(icon_ref)
    if not icon_extension:
        icon_extension = ".icns"
    icon_path = icon_name + icon_extension
    
    return os.path.join(app_path, "Contents", "Resources", icon_path)

# ÉVALUATION DE LA COULEUR DOMINANTE DE L'ICÔNE
# Les icônes possède un masque de transparence, qu'il faut aplatir.
# Les zones noires issues de l'applatissement faussent les calculs.
# Mieux vaut donc extraire une section plus ou moins centrale de
# l'icône. Un nombre tiré au hasard permet de décaler la zone d’extraction
# d'un essai à l'autre, ce qui peut produire des résultats différents.
# (La ligne 57 peut être décommentée pour observer les variations.)
# On transforme ensuite l'image en liste de pixels, que l'on regroupe
# en clusters. On trouve le centre des clusters, puis on sélectionne
# le cluster dominant.
def get_color(icon_path, k=5, img_size=250, random=250):
    icon = Image.open(icon_path)
    icon = icon.convert("RGB")

    width, height = icon.size
    random = randrange(-random, random)
    left = (width - img_size)/2+random
    top = (height - img_size)/2+random
    right = (width + img_size)/2+random
    bottom = (height + img_size)/2+random
    crop = icon.crop((left, top, right, bottom))
    #crop.save("output.jpg")
    
    pixels = list(crop.getdata())
    cluster = KMeans(n_clusters = k)
    labels = cluster.fit_predict(pixels)
    count = Counter(labels)
    dominant = cluster.cluster_centers_[count.most_common(1)[0][0]]

    return list(dominant)

# CRÉATION DE L'ARRIÈRE-PLAN
# À partir de la couleur dominante, on crée un arrière-plan de
# 1 200 pixels de côté.
def create_bg(color, bg_width=2000, bg_height=1200):
    red = int(color[0])
    green = int(color[1])
    blue = int(color[2])
    bg = Image.new("RGB", (bg_width, bg_height), (red, green, blue))

    return bg

# ASSEMBLAGE FINAL
# Enfin, on réunit l'icône et l'arrière-plan. On repart de l'icône originale
# avec son masque de transparence. On la cale au milieu de l'arrière-plan, 
# et on colle les deux. Le résultat est écrit sur le disque.
def paste_icon(bg, icon_path):
    icon = Image.open(icon_path)

    position = ((bg.width - icon.width) // 2, (bg.height - icon.height) // 2)
    bg.paste(icon, position, icon)
    bg.save("output.png")

def main():
    help = "icon-background.py -a <path_to_the_app>"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ha:") # Getopt pourrait être remplacé par argparse
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(help)
            sys.exit()
        elif opt == "-a":
            app_path = arg
            icon_path = extract_icon(app_path)
            color = get_color(icon_path)
            bg = create_bg(color)
            paste_icon(bg, icon_path)

if __name__ == '__main__':
    main()