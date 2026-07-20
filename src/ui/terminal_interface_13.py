"""\nterminal_interface_13.py - NeuroShell Component\nGenerated on 2026-07-20\n"""\n\nclass ProgressIndicator:
    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.current_step = 0
        
    def update(self, step):
        self.current_step = step
        percentage = (step / self.total_steps) * 100
        bar_length = 50
        filled_length = int(bar_length * step // self.total_steps)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f'\r|{bar}| {percentage:.1f}%', end='')\n\nclass InteractiveMenu:
    def __init__(self):
        self.options = []
        self.selected_index = 0
        
    def add_option(self, text, callback):
        self.options.append({'text': text, 'callback': callback})
        
    def show(self):
        for i, option in enumerate(self.options):
            marker = '>' if i == self.selected_index else ' '
            print(f"{marker} {option['text']}")\n\nclass InteractiveMenu:
    def __init__(self):
        self.options = []
        self.selected_index = 0
        
    def add_option(self, text, callback):
        self.options.append({'text': text, 'callback': callback})
        
    def show(self):
        for i, option in enumerate(self.options):
            marker = '>' if i == self.selected_index else ' '
            print(f"{marker} {option['text']}")