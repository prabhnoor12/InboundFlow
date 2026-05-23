# Simple in-memory cache controller to manage cache buildup
from collections import OrderedDict
from threading import Lock

class CacheController:
	def __init__(self, max_size=1000):
		self.cache = OrderedDict()
		self.max_size = max_size
		self.lock = Lock()

	def get(self, key):
		with self.lock:
			if key in self.cache:
				# Move to end to mark as recently used
				self.cache.move_to_end(key)
				return self.cache[key]
			return None

	def set(self, key, value):
		with self.lock:
			if key in self.cache:
				self.cache.move_to_end(key)
			self.cache[key] = value
			if len(self.cache) > self.max_size:
				# Remove least recently used item
				self.cache.popitem(last=False)

	def clear(self):
		with self.lock:
			self.cache.clear()
