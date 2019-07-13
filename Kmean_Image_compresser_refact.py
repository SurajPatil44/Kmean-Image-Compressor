# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:33:18 2019

@author: sdpatil
"""

import random
from PIL import Image
import numpy as np


class KmeanImageCompressor:
    '''Class used for Image Compression
    n = number of clusters
    MAX = number of max iterations
    USAGE:
    img = KmeanImageComressor('test_im_flower.jpeg',n=16)
    img.Compress()
    img.SaveImage("Saving.jpg")
    '''
    
    def __init__(self,path,n=64,MAX=300):
        self.path = path
        self.np_img = np.array(Image.open(path))
        self.n = n
        self.MAX = MAX
        self.cluster = {}
        self.new_cents = None
        self.old_cents = None
        self.counter = np.zeros((self.np_img.shape[0],self.np_img.shape[1]))
        
    def rgb2gray(self,rgb):
        return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])
    
    def createOrClearDict(self):
        for i in range(self.n):
            self.cluster[i] = []
            
    def getRandomCentroids(self):
        randomCentroid = []
        _shape = self.np_img.shape
        for i in range(self.n):
            randomCentroid.append(self.np_img[random.randint(0,_shape[0]-1),random.randint(0,_shape[0]-1)])
        return randomCentroid
    
    def getCentroids(self):
        newCentroids = []
        for key,val in self.cluster.items():
            if len(val) > 0:
                cen = np.array(val).sum(axis=0)
                cent = cen // len(val)
                newCentroids.append(cent.astype('uint8'))
            else:
                newCentroids.append(np.array([0,0,0]).astype('uint8'))
    
        return newCentroids
    
    def create_clust_dict(self,cents):
        self.createOrClearDict()
        
        for i in range(self.np_img.shape[0]):
            for j in range(self.np_img.shape[1]):
                _min,clust = self.find_cluster(self.np_img[i,j],cents)
                self.counter[i,j] = clust
                self.cluster[clust].append(self.np_img[i][j])
    
    def find_cluster(self,point,Cents):
        '''Main Kmeans Clustering Algorithm'''
        if point.size > 1:
            point = self.rgb2gray(point)
            Cents = self.rgb2gray(np.array(Cents))
            dists = np.sqrt(abs(point - Cents))
        elif point.size == 1:
            #print(point - Cents)
            dists = np.sqrt((point - Cents))
        #print(dists)
        clust = dists.argmin()
        _min = min(dists)
        
        return (_min,clust)
    
    def Run_iteration(self,it):
        self.new_cents = self.getCentroids()
            #print(new_cents)
        self.create_clust_dict(self.new_cents)
        
    def compare(self):
        comp_list = [a for a,b in zip(self.new_cents,self.old_cents)
                        if np.array_equal(a,b) ]
        
        if len(comp_list) == 64:
            return True
        else:
            return False
        
    def SaveImage(self,out_path):
        '''Method used for saving image'''
        self.compressed.save(out_path)
            
        
    def Compress(self):
        self.old_cents = self.getRandomCentroids()
        self.createOrClearDict()
        self.create_clust_dict(self.old_cents)
        for it in range(self.MAX):
            print(it)
            print(len(self.old_cents))
            self.Run_iteration(it)
            print(len(self.new_cents))
            if self.compare():
                break
            else:
                self.old_cents = self.new_cents
        count_image = np.zeros_like(self.np_img)
        ####creating a compressed image
        for i in range(self.np_img.shape[0]):
            for j in range(self.np_img.shape[1]):
                clust = self.counter[i,j].astype('int8')
                count_image[i,j] = self.new_cents[clust]
               
        im = Image.fromarray(count_image.astype(np.uint8)) # monochromatic image
        self.compressed = im.convert('RGB') # color image
        #self.comressed.show()
        

                

            