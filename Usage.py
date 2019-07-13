from Kmean_Image_compresser_refact import KmeanImageCompressor

path = r'./data/test_im_flower.jpeg'

img = KmeanImageCompressor(path,n=32)
img.Compress()
img.SaveImage(r'./data/flower_32.jpg')
