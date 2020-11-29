from random import randint
from time import sleep
print('-=-'*20)
print ('VOU PENSAR EM UM NUMERO. TENTE ADIVINHA.......')
pc = randint(0,5)
print ('-=-'*20)
vc = int(input('Digite um numero de 0 a 5: '))
print ('PROCESSANDO......')
sleep(2)
print ('VOCÊ GANHOU!!!' if vc == pc else 'VOCÊ PERDEU!! você escolheu {} e eu {} HUAHAUHAUH....'.format(vc,pc))

#FUNCIONA NA FORMA DE BAIXO MAS FAZER DE UMA FORMA MELHORADA.
#import random
#n = int(input('Digite um numero de 0 a 5: '))
#l = (1,2,3,4,5)
#g = random.choice(l)
#print ('Você ganhou!!!' if n == g else 'Você perdeu, tente novamente!')
#print ('Número você escolheu foi {} e PC {}.'.format(n,g))