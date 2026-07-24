"""\nperformance_monitor_23.py - NeuroShell Component\nGenerated on 2026-07-20\n"""\n\nclass PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
        
    def start_timing(self, operation):
        self.start_times[operation] = time.time()
        
    def end_timing(self, operation):
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            if operation not in self.metrics:
                self.metrics[operation] = []
            self.metrics[operation].append(duration)
            del self.start_times[operation]
            return duration
        return 0\n\nclass ResourceTracker:
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        
    def track_resources(self):
        import psutil
        self.cpu_usage.append(psutil.cpu_percent())
        self.memory_usage.append(psutil.virtual_memory().percent)
        
    def get_average_usage(self):
        if self.cpu_usage and self.memory_usage:
            return {
                'cpu': sum(self.cpu_usage) / len(self.cpu_usage),
                'memory': sum(self.memory_usage) / len(self.memory_usage)
            }
        return {'cpu': 0, 'memory': 0}\n\nclass PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
        
    def start_timing(self, operation):
        self.start_times[operation] = time.time()
        
    def end_timing(self, operation):
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            if operation not in self.metrics:
                self.metrics[operation] = []
            self.metrics[operation].append(duration)
            del self.start_times[operation]
            return duration
        return 0\n\nclass ResourceTracker:
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        
    def track_resources(self):
        import psutil
        self.cpu_usage.append(psutil.cpu_percent())
        self.memory_usage.append(psutil.virtual_memory().percent)
        
    def get_average_usage(self):
        if self.cpu_usage and self.memory_usage:
            return {
                'cpu': sum(self.cpu_usage) / len(self.cpu_usage),
                'memory': sum(self.memory_usage) / len(self.memory_usage)
            }
        return {'cpu': 0, 'memory': 0}\n\nclass ResourceTracker:
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        
    def track_resources(self):
        import psutil
        self.cpu_usage.append(psutil.cpu_percent())
        self.memory_usage.append(psutil.virtual_memory().percent)
        
    def get_average_usage(self):
        if self.cpu_usage and self.memory_usage:
            return {
                'cpu': sum(self.cpu_usage) / len(self.cpu_usage),
                'memory': sum(self.memory_usage) / len(self.memory_usage)
            }
        return {'cpu': 0, 'memory': 0}