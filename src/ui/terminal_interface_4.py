"""\nterminal_interface_4.py - NeuroShell Component\nGenerated on 2026-07-17\n"""\n\nclass InteractiveMenu:
    def __init__(self):
        self.options = []
        self.selected_index = 0
        
    def add_option(self, text, callback):
        self.options.append({'text': text, 'callback': callback})
        
    def show(self):
        for i, option in enumerate(self.options):
            marker = '>' if i == self.selected_index else ' '
            print(f"{marker} {option['text']}")