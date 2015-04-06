import math;


class LookupResponse(object): #TODO: Make these some non-colliding hashes maybe?
	found = "found"
	not_found_overrode = "not found and overrode an existing entry"
	not_found_no_overrode = "not found and did not override an existing entry"


class Memory(object):

	DEFAULT_VALUE = 0;

	def __init__(self, address_length=32):
		self.address_length = address_length;
		self.mem = map() # {32 bit address => value}

	def _enumerate_bits(num_bits):

		if num_bits == 0:
			return [];

		last_num = 0;
		for i in range(num_bits):
			last_num += (1 << i)
		last_num += 1;
		num = 0;

		ans = list();
		while (num != last_num):
			ans.append(bin(num));
			num += 1
		return ans;


	def lookup_one(self, address, block_offset):

		if address not in self.mem:
			self.mem[address] = DEFAULT_VALUE;

		return self.mem[address]

	def lookup(self, address, block_offset):
		address = address[0: (29 - block_offset)] # Word addressed
		addresses = [address + str(snippet) + "00" for snippet in Memory._enumerate_bits(block_offset)]
		ans = [lookup_one(addr) for addr in addresses]
		return ans;
	

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

		# Address segment sizes
		self.set_index_size = math.log2(self.entries_per_set)
		self.block_offset = math.log2(self.blocks_per_entry)

		self.sets = map(); # {Set Index => Set Objects}

		# Used to track misses. Keeps track of tags.
		
		# Keeps track of all entries overriden because of conflict misses
		self.overriden_conflict = set()

		# Keeps track of all entries overriden because of capacity misses
		self.overriden_capacity = set()

		self.bytes_written = 0;

		self.num_misses = 0;
		self.compulsory_misses = list();
		self.conflict_misses = list();
		self.capacity_misses = list();

	def is_full(self):
		# TODO: Does this work?
		return self.bytes_written >= self.cache_size;

	def lookup(self, address):
		start = 0
		end = self.address_length

		address = address[start : end] # Byte offset

		start = (end - self.block_offset) + 1
		end = end 
		block_offset = address[start:end];

		end = start - 1
		start = (end - self.set_index_size) + 1
		set_addr = address[start:end];

		end = start - 1
		start = 0
		tag = address[start:end];

		print("Divided: " + tag + " | " + set_addr + " | " + block_offset + " | 00 ")


		if set_addr not in self.sets:
			self.sets[set_addr] = CacheSet(self, set_addr)

		(val, response, old_tag) = self.sets[set_addr].lookup(tag, block_offset)

		if response != LookupResponse.found:
			
			num_misses += 1;
			self.bytes_written += self.bytes_per_entry

			if old_tag in self.overriden_conflict: 
				self.conflict_misses.append(old_tag);

			if old_tag in self.overriden_capacity: 
				self.capacity_misses.append(old_tag);

			if response == LookupResponse.not_found_overrode:
				# We overrode something. Capacity miss or conflict miss
				# It's capacity miss iff we were full
				if self.is_full():
					self.capacity_misses.append(old_tag)
				else:
					self.conflict_misses.append(old_tag)

				self.bytes_written -= self.bytes_per_entry

		return val;


class CacheSet(object):

	def __init__(self, cache, set_index):
		self.index_size = cache.set_index_size;
		self.num_ways = cache.num_ways;
		self.index = set_index;


		# Contains CacheEntry objects. len = num_ways
		# Initially all invalid
		self.entries = [CacheEntry(0) for i in range(self.num_ways)] 


	"""
	Returns (Value, Lookup Response)
	"""
	def lookup(self, tag, block_offset):
		ans = False;

		for entry in self.entries:
			entry.age += 1
			if entry.tag == tag and entry.valid :
				ans = entry.lookup(block_offset);

		if not ans:
			# We have not found it, time to replace the least recently used one
			ans = self.ask_memory(self.index, tag, block_offset)

		# Make the entry young again
		# TODO: What if Null? Should be impossible...
		ans[0].age = 0;
		return ans;


	def oldest_entry(self):
		ans = (0, False);
		for entry in self.entries:
			if entry.age <= ans[0]:
				ans = (entry.age, entry)
		return ans[1];

	def ask_memory(self, set_index, tag, block_offset):
		query = str(tag) + str(set_index) + str(block_offset) + "00"

		# vals for that entry. len should be blocks_per_entry
		values = self.cache.memory.lookup(query, block_offset) 

		to_change = self.oldest_entry();
		old_tag = to_change.tag;
		to_change.blocks = values;
		to_change.tag = tag;
		to_change.age = 0;

		response = LookupResponse.not_found_overrode
		if not to_change.valid:
			to_change.valid = True
			response = LookupResponse.not_found_no_overrode

		val = to_change.lookup(block_offset)[0]
		return (val, response, old_tag);



class CacheEntry(object):

	def __init__(self, tag, cache):
		self.cache = cache;
		self.tag = tag;
		self.blocks = [0 for i in range(cache.blocks_per_entry)] # Will contain values
		self.valid = False;

		self.age = 0; # If age is 0, it's just been used.

	def lookup(self, block_offset):
		# if self.tag != self.block_offset:
		# 	return (False, LookupResponse.not_found_overrode);
		# 	# Now gotta pull the info?

		if self.blocks[block_offset]:
			return (self.blocks[block_offset], LookupResponse.found, False);
		else:
			print("SOMETHING WRONG");
			return False; # TODO: Better things later? Also will this ever even happen?

