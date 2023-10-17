import cv2

""" #-----Abrindo imagem na tela------- 

#lendo imagem
img = cv2.imread('farol.jpg') #armazenando na varial que guarda a imagem 
#Transformando a imagem em cinza
imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Mostrando imagens 
cv2.imshow('Imagem do Farol', img) #Nome da tela que vai exibir e variavel que vai abrir
cv2.imshow('Imagem Cinza', imgCinza) #Nome da tela que vai exibir e variavel que vai abrir
cv2.waitKey(0) # travar imagem
print(img.shape) #mostrar as dimensoes das cores imagem

 """

""" # --------reproduzir video-----------------

#Leitura do video 
video = cv2.VideoCapture('runners.mp4')

# Loop para mostrar o video 
while True:
     #Fazendo a leitura do video, deve ser com suas variavies
     check, vd = video.read()

     #Redimensionar os videos
     imgRedim = cv2.resize(vd,(640,420))
     cv2.imshow('video', imgRedim)
     cv2.waitKey(0)

 """



""" """ """ # ------ cortar imagem -------

#leitura da imagem
img = cv2.imread('farol.jpg')

#funcao para descobrir as dimensoes da area de recorte 
dimensao = cv2.selectROIs("Selecione a area da imagem", img, False)
print(dimensao)

#separando a variavel dimensao em um array 
v1 = int(dimensao[0])
v2 = int(dimensao[1])
v3 = int(dimensao[2])
v4 = int(dimensao[3])

#recorte pixels eixo x e eixo y 
recorte = img[v1:v2+v4, v1:v1+v3]
cv2.imshow('Imagem', img)
cv2.imshow('Recorte', recorte)
cv2.waitKey(0) 
 



 """ 
""" #----------Recortando utilizando outra ferramenta para descobrir os pixels --------------
img = cv2.imread('farol.jpg')

#recorte pixels eixo x e eixo y 
recorte = img[310:520, 120:420]
cv2.imshow('Imagem', img)
cv2.imshow('Recortado', recorte)

cv2.waitKey(0)

  """


""" 
""" """ #Abrir camera
camera = cv2.VideoCapture(0)
 #camera.set(3,640) #largura 
 #camera.set(4, 420) #altura
 #camera.set(10, 10) #brilho

while True: 
     check, img = camera.read()
     cv2.imshow('Web can', img)
     
     #leitura de teclado com a tecla q pressionada
     if cv2.waitKey(1) & 0xFF == ord('q'):
      break
 """
 

""" """ # ------ cortar imagem e salvar no diretorio -------

#leitura da imagem
print('oi')
img = cv2.imread('farol.jpg')

#funcao para descobrir as dimensoes da area de recorte 
dimensao = cv2.selectROIs("Selecione a area da imagem", img, False)
cv2.destroyWindow('Selecione a area da imagem')
print(dimensao)

#separando a variavel dimensao em um array 
v1 = int(dimensao[0])
v2 = int(dimensao[1])
v3 = int(dimensao[2])
v4 = int(dimensao[3])

#recorte pixels eixo x e eixo y 
recorte = img[v1:v2+v4, v1:v1+v3]

#criando o caminho que a imagem será salva
caminho = 'recortes/' # nome da pasta da qual será usada 
nome_arquivo = input('Digite o nome do arquivo ')

#salvando imagem
cv2.imwrite(f'{caminho}{nome_arquivo}.jpg', recorte)
print("Imagem salva com sucesso")

cv2.imshow('Imagem', img)
cv2.imshow('Recorte', recorte)
cv2.waitKey(0)

 
 
