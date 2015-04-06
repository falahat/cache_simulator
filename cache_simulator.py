import math;


class LookupResponse(object):
	found = "found"
	not_found_overrode = "not found and overrode an existing entry"
	not_found_no_overrode = "not found and did not override an existing entry"

class Memory(object):

	DEFAULT_VALUE = 0;

	def __init__(self):
		self.mem = map() # {32 bit address => value}

	def lookup(self, address, byte_offset):

		if address in self.mem:
			return self.mem[address]
		else:
			self.mem[address] = DEFAULT_VALUE;

	def write(self, address, val):
		self.mem[address] = val;

class Cache(object):
	def __init__(self, cache_size, N_way, bytes_per_entry, memory):

		# Given
		self.memory = memory;
		self.cache_size = cache_size
		self.N_way = N_way
		self.bytes_per_entry = bytes_per_entry

		# Calculating Sizes
		self.num_entries = cache_size / bytes_per_entry # Entries total
		self.num_sets = num_entries / N_way
		self.num_ways = self.num_entries / self.num_sets
		self.entries_per_set = self.num_entries / self.num_sets;
		self.set_index_size = math.log2(self.entries_per_set)

		self.sets = map(); # {Set Index => Set Objects}


class CacheSet(object):

	def __init__(self, cache, set_index):
		self.index_size = cache.set_index_size;
		self.num_ways = cache.num_ways;
		self.index = set_index;


		# Contains CacheEntry objects. len = num_ways
		# entries[0] is oldest used, entries[len(entries) - 1] is most recently used
		self.entries = list() 


	"""
	Returns (Value, Lookup Response)
	"""
	def lookup(self, tag, block_offset):
		ans = False;
		for entry in self.entries:
			if entry.tag == tag:
				ans = entry.lookup(block_offset);
				return ans;

		if not ans:
			# We have not found it, time to replace the least recently used one
			ans = self.ask_memory(self.index, tag, block_offset)

		# Move the tag to index zero


	def ask_memory(self, set_index, tag, block_offset):
		query = str(tag) + str(set_index) + str(block_offset) + "00"
		value = self.cache.memory



class CacheEntry(object):

	def __init__(self, tag, cache):
		self.cache = cache;
		self.tag = tag;
		self.blocks = [0 for i in range(cache.blocks_per_entry)] # Will contain values
		self.valid = False;

	def lookup(self, block_offset):
		# if self.tag != self.block_offset:
		# 	return (False, LookupResponse.not_found_overrode);
		# 	# Now gotta pull the info?

		if self.blocks[block_offset]:
			return (self.blocks[block_offset], LookupResponse.found);
		else:
			print("SOMETHING WRONG");
			return False; # TODO: Better things later? Also will this ever even happen?
