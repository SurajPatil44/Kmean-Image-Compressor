# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:07:38 2019

@author: sdpatil
"""

#!/usr/bin/env python
# coding: utf-8

import random
from PIL import Image
import numpy as np
import sys

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


def getRandomCentroids(data,n):
    randomCentroid = []
    _shape = data.shape
    for i in range(n):
        randomCentroid.append(data[random.randint(0,_shape[0]-1),random.randint(0,_shape[0]-1)])
    return randomCentroid

def find_cluster(point,Cents):
    if point.size > 1:
        point = rgb2gray(point)
        Cents = rgb2gray(np.array(Cents))
        dists = np.sqrt(abs(point - Cents))
    elif point.size == 1:
        #print(point - Cents)
        dists = np.sqrt((point - Cents))
    #print(dists)
    clust = dists.argmin()
    _min = min(dists)
    
    return (_min,clust)

def getCentroids(cluster):
    newCentroids = []
    for key,val in cluster.items():
        if len(val) > 0:
            cen = np.array(val).sum(axis=0)
            cent = cen // len(val)
            newCentroids.append(cent.astype('uint8'))
        else:
            newCentroids.append(np.array([0,0,0]).astype('uint8'))

    return newCentroids

def create_clust_dict(cents,n):
    Clusters = {}
    for i in range(n):
        Clusters[i] = []

    counter = np.zeros((np_img.shape[0],np_img.shape[1]))
    for i in range(np_img.shape[0]):
        for j in range(np_img.shape[1]):
            _min,clust = find_cluster(np_img[i,j],cents)
            counter[i,j] = clust
            Clusters[clust].append(np_img[i][j])
    return counter,Clusters

def Run_iteration(cluster,it):
    new_cents = getCentroids(cluster)
        #print(new_cents)
    counter,Clusters = create_clust_dict(new_cents)
    return counter,Clusters,new_cents


def main(path):
    img = Image.open(path)
    np_img = np.array(img)
    n =64
    Cents = getRandomCentroids(np_img,n)
    MAX = 300
    Cluster = {}
    for i in range(n):
        Cluster[i] = []
    _,Cluster = create_clust_dict(Cents,n)
    old_cents = Cents
    for it in range(MAX):
        print(it)
        counter,Cluster,new_cents= Run_iteration(Cluster,it)
        if new_cents == old_cents:
            break
        else:
            old_cents = new_cents
            
    count_image = np.zeros_like(np_img)
    for i in range(np_img.shape[0]):
        for j in range(np_img.shape[1]):
            clust = counter[i,j].astype('int8')
            count_image[i,j] = Cents[clust]
           
    im = Image.fromarray(count_image.astype(np.uint8)) # monochromatic image
    imrgb = im.convert('RGB') # color image
    imrgb.show()
    
path = sys.argv[1]   

main(path) 
        




