from math import sqrt
from skimage import color
from skimage.feature import blob_dog
from skimage.color import rgb2gray
from skimage import io
from skimage.transform import rotate
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import random
import numpy as np
from skimage import transform as tf
import math
from skimage.transform import rescale, resize, downscale_local_mean
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from matplotlib.patches import ConnectionPatch
escalas=[25,50,100,200,400]

def Gauss(titulo,image):
    global blob
    image_gray = rgb2gray(image)
    blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=0.1)
    blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)
    fig,ax = plt.subplots(1)
    plt.title(titulo)
    ax.imshow(image)
    for blob in blobs_dog:
            y, x, r = blob
            c = plt.Circle((x, y), r, color="blue", linewidth=2, fill=False)
            ax.add_patch(c)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
    blob=blobs_dog
    return blobs_dog

def Porcentaje(matches,kporiginal):
    
    Porcentajes = []
    for a in range(0,len(matches)):
        prom=(matches[a]/len(kporiginal))*100
        Porcentajes.append(prom)
    return Porcentajes




def ImagenTransform():
    x=int(Ex.get())
    y=int(Ey.get())
    FinalkpOriginal = []
    FinalkpTransformada =[]
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.jpg*"),("all files","*.*")))
    ls=raiz.filename
    imgOriginal = io.imread(ls)
    imgCv=cv2.imread(ls,0)
    raiz.destroy()
    kpOrignalesTranformada = []
    imgCvMaker = cv2.copyMakeBorder(imgCv, int(y), int(y),int(x), int(x), cv2.BORDER_CONSTANT, value=None)
    img = cv2.copyMakeBorder(imgOriginal, int(y), int(y),int(x), int(x), cv2.BORDER_CONSTANT, value=None)
   
    #Nueva imagen Original
   
    kp=Gauss("Imagen Original",img)
    for a in range(0,len(kp)):
        nuevaY= kp[a][0]+y
        nuevaX =kp[a][1]+x
        kpOrignalesTranformada.append((nuevaY,nuevaX))
    tform = tf.AffineTransform(scale=(1, 1), rotation=0,
                                translation=(-x, -y))
    img3 = tf.warp(img, tform)
    rows,cols = imgCvMaker.shape
    M = np.float64([[1,0,x],[0,1,y]])
    dst = cv2.warpAffine(img,M,(cols,rows))
    kpTrans = Gauss("Desplazada",dst)
    FinalkpOriginal,FinalkpTransformada=MatchingDistancia(img,dst,kpTrans,kpOrignalesTranformada,kp)    
    
    #mostrar
    colors =["blue","orange","yellow","green","black","pink","purple","gray"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))
    ax1.imshow(img)
    ax2.imshow(img3)

    for o in range(0,len(kp)):
        d=plt.Circle((kp[o][1], kp[o][0]), 3 ,color="red", linewidth=1, fill=False)
        ax1.add_patch(d)

    for t in range(0,len(FinalkpTransformada)):
        c = plt.Circle((FinalkpTransformada[t][1], FinalkpTransformada[t][0]), 3, color="red", linewidth=1, fill=False)
        ax2.add_patch(c)

    for b in range(0,len(FinalkpTransformada)):
        xyB = (FinalkpOriginal[b][1],FinalkpOriginal[b][0])
        xy =  (FinalkpTransformada[b][1],FinalkpTransformada[b][0])
        coordsA = "data"
        coordsB = "data"
        con = ConnectionPatch(xyA=xy, xyB=xyB, coordsA=coordsA, coordsB=coordsB,
                            axesA=ax2, axesB=ax1,
                            arrowstyle="-", shrinkB=1 ,linewidth=2,color=colors[random.randint(0,7)])
        ax2.add_artist(con)
        
        
    plt.show()

def ImagenEscalada():
    FinalkpOriginal = []
    FinalkpTransformada =[]
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("png files","*.jpg*"),("all files","*.*")))
    ls=raiz.filename
    imgOriginal = cv2.imread(ls)
    raiz.destroy()
    kpOrignalesTranformada=[]
    
    kp=Gauss("Imagen Original",imgOriginal)
    for f in range(len(escalas)):
        kpOrignalesTranformada.clear()
        FinalkpOriginal.clear()
        FinalkpTransformada.clear()
        widht = int(imgOriginal.shape[1] * escalas[f]/100)
        height= int(imgOriginal.shape[0] * escalas[f]/100)
        dim =(widht,height)
        dst =cv2.resize(imgOriginal,dim, interpolation = cv2.INTER_AREA) 
        kpTrans =Gauss("Resized",dst)   
        for g in kp:
            nuevaY=0
            nuevaX=0
            nuevaY= (g[0]*escalas[f]/100)
            nuevaX =(g[1]*escalas[f]/100)
            kpOrignalesTranformada.append((nuevaY,nuevaX))
        
        FinalkpOriginal,FinalkpTransformada=MatchingDistancia(imgOriginal,dst,kpTrans,kpOrignalesTranformada,kp)
        
        colors =["blue","orange","yellow","green","black","pink","purple","gray"]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))
        ax1.imshow(imgOriginal)
        ax2.imshow(dst)

        for o in range(0,len(kp)):
            d=plt.Circle((kp[o][1], kp[o][0]), 3 ,color="red", linewidth=1, fill=False)
            ax1.add_patch(d)

        for t in range(0,len(kpTrans)):
            c = plt.Circle((kpTrans[t][1], kpTrans[t][0]), 3, color="red", linewidth=1, fill=False)
            ax2.add_patch(c)

        for b in range(0,len(FinalkpTransformada)):
            xyB = (FinalkpOriginal[b][1],FinalkpOriginal[b][0])
            xy =  (FinalkpTransformada[b][1],FinalkpTransformada[b][0])
            coordsA = "data"
            coordsB = "data"
            con = ConnectionPatch(xyA=xy, xyB=xyB, coordsA=coordsA, coordsB=coordsB,
                                axesA=ax2, axesB=ax1,
                                arrowstyle="-", shrinkB=1 ,linewidth=2,color=colors[random.randint(0,7)])
            ax2.add_artist(con)
        plt.show()
  
def rotated(origin,point, radians):
    x, y = point
    ox, oy = origin
    qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
    qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)
    return qx, qy
    

def ImagenRotada():
    FinalkpOriginal = []
    FinalkpTransformada =[]
    kpOrignalesTranformada=[]
    a=int(Entrada.get())
    raiz.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    ls=raiz.filename
    imgShow = io.imread(ls)
    img = cv2.imread(ls,0)
    raiz.destroy()
    rows,cols = img.shape[:2]
    
    nrow = int(pow(pow(cols,2)+ pow(rows,2),1/2))/2
    nrowRectangle =int(pow(pow(cols,2)+ pow(rows,2),1/2))/4
    #imgBorder = cv2.copyMakeBorder(img, int(nrow-(cols//2)), int(nrow-(rows//2)),int(nrow-(cols//2)), int(nrow-(rows//2)), cv2.BORDER_CONSTANT, value=None)
    imgBorder = cv2.copyMakeBorder(img, int(nrowRectangle), int(nrowRectangle),int(nrowRectangle), int(nrowRectangle), cv2.BORDER_CONSTANT, value=None)
   
    #imgShow2 = cv2.copyMakeBorder(imgShow, int(nrow-(cols//2)), int(nrow-(rows//2)),int(nrow-(cols//2)), int(nrow-(rows//2)), cv2.BORDER_CONSTANT, value=None)
    imgShow2 = cv2.copyMakeBorder(imgShow, int(nrowRectangle), int(nrowRectangle),int(nrowRectangle), int(nrowRectangle), cv2.BORDER_CONSTANT, value=None)
    
    xrow,ycol =imgBorder.shape[:2]
    kp = Gauss("Original",imgBorder)
    for j in range(360,0,-a):
        kpOrignalesTranformada.clear()
        FinalkpOriginal.clear()
        FinalkpTransformada.clear()
        imgrotada = rotate(imgBorder,j)
        RotadaShow = rotate(imgShow2,j)
        kpTrans = Gauss("rotada",imgrotada )
        origin=(ycol/2,xrow/2)
        for b in range(0,len(kp)):
            point =(kp[b][1] ,kp[b][0])
            nuevaX,nuevaY = rotated(origin, point, math.radians(j))
            nuevaR =kp[b][2]
            kpOrignalesTranformada.append((nuevaY,nuevaX,nuevaR))
        FinalkpOriginal,FinalkpTransformada=MatchingDistancia(imgBorder,imgrotada,kpTrans,kpOrignalesTranformada,kp)
        colors =["blue","orange","yellow","green","black","pink","purple","gray"]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 8))
        ax1.imshow(imgShow2)
        ax2.imshow(RotadaShow)

        for o in range(0,len(kp)):
            d=plt.Circle((kp[o][1], kp[o][0]), 3 ,color="red", linewidth=1, fill=False)
            ax1.add_patch(d)

        for t in range(0,len(kpTrans)):
            c = plt.Circle((kpTrans[t][1], kpTrans[t][0]), 3, color="red", linewidth=1, fill=False)
            ax2.add_patch(c)

        for b in range(0,len(FinalkpTransformada)):
            xyB = (FinalkpOriginal[b][1],FinalkpOriginal[b][0])
            xy =  (FinalkpTransformada[b][1],FinalkpTransformada[b][0])
            coordsA = "data"
            coordsB = "data"
            con = ConnectionPatch(xyA=xy, xyB=xyB, coordsA=coordsA, coordsB=coordsB,
                                axesA=ax2, axesB=ax1,
                                arrowstyle="-", shrinkB=1 ,linewidth=1,color=colors[random.randint(0,7)])
            ax2.add_artist(con)
        plt.show()



def MatchingDistancia(imgOriginal,ImgTransformada,kpTransformada,kpOriTransformada,kp):
    kp1=[]
    kp2=[]
    contador=0
    catch =[]
    try:
        for a in kpOriTransformada:
            for b in kpTransformada:
                result=pow(pow(b[0]-a[0],2)+pow(b[1]-a[1],2),1/2)
                if result<=2 and result>=-2:
                    kp1.append(kp[contador]) #referencia a Originales con OriTrans
                    kp2.append(b) #
                else:
                    catch.append("Error")
            contador=contador+1
    except:
        pass
    return kp1,kp2 #kp1 es la Original kp2 Transformada

        


raiz = Tk()
raiz.geometry('400x450')
raiz.configure(bg = 'white')
raiz.title('Imagenes metodo DoG')
e1=ttk.Label(raiz,text="Rotacion : ")
e1.pack(padx=5,pady=4,ipadx=5,ipady=5)
Entrada =ttk.Entry(raiz)
Entrada.pack(padx=5,pady=5,ipadx=5,ipady=5)
ttk.Button(raiz, text='   Imagen Rotada   ', command=ImagenRotada).pack(padx=5,pady=4,ipadx=5,ipady=5)
e2=ttk.Label(raiz,text="X : ")
e2.pack(padx=0,pady=4,ipadx=0,ipady=0)
Ex =ttk.Entry(raiz)
Ex.pack(padx=5,pady=4,ipadx=5,ipady=5)
e3=ttk.Label(raiz,text="Y : ")
e3.pack(padx=0,pady=4,ipadx=0,ipady=0)
Ey =ttk.Entry(raiz)
Ey.pack(padx=5,pady=4,ipadx=5,ipady=5)
ttk.Button(raiz, text='Imagen Transformada', command=ImagenTransform).pack(padx=5,pady=4,ipadx=5,ipady=5)
ttk.Button(raiz, text='  Imagen Escalada  ', command=ImagenEscalada).pack(padx=5,pady=4,ipadx=5,ipady=5)
raiz.mainloop()