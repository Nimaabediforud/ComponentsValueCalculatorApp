from .components import ResistorComponent

COMPONENTS = {
    "resistor": ResistorComponent(),
    # "capacitor": CapacitorComponent(),  # future
}

def get_component(name):
    return COMPONENTS.get(name.lower())

def get_component_names():
    return list(COMPONENTS.keys())
