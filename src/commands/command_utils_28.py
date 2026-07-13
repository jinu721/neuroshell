"""\ncommand_utils_28.py - NeuroShell Component\nGenerated on 2026-07-12\n"""\n\ndef measure_execution_time(func):
        """Decorator to measure command execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            return result, execution_time
        return wrapper\n\ndef validate_command_syntax(command):
        """Validate command syntax and structure"""
        if not command or len(command.strip()) == 0:
            return False
        return True\n\ndef measure_execution_time(func):
        """Decorator to measure command execution time"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            return result, execution_time
        return wrapper\n\ndef sanitize_input(user_input):
        """Sanitize user input for security"""
        dangerous_chars = ['|', '&', ';', '$', '`']
        for char in dangerous_chars:
            user_input = user_input.replace(char, '')
        return user_input.strip()\n\ndef validate_command_syntax(command):
        """Validate command syntax and structure"""
        if not command or len(command.strip()) == 0:
            return False
        return True\n\ndef sanitize_input(user_input):
        """Sanitize user input for security"""
        dangerous_chars = ['|', '&', ';', '$', '`']
        for char in dangerous_chars:
            user_input = user_input.replace(char, '')
        return user_input.strip()