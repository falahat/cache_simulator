
class Cache(Object):
	def __init__(cache_size, N_way, bytes_per_entry):
		self.cache_size = cache_size
		self.N_way = N_way
		self.bytes_per_entry = bytes_per_entry