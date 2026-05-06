import sys
from pathlib import Path

# Add project root to Python path (so Convertors can be imported)
root_dir = Path(__file__).parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from Convertors.utils.Convertors import Resistor

class ResistorComponent:
    def run(self, subtype: str, value: str):
        band, result = Resistor().Run(type=subtype, value=value, stat=False)
        return band, result

