
from cache_simulator import Memory, Cache


# Address length
memory = Memory(32);

# size(bytes), N_way, bytes per entry, memory
cache = Cache(4*1024, 1, 4, memory)

lookup = cache.lookup # For convenience
write = cache.write

i = 0
j = 0
array = list()

for i in range(255):
  for j in range(256):

  	addr_a = 256*j
  	addr_b = 256*j + i + 1
  	addr_c = addr_a

  	a = lookup(addr_a , False, False, True)
  	b = lookup(addr_b , False, False, True)
  	c = write(256*j, a[0] + b[0], True)


  	addr_a = bin(addr_a)
  	addr_b = bin(addr_b)
  	addr_c = bin(addr_c)

  	print("i: " + str(i) + " j: " + str(j) + "-+-"*10)
  	print("a/b/c \t | address \t\t response")
  	print("A |\t" + addr_a + "\t" + a[1])
  	print("B |\t" + addr_b + "\t" + b[1])
  	print("C |\t" + addr_c + "\t" + c[1])


  