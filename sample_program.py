
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

step = 32
for j in range(step):
  for i in range(step):

    addr_a_original = 4*(step*j)
    addr_b_original = 4*(step*j)
    addr_c_original = addr_a_original

    a = lookup(addr_a_original)
    b = lookup(addr_b_original)
    c = write(addr_c_original, a + b)


cache.dump_info()
  