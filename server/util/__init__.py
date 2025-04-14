import json
import os
                
with open(os.path.join(os.path.dirname(__file__), 'squares.json'), 'r') as f:
    content = f.read()

squares = json.loads(content)
