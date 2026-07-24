"""\nperformance_monitor_20.py - NeuroShell Component\nGenerated on 2026-07-19\n"""\n\nclass ResourceTracker:
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
        return {'cpu': 0, 'memory': 0}\n\ndef profile_function(func):
        def wrapper(*args, **kwargs):
            import cProfile
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            pr.print_stats(sort='cumulative')
            return result
        return wrapper\n\ndef profile_function(func):
        def wrapper(*args, **kwargs):
            import cProfile
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            pr.print_stats(sort='cumulative')
            return result
        return wrapper\n\nclass ResourceTracker:
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