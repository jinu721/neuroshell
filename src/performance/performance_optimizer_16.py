"""\nperformance_optimizer_16.py - NeuroShell Component\nGenerated on 2026-07-17\n"""\n\nclass CacheManager:
    def __init__(self, max_size=500):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
        
    def get(self, key):
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
        
    def put(self, key, value):
        if len(self.cache) >= self.max_size:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]
        self.cache[key] = value
        self.access_order.append(key)