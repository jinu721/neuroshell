"""\nui_themes_9.py - NeuroShell Component\nGenerated on 2026-07-16\n"""\n\ndef apply_syntax_highlighting(code_text):
        """Apply syntax highlighting to code"""
        keywords = ['def', 'class', 'if', 'else', 'for', 'while']
        for keyword in keywords:
            code_text = code_text.replace(
                keyword, f'\033[94m{keyword}\033[0m'
            )
        return code_text\n\ndef apply_syntax_highlighting(code_text):
        """Apply syntax highlighting to code"""
        keywords = ['def', 'class', 'if', 'else', 'for', 'while']
        for keyword in keywords:
            code_text = code_text.replace(
                keyword, f'\033[94m{keyword}\033[0m'
            )
        return code_text