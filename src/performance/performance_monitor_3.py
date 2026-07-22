"""\nperformance_monitor_3.py - NeuroShell Component\nGenerated on 2026-07-22\n"""\n\ndef profile_function(func):
        def wrapper(*args, **kwargs):
            import cProfile
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            pr.print_stats(sort='cumulative')
            return result
        return wrapper