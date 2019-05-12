from parse import parse_archive, checkComing
from db import *
# from multiprocessing.dummy import Pool as ThreadPool

good_ids = []
bad_ids = []

# threads = 100
#
# pool = ThreadPool(threads)
#
# task = []

def funct(i):
    print('Cheking id= ' +str(i))
    if getGameData(i) != []:
        try:
            if parse_archive(i):
               print('id ' + str(i) + ' is good')
            else:
               print('id ' + str(i) + ' is bad')
        except:
            print('ERROR ' + str(i))

# task = [x for x in range(230, 400)]
#
# results = pool.map(funct, task)
#
# pool.close()
# pool.join()
# print(results)

for i in range(194,346):
    funct(i)

