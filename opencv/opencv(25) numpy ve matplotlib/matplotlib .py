import matplotlib.pyplot as plt
import numpy as  np

# veri görselleşitrme

# x =.arange(5) # 0 dan başlar 5 tane sayı verir
# # print(x)
# y = x
#
# plt.plot(x,y,"o--") # çemberli kesikli çizgi
# plt.plot(x,-y) # düz çizgi
# plt.plot(-x,y,"o") # sadece çember
#
# plt.title("y=x,y=-x")
#
# plt.show()

########################################
# N = 11
# x = np.linspace(0,10,N) #sıfırdan 11 e 10 tane sayı görmek istiyorum
#
# y = x
#
# plt.plot(x,y,"o--")
# plt.axis("off")
# plt.show()

# x = [1,2,3,4] #indexine göre değerleri grafikte gösterdi
# plt.plot(x,[y**2 for y in x])
# plt.show()

########################################

# x = np.arange(3)
#
# plt.plot(x,[y**2 for y in x])
# plt.plot(x,[y**3 for y in x])
# plt.plot(x, 2*x)
# plt.plot(x, 5.2*x)
#
# plt.legend(['x**2','x**3', 'x*2', 'x*5.2'], loc= 'lower right') # doğruların hangisi old kutucuğa yazar
#
# plt.grid(True) # ızgara koyar
#
# plt.xlabel('x = np.arange(3)') # eksenlere isimler veriyoruz
# plt.ylabel('y = f(x)')
#
# plt.axis([0,2,0,10]) # max ve min noktaları ayarlanıyor
# plt.title("simple plot")
#
# plt.show()
#############################################

# path = 'C:\\Users\\Asus\\Desktop\\artek\\coins.jpg'
# img = plt.imread(path)
#
# # plt.imshow(img)
# # plt.show()
#
# print(img); print("type: ",type(img)); print("shape: ", img.shape); print("ndim: ", img.ndim); print("size: ", img.size); print("dtype: ", img.dtype)
#
# print("red channel: ", img[50,50,0]) # rgb r=0
# print("green channel: ", img[50,50,1])
# print("blue channel: ", img[50,50,2])
#
# print("rgb channel value: ", img[50,50,:])

##############################################


