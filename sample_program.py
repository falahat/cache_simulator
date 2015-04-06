
from cache_simulator import Memory, Cache


# Address length
memory = Memory(32);

# size(bytes), N_way, bytes per entry, memory
cache = Cache(4*1024, 1, 4, memory)

lookup = cache.lookup # For convenience
cache.lookup(0)

