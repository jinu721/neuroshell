"""\ncommand_utils_24.py - NeuroShell Component\nGenerated on 2026-07-08\n"""\n\ndef sanitize_input(user_input):
        """Sanitize user input for security"""
        dangerous_chars = ['|', '&', ';', '$', '`']
        for char in dangerous_chars:
            user_input = user_input.replace(char, '')
        return user_input.strip()\n\ndef sanitize_input(user_input):
        """Sanitize user input for security"""
        dangerous_chars = ['|', '&', ';', '$', '`']
        for char in dangerous_chars:
            user_input = user_input.replace(char, '')
        return user_input.strip()