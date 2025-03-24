# -*- coding: utf-8 -*-
"""
Created on Fri May 19 14:07:30 2023

@author: LILARI
"""
from PIL import Image
reine = Image.open("camilla.jpg")
largeur=reine.width
hauteur=reine.height
largeur_x=reine.width//2
hauteur_y=reine.height//2
for y in range(hauteur_y):
    for x in range(largeur_x):
        r,v,b=reine.getpixel((x,y))
        if -1<r<90 and -1<v<175 and 24<b<260:
            n_r=b
            n_v=b
            n_b=r
            reine.putpixel((x,y),(n_r,n_v,n_b))

    for x in range(largeur):
        r,v,b=reine.getpixel((x,y))
        if -1<r<90 and -1<v<175 and 24<b<260:
            n_r=b
            n_v=b
            n_b=b
            reine.putpixel((x,y),(n_r,n_v,n_b))

for y in range(hauteur):
    for x in range(largeur_x):
        r,v,b=reine.getpixel((x,y))
        if -1<r<90 and -1<v<175 and 24<b<260:
            n_r=b
            n_v=v
            n_b=b
            reine.putpixel((x,y),(n_r,n_v,n_b))

    for x in range(largeur):
        r,v,b=reine.getpixel((x,y))
        if -1<r<90 and -1<v<175 and 24<b<260:
            n_r=b
            n_v=r
            n_b=r
            reine.putpixel((x,y),(n_r,n_v,n_b))
   
            
reine.show()