"""
Command Processor
Handles command execution and neural integration
"""

import subprocess
from typing import Dict, Any

class CommandProcessor:
    def __init__(self):
        self.execution_count = 0
    
    def execute(self, command: str, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """Execute command with neural assistance"""
        self.execution_count += 1
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'prediction_used': prediction
            }
        
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'prediction_used': prediction
            }
