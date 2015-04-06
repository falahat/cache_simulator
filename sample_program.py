
from cache_simulator import Memory, Cache


# Address length
memory = Memory(32);

# size(bytes), N_way, bytes per entry, memory
cache = Cache(1024, 1, 16, memory)

lookup = cache.lookup # For convenience
write = cache.write

i = 0
j = 0
array = list()

step = 256
for j in range(step):
  for i in range(step - 1):

    addr_a_original = 4*(step*j)
    addr_b_original = 4*(step*j + i + 1)
    addr_c_original = addr_a_original

    a = lookup(addr_a_original , False, False, True)
    b = lookup(addr_b_original , False, False, True)
    c = write(addr_c_original  , a[0] + b[0], True)


    addr_a = bin(addr_a_original)
    addr_b = bin(addr_b_original)
    addr_c = bin(addr_c_original)

    print("i: " + str(i) + " j: " + str(j) + " -+-"*10)
    print("A address\t\tresponse\tB address\t\tresponse\tc response")
    print(addr_a + " : " + a[1] + "\t" + addr_b + " : " + b[1] + "\t" + c[1])
    addr_a = ""
    for el in list(cache.tokenize(addr_a_original)):
        if type(el) == type(1):
            el = bin(el)[2:]
        addr_a += "|" + str(el) +  "|" 
    print("A:  " + addr_a)
    addr_b = ""
    for el in list(cache.tokenize(addr_b_original)):
        if type(el) == type(1):
            el = bin(el)[2:]
        addr_b +=   "|" + str(el) + "|";
    print("B:  " + addr_b)


cache.dump_info()
  