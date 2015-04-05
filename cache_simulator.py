
class Cache(Object):
	def __init__(cache_size, N_way, bytes_per_entry):

		# Given
		self.cache_size = cache_size
		self.N_way = N_way
		self.bytes_per_entry = bytes_per_entry

		# Calculating Sizes
		self.num_entries = cache_size / bytes_per_entry
		self.num_sets = num_entries / N_way
		self.num_ways = self.num_entries / self.num_sets


		self.sets = map(); # {Set Index => Cache Blocks} but in a set object
