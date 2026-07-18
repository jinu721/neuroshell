"""\nui_themes_30.py - NeuroShell Component\nGenerated on 2026-07-17\n"""\n\ndef create_ascii_art_banner():
        return '''
    ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗ 
    ████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗
    ██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║
    ██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║
    ██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝
    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
        '''\n\ndef apply_syntax_highlighting(code_text):
        """Apply syntax highlighting to code"""
        keywords = ['def', 'class', 'if', 'else', 'for', 'while']
        for keyword in keywords:
            code_text = code_text.replace(
                keyword, f'\033[94m{keyword}\033[0m'
            )
        return code_text