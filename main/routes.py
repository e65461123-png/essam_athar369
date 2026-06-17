
from . import main_bp

@main_bp.route('/')
def home():
    return "الموقع يعمل بنجاح وبأفضل هيكل برمجى!"
