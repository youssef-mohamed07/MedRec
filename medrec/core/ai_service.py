import os
from pathlib import Path

def infer(image_path: str) -> dict:
    """Placeholder AI inference function.

    Replace this with a call to your model or external AI service.
    It should return a dict with keys like `name`, `confidence`, `description`.
    """
    name = Path(image_path).name
    # Dummy response: in real life call model or API here
    return {
        'predicted_name': 'example-medicine',
        'confidence': 0.75,
        'description': f'Dummy detection for file {name}. Replace with real model output.'
    }
