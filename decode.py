import os
import subprocess
import PIL
from PIL import Image


def getheight(str):
    for i in range(len(str)):
        if str[i] == 'x':break
    for j in range(len(str)):
        if str[j] == '_':break
    return str[i+1:j]    
            
    
def getwidth(str):
        for i in range(len(str)):
            if str[i] == 'x':
                return str[0:i]

compressed_imgs_path = 'compressed_imgs/'

#读取图像目录
fileName = os.listdir('compressed_imgs')
for file in fileName:
    if file[-3:] != 'bin':
        fileName.remove(file)



#批量解压，转png
if not os.path.exists('rec'): os.mkdir('rec')
for img in fileName:
    #解码
    subprocess.call("""
                    ./decode \
                    -b %s%s     \
                    -o %s.yuv
                    """% (compressed_imgs_path,img,img[:-4]),
                    shell=True)
    #yuv444转png
    subprocess.call("""
                    ffmpeg -s %dx%d \
                    -pix_fmt yuv444p \
                    -i %s.yuv \
                    -frames:v 1 ./rec/%s.png -y
                    """%(int(getwidth(img)),int(getheight(img)),img[:-4],img[:-4]),
                    shell=True)
    subprocess.call("rm -f %s.yuv" % img[:-4],shell=True)