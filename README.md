# This Cache Simulator Is Terrible
It's honestly incredibly buggy

## Features & Warnings
Evicts based on LRU. It's also a write-back cache (though that doesn't make a performace difference here.)
It assumes that all requests are byte addressed, but it does everything word addressed. The first thing that it does to a requested address is chop off the rightmost two bits. So requesting 0b0...001 or 0b0...010 end up being the same request.

## Definition of Different Misses
This cache simulator keeps track of all entries that we have ever evicted and keeps track of why we evicted them. If we kicked out an entry but the cache was not full, then we know that this entry was kicked out only because of a set conflict. If we kicked an entry out and the cache was full at the time, we say that this entry was kicked out because there was just no room in the cache.
I'm 15% sure I'm correct, but this is how the program computes it:

* Compulsory Miss: If we've never asked for this address before, it's a compulsory miss
* Conflict Miss: If we asked for this at some point in the past and kicked it out because of some sort of set conflict. Remember that we keep track of whether or not we've asked for this value before, and why we had it then and we don't have it now.
* Capacity Miss: We used to have this data in the cache, but we evicted it at some point because our cache was full and we had to bring in new data.

Keep in mind that when we evict a value, we keep track of why we evicted it, but we don't count it that particular type of miss until we ask for that value again AFTER evicting it.
