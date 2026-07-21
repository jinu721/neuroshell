"""\nperformance_monitor_25.py - NeuroShell Component\nGenerated on 2026-07-18\n"""\n\ndef profile_function(func):
        def wrapper(*args, **kwargs):
            import cProfile
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            pr.print_stats(sort='cumulative')
            return result
        return wrapper\n\nclass PerformanceMonitor:
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
        return 0