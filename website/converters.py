# converters.py
import re

class FileNameConverter:
    regex = r'^[a-zA-Z0-9._-]+$'

    def to_python(self, value):
        # Procesa el valor para eliminar caracteres no válidos
        return ''.join(c for c in value if self.regex.match(c))

    def to_url(self, value):
        return value
