import numpy as np

# x = np.array([1,2,3],np.int16)
# print(x)
# print(type(x))
#
# print(x[0]); print(x[1]); print(x[2])
#
# print(x[-1]) # tersten başlar yani 3 yazar
#
# print(x[3]) #error böyle bi eleman yok

###########################################
#2 boyutlu dizi yani matris

# x = np.array([[1,2,3],[4,5,6]],np.int16)
# print(x)
# print("-------")
# print(x[0]) # matrisin ilk elemanı yani ilk satırı veriyor
# print(x[0,0]) # ilkin ilkini almayı sağlıyor
# print("-------")
# print(x[1]);print(x[1,0]);print(x[1,1]);print(x[1,2])

#print(x[:,0]);print(x[:,1]);print(x[:,2]) # : tümünü tarıyor

############################################
# 3 boyutlu diziler

# x = np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]],np.int16) # 2 tane 2 boyutlu dizi art arda gelince derinlik kazanır ve 3 boyutlu olur
# print(x)
#
# print(x[0,0,0]) # 1
# print(x[0,1,0]) # 4
# print(x[1,1,1]) # 11

############################################
# ndarray
# x = np.array([[-2,-1,0,5],[9,4,5,-7]],np.int8)
# print(x)
#
# print(x.shape) # kaç satır kaç sütun onu veriyor
# print(x.ndim) # kaç boyutlu old veriyor
#
# print(x.dtype)
#
# print(x.size) #eleman sayısını veriyor
#
# print(x.T) #transpozunu veriyor

###########################################

x = np.empty([3,3], np.uint8) # boş bir dizi oluşturur, içini ratsgele doldurur
print(x)
print("---------------")

y = np.full([3,3,3],dtype=np.int16, fill_value = 10)
print(y)
print("---------------")

z = np.ones((2,5,5), dtype = np.int8) #3 boyutlu
print(z)
print("---------------")

j = np.zeros((2,3,3), dtype = np.int8) # 2 tane 3 e 3 lük matris verir bunları arka arkaya koyduğunda ise 3 boyutlu olmuş olur
print(j) #0 siyah

