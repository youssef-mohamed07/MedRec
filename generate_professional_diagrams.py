"""
Professional Diagram Generator for MedRec System
Generates high-quality ERD, EERD, and System Architecture diagrams
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon, Wedge
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
import numpy as np
import os

# Create output directory
output_dir = 'diagrams'
os.makedirs(output_dir, exist_ok=True)

# Professional color palette
COLORS = {
    'primary': '#2563EB',      # Blue
    'secondary': '#7C3AED',    # Purple
    'success': '#10B981',      # Green
    'warning': '#F59E0B',      # Amber
    'danger': '#EF4444',       # Red
    'info': '#6B7280',         # Gray
    'user': '#EC4899',         # Pink
    'medicine': '#14B8A6',     # Teal
    'upload': '#8B5CF6',       # Violet
    'dark': '#1F2937',         # Dark Gray
    'light': '#F9FAFB',        # Very Light Gray
}

def add_shadow(ax, patch, offset=0.15):
    """Add drop shadow to a patch"""
    from matplotlib.transforms import offset_copy
    shadow = type(patch)(
        (patch.get_x() + offset, patch.get_y() - offset),
        patch.get_width(), patch.get_height(),
        **{k: v for k, v in patch.properties().items() if k in ['boxstyle']}
    )
    shadow.set_facecolor('black')
    shadow.set_edgecolor('none')
    shadow.set_alpha(0.15)
    shadow.set_zorder(patch.get_zorder() - 1)
    ax.add_patch(shadow)

def create_modern_card(ax, x, y, width, height, title, color, emoji=''):
    """Create a modern card design"""
    # Shadow
    shadow = FancyBboxPatch((x + 0.1, y - 0.1), width, height,
                           boxstyle="round,pad=0.1",
                           facecolor='black', edgecolor='none',
                           alpha=0.1, zorder=1)
    ax.add_patch(shadow)
    
    # Main card
    card = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.1",
                         facecolor='white', edgecolor=color,
                         linewidth=3, zorder=2)
    ax.add_patch(card)
    
    # Header
    header = Rectangle((x + 0.15, y + height - 0.5), width - 0.3, 0.4,
                      facecolor=color, edgecolor='none',
                      alpha=0.95, zorder=3)
    ax.add_patch(header)
    
    # Title
    title_text = f'{emoji} {title}' if emoji else title
    ax.text(x + width/2, y + height - 0.3, title_text,
           fontsize=14, fontweight='bold', ha='center', va='center',
           color='white', zorder=4)
    
    return y + height - 0.7  # Return starting y position for content

# =============================================================================
# ERD - Entity Relationship Diagram
# =============================================================================
def create_erd():
    print("Creating professional ERD...")
    fig = plt.figure(figsize=(18, 12), facecolor='white', dpi=150)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_facecolor('#F8F9FA')
    
    # Title with gradient effect
    title = ax.text(9, 11.2, 'Entity Relationship Diagram',
                   fontsize=32, fontweight='bold', ha='center',
                   color=COLORS['dark'])
    title.set_path_effects([path_effects.withStroke(linewidth=4, foreground='white')])
    
    ax.text(9, 10.6, 'MedRec - Medicine Recognition System Database Schema',
           fontsize=14, ha='center', color=COLORS['info'], style='italic')
    
    # USER ENTITY
    user_y = create_modern_card(ax, 0.5, 5, 5.5, 4.5, 'USER', COLORS['user'], '👤')
    
    user_fields = [
        ('🔑', 'id', 'Integer', 'PK', COLORS['warning']),
        ('👤', 'username', 'String', 'Unique', COLORS['success']),
        ('📧', 'email', 'String', 'Unique', COLORS['success']),
        ('🔒', 'password', 'String', '', None),
        ('📝', 'first_name', 'String', '', None),
        ('📝', 'last_name', 'String', '', None),
        ('📅', 'date_joined', 'DateTime', '', None),
        ('⏰', 'last_login', 'DateTime', '', None),
        ('✅', 'is_active', 'Boolean', '', None),
        ('⚙️', 'is_staff', 'Boolean', '', None),
        ('👑', 'is_superuser', 'Boolean', '', None),
    ]
    
    for i, (emoji, field, ftype, badge, badge_color) in enumerate(user_fields):
        y = user_y - i * 0.35
        ax.text(0.8, y, emoji, fontsize=11, va='center')
        ax.text(1.3, y, field, fontsize=10, fontweight='600',
               va='center', color=COLORS['dark'])
        ax.text(3.2, y, ftype, fontsize=9, va='center',
               color=COLORS['info'], style='italic')
        if badge:
            badge_box = FancyBboxPatch((4.8, y - 0.12), 0.6, 0.24,
                                      boxstyle="round,pad=0.02",
                                      facecolor=badge_color, edgecolor='none')
            ax.add_patch(badge_box)
            ax.text(5.1, y, badge, fontsize=7, fontweight='bold',
                   ha='center', va='center', color='white')
    
    # MEDICINE ENTITY
    med_y = create_modern_card(ax, 12, 5, 5.5, 4.5, 'MEDICINE', COLORS['medicine'], '💊')
    
    med_fields = [
        ('🔑', 'id', 'Integer', 'PK', COLORS['warning']),
        ('🏷️', 'code', 'String', 'Unique', COLORS['success']),
        ('🇸🇦', 'name_ar', 'String', '', None),
        ('🇬🇧', 'name_en', 'String', '', None),
        ('🔬', 'scientific_name', 'String', '', None),
        ('🏭', 'manufacturer', 'String', '', None),
        ('📄', 'description_ar', 'Text', '', None),
        ('💉', 'dosage', 'String', '', None),
        ('⚠️', 'side_effects', 'Text', '', None),
        ('📂', 'category', 'String', '', None),
        ('💰', 'price', 'Decimal', '', None),
    ]
    
    for i, (emoji, field, ftype, badge, badge_color) in enumerate(med_fields):
        y = med_y - i * 0.35
        ax.text(12.3, y, emoji, fontsize=11, va='center')
        ax.text(12.8, y, field, fontsize=10, fontweight='600',
               va='center', color=COLORS['dark'])
        ax.text(14.8, y, ftype, fontsize=9, va='center',
               color=COLORS['info'], style='italic')
        if badge:
            badge_box = FancyBboxPatch((16.3, y - 0.12), 0.6, 0.24,
                                      boxstyle="round,pad=0.02",
                                      facecolor=badge_color, edgecolor='none')
            ax.add_patch(badge_box)
            ax.text(16.6, y, badge, fontsize=7, fontweight='bold',
                   ha='center', va='center', color='white')
    
    # IMAGE UPLOAD ENTITY
    upload_y = create_modern_card(ax, 6, 1, 6, 3, 'IMAGE UPLOAD', COLORS['upload'], '📤')
    
    upload_fields = [
        ('🔑', 'id', 'Integer', 'PK', COLORS['warning']),
        ('🖼️', 'image', 'ImageField', '', None),
        ('👤', 'uploaded_by', 'FK → User', 'FK', COLORS['primary']),
        ('💊', 'detected_medicine', 'FK → Medicine', 'FK', COLORS['primary']),
        ('📊', 'confidence', 'Float', '', None),
        ('📝', 'result', 'JSON', '', None),
        ('📅', 'created_at', 'DateTime', '', None),
    ]
    
    for i, (emoji, field, ftype, badge, badge_color) in enumerate(upload_fields):
        y = upload_y - i * 0.35
        ax.text(6.3, y, emoji, fontsize=11, va='center')
        ax.text(6.8, y, field, fontsize=10, fontweight='600',
               va='center', color=COLORS['dark'])
        ax.text(9.5, y, ftype, fontsize=9, va='center',
               color=COLORS['info'], style='italic')
        if badge:
            badge_box = FancyBboxPatch((11, y - 0.12), 0.6, 0.24,
                                      boxstyle="round,pad=0.02",
                                      facecolor=badge_color, edgecolor='none')
            ax.add_patch(badge_box)
            ax.text(11.3, y, badge, fontsize=7, fontweight='bold',
                   ha='center', va='center', color='white')
    
    # RELATIONSHIPS
    # User to ImageUpload
    ax.plot([6, 6.5], [7, 4], color=COLORS['user'], linewidth=4, alpha=0.6, zorder=0)
    
    # Cardinality circles
    c1 = Circle((6, 7), 0.3, facecolor=COLORS['user'], edgecolor='white', linewidth=2.5, zorder=5)
    ax.add_patch(c1)
    ax.text(6, 7, '1', fontsize=13, fontweight='bold', ha='center', va='center', color='white', zorder=6)
    
    c2 = Circle((6.5, 4), 0.3, facecolor=COLORS['user'], edgecolor='white', linewidth=2.5, zorder=5)
    ax.add_patch(c2)
    ax.text(6.5, 4, 'N', fontsize=13, fontweight='bold', ha='center', va='center', color='white', zorder=6)
    
    # Relationship label
    rel1 = FancyBboxPatch((5, 5.3), 2, 0.5, boxstyle="round,pad=0.08",
                         facecolor=COLORS['user'], edgecolor='white', linewidth=2.5, alpha=0.95, zorder=5)
    ax.add_patch(rel1)
    ax.text(6, 5.55, '📤 uploads', fontsize=11, fontweight='bold',
           ha='center', va='center', color='white', zorder=6)
    
    # Medicine to ImageUpload
    ax.plot([12, 11.5], [7, 4], color=COLORS['medicine'], linewidth=4, alpha=0.6, zorder=0)
    
    c3 = Circle((12, 7), 0.3, facecolor=COLORS['medicine'], edgecolor='white', linewidth=2.5, zorder=5)
    ax.add_patch(c3)
    ax.text(12, 7, '1', fontsize=13, fontweight='bold', ha='center', va='center', color='white', zorder=6)
    
    c4 = Circle((11.5, 4), 0.3, facecolor=COLORS['medicine'], edgecolor='white', linewidth=2.5, zorder=5)
    ax.add_patch(c4)
    ax.text(11.5, 4, 'N', fontsize=13, fontweight='bold', ha='center', va='center', color='white', zorder=6)
    
    rel2 = FancyBboxPatch((10.5, 5.3), 2.4, 0.5, boxstyle="round,pad=0.08",
                         facecolor=COLORS['medicine'], edgecolor='white', linewidth=2.5, alpha=0.95, zorder=5)
    ax.add_patch(rel2)
    ax.text(11.7, 5.55, '🔍 detections', fontsize=11, fontweight='bold',
           ha='center', va='center', color='white', zorder=6)
    
    # LEGEND
    legend_box = FancyBboxPatch((0.5, 0.2), 4.5, 0.8, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=COLORS['info'], linewidth=2.5)
    ax.add_patch(legend_box)
    
    ax.text(0.8, 0.75, '📌 Legend', fontsize=12, fontweight='bold', color=COLORS['dark'])
    
    # PK Badge
    pk = FancyBboxPatch((0.8, 0.38), 0.5, 0.25, boxstyle="round,pad=0.02",
                       facecolor=COLORS['warning'], edgecolor='none')
    ax.add_patch(pk)
    ax.text(1.05, 0.5, 'PK', fontsize=8, fontweight='bold', ha='center', va='center', color='white')
    ax.text(1.5, 0.5, '= Primary Key', fontsize=10, va='center')
    
    # FK Badge
    fk = FancyBboxPatch((2.7, 0.38), 0.5, 0.25, boxstyle="round,pad=0.02",
                       facecolor=COLORS['primary'], edgecolor='none')
    ax.add_patch(fk)
    ax.text(2.95, 0.5, 'FK', fontsize=8, fontweight='bold', ha='center', va='center', color='white')
    ax.text(3.4, 0.5, '= Foreign Key', fontsize=10, va='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_ERD.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none', pad_inches=0.3)
    plt.close()
    print("✅ ERD created successfully!")

# =============================================================================
# EERD - Enhanced ERD
# =============================================================================
def create_eerd():
    print("Creating professional EERD...")
    fig = plt.figure(figsize=(18, 12), facecolor='white', dpi=150)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_facecolor('#F8F9FA')
    
    # Title
    title = ax.text(9, 11.2, 'Enhanced Entity Relationship Diagram',
                   fontsize=32, fontweight='bold', ha='center', color=COLORS['dark'])
    title.set_path_effects([path_effects.withStroke(linewidth=4, foreground='white')])
    
    ax.text(9, 10.6, 'MedRec - Detailed Database Design with Attributes',
           fontsize=14, ha='center', color=COLORS['info'], style='italic')
    
    # USER ENTITY (Rectangle)
    user_rect = FancyBboxPatch((1.5, 6.5), 2.5, 1, boxstyle="round,pad=0.08",
                              facecolor=COLORS['user'], edgecolor='white',
                              linewidth=3, alpha=0.9)
    ax.add_patch(user_rect)
    ax.text(2.75, 7, '👤 User', fontsize=13, fontweight='bold',
           ha='center', va='center', color='white')
    
    # User Attributes (Ellipses)
    user_attrs = [
        ('id', 0.8, 5, COLORS['warning'], True, '🔑'),
        ('username', 2, 5, COLORS['success'], False, ''),
        ('email', 3.2, 5, COLORS['success'], False, ''),
        ('password', 0.8, 4, COLORS['info'], False, '🔒'),
        ('first_name', 2, 4, COLORS['info'], False, ''),
        ('last_name', 3.2, 4, COLORS['info'], False, ''),
    ]
    
    for name, x, y, color, is_key, emoji in user_attrs:
        from matplotlib.patches import Ellipse
        ellipse = Ellipse((x, y), 1, 0.45, facecolor=color,
                         edgecolor='white', linewidth=2.5 if is_key else 2, alpha=0.9)
        ax.add_patch(ellipse)
        display = f'{emoji} {name}' if emoji else name
        ax.text(x, y, display, fontsize=8 if is_key else 7,
               fontweight='bold' if is_key else 'normal',
               ha='center', va='center', color='white')
        # Connect to entity
        ax.plot([x, 2.75], [y + 0.23, 6.5], color=color, linewidth=2, alpha=0.6)
    
    # MEDICINE ENTITY
    med_rect = FancyBboxPatch((13, 6.5), 3, 1, boxstyle="round,pad=0.08",
                             facecolor=COLORS['medicine'], edgecolor='white',
                             linewidth=3, alpha=0.9)
    ax.add_patch(med_rect)
    ax.text(14.5, 7, '💊 Medicine', fontsize=13, fontweight='bold',
           ha='center', va='center', color='white')
    
    # Medicine Attributes
    med_attrs = [
        ('id', 12.2, 5, COLORS['warning'], True, '🔑'),
        ('code', 13.5, 5, COLORS['success'], True, '🏷️'),
        ('name_ar', 14.8, 5, COLORS['info'], False, '🇸🇦'),
        ('name_en', 12.2, 4, COLORS['info'], False, '🇬🇧'),
        ('category', 13.5, 4, COLORS['info'], False, '📂'),
        ('price', 14.8, 4, COLORS['info'], False, '💰'),
    ]
    
    for name, x, y, color, is_key, emoji in med_attrs:
        from matplotlib.patches import Ellipse
        ellipse = Ellipse((x, y), 1.1, 0.45, facecolor=color,
                         edgecolor='white', linewidth=2.5 if is_key else 2, alpha=0.9)
        ax.add_patch(ellipse)
        display = f'{emoji} {name}' if emoji else name
        ax.text(x, y, display, fontsize=8 if is_key else 7,
               fontweight='bold' if is_key else 'normal',
               ha='center', va='center', color='white')
        ax.plot([x, 14.5], [y + 0.23, 6.5], color=color, linewidth=2, alpha=0.6)
    
    # IMAGE UPLOAD ENTITY
    upload_rect = FancyBboxPatch((7.25, 2.5), 3.5, 1, boxstyle="round,pad=0.08",
                                facecolor=COLORS['upload'], edgecolor='white',
                                linewidth=3, alpha=0.9)
    ax.add_patch(upload_rect)
    ax.text(9, 3, '📤 ImageUpload', fontsize=13, fontweight='bold',
           ha='center', va='center', color='white')
    
    # ImageUpload Attributes
    upload_attrs = [
        ('id', 6.5, 1.3, COLORS['warning'], True, '🔑'),
        ('image', 8, 1.3, COLORS['info'], False, '🖼️'),
        ('confidence', 9.5, 1.3, COLORS['info'], False, '📊'),
        ('result', 11, 1.3, COLORS['info'], False, '📝'),
    ]
    
    for name, x, y, color, is_key, emoji in upload_attrs:
        from matplotlib.patches import Ellipse
        ellipse = Ellipse((x, y), 1.1, 0.45, facecolor=color,
                         edgecolor='white', linewidth=2.5 if is_key else 2, alpha=0.9)
        ax.add_patch(ellipse)
        display = f'{emoji} {name}' if emoji else name
        ax.text(x, y, display, fontsize=8 if is_key else 7,
               fontweight='bold' if is_key else 'normal',
               ha='center', va='center', color='white')
        ax.plot([x, 9], [y + 0.23, 2.5], color=color, linewidth=2, alpha=0.6)
    
    # RELATIONSHIPS (Diamonds)
    # uploads relationship
    diamond1 = Polygon([(5.5, 5), (6.2, 5.7), (5.5, 6.4), (4.8, 5.7)],
                      facecolor=COLORS['user'], edgecolor='white', linewidth=3, alpha=0.9)
    ax.add_patch(diamond1)
    ax.text(5.5, 5.7, 'uploads', fontsize=9, fontweight='bold',
           ha='center', va='center', color='white')
    
    # Connect User to uploads
    ax.plot([4, 4.8], [7, 5.7], color=COLORS['user'], linewidth=3, alpha=0.7)
    c1 = Circle((4, 7), 0.25, facecolor=COLORS['user'], edgecolor='white', linewidth=2)
    ax.add_patch(c1)
    ax.text(4, 7, '1', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
    
    # Connect uploads to ImageUpload
    ax.plot([6.2, 7.25], [5.7, 3.5], color=COLORS['user'], linewidth=3, alpha=0.7)
    c2 = Circle((7.25, 3.5), 0.25, facecolor=COLORS['user'], edgecolor='white', linewidth=2)
    ax.add_patch(c2)
    ax.text(7.25, 3.5, 'N', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
    
    # detects relationship
    diamond2 = Polygon([(11.5, 5), (12.2, 5.7), (11.5, 6.4), (10.8, 5.7)],
                      facecolor=COLORS['medicine'], edgecolor='white', linewidth=3, alpha=0.9)
    ax.add_patch(diamond2)
    ax.text(11.5, 5.7, 'detects', fontsize=9, fontweight='bold',
           ha='center', va='center', color='white')
    
    # Connect Medicine to detects
    ax.plot([13, 12.2], [7, 5.7], color=COLORS['medicine'], linewidth=3, alpha=0.7)
    c3 = Circle((13, 7), 0.25, facecolor=COLORS['medicine'], edgecolor='white', linewidth=2)
    ax.add_patch(c3)
    ax.text(13, 7, '1', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
    
    # Connect detects to ImageUpload
    ax.plot([10.8, 10.75], [5.7, 3.5], color=COLORS['medicine'], linewidth=3, alpha=0.7)
    c4 = Circle((10.75, 3.5), 0.25, facecolor=COLORS['medicine'], edgecolor='white', linewidth=2)
    ax.add_patch(c4)
    ax.text(10.75, 3.5, 'N', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
    
    # LEGEND
    legend_box = FancyBboxPatch((0.5, 9.2), 5, 0.9, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=COLORS['info'], linewidth=2.5)
    ax.add_patch(legend_box)
    ax.text(0.8, 9.85, '📌 Notation Guide', fontsize=12, fontweight='bold', color=COLORS['dark'])
    
    # Symbols
    from matplotlib.patches import Ellipse
    # PK
    pk_ellipse = Ellipse((1.2, 9.5), 0.6, 0.3, facecolor=COLORS['warning'],
                        edgecolor='white', linewidth=2)
    ax.add_patch(pk_ellipse)
    ax.text(1.2, 9.5, '🔑 PK', fontsize=8, fontweight='bold',
           ha='center', va='center', color='white')
    ax.text(1.8, 9.5, '= Primary Key', fontsize=9, va='center')
    
    # Unique
    unique_ellipse = Ellipse((3.5, 9.5), 0.7, 0.3, facecolor=COLORS['success'],
                            edgecolor='white', linewidth=2)
    ax.add_patch(unique_ellipse)
    ax.text(3.5, 9.5, 'Unique', fontsize=7, fontweight='bold',
           ha='center', va='center', color='white')
    ax.text(4.2, 9.5, '= Unique Constraint', fontsize=9, va='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_EERD.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none', pad_inches=0.3)
    plt.close()
    print("✅ EERD created successfully!")

# =============================================================================
# System Architecture
# =============================================================================
def create_architecture():
    print("Creating professional System Architecture...")
    fig = plt.figure(figsize=(18, 14), facecolor='white', dpi=150)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.axis('off')
    ax.set_facecolor('#F8F9FA')
    
    # Title
    title = ax.text(9, 13.3, 'System Architecture',
                   fontsize=34, fontweight='bold', ha='center', color=COLORS['dark'])
    title.set_path_effects([path_effects.withStroke(linewidth=4, foreground='white')])
    
    ax.text(9, 12.7, 'MedRec - Layered Architecture Design',
           fontsize=14, ha='center', color=COLORS['info'], style='italic')
    
    layer_configs = [
        # (y, height, title, color, components)
        (11, 1.3, '🖥️ CLIENT LAYER', '#3B82F6', [
            ('📱 Mobile App', 2),
            ('🌐 Web App', 9),
            ('🔧 API Tools', 16)
        ]),
        (9.2, 1.2, '🌐 API GATEWAY', '#8B5CF6', [
            ('🔀 Load Balancer', 5.5),
            ('🔐 CORS & Auth', 12.5)
        ]),
        (7, 1.8, '⚙️ APPLICATION LAYER', '#10B981', [
            ('🔐 Auth API', 2),
            ('💊 Medicine API', 7),
            ('📤 Upload API', 12),
            ('👨‍💼 Admin Panel', 16)
        ]),
        (4.8, 1.5, '🔧 SERVICE LAYER', '#F59E0B', [
            ('🎫 JWT Service', 3),
            ('🤖 AI Service', 9),
            ('📋 Serializers', 15)
        ]),
        (2.8, 1.4, '💾 DATA LAYER', '#EF4444', [
            ('🗄️ Database', 5),
            ('📁 Media Storage', 13)
        ]),
        (0.8, 1.4, '🔌 EXTERNAL SERVICES', '#EC4899', [
            ('🧠 AI Model', 5),
            ('📧 Email Service', 13)
        ]),
    ]
    
    for y, height, title, color, components in layer_configs:
        # Layer background
        layer_bg = FancyBboxPatch((0.5, y), 17, height,
                                 boxstyle="round,pad=0.1",
                                 facecolor=color, edgecolor='white',
                                 linewidth=2, alpha=0.15)
        ax.add_patch(layer_bg)
        
        # Layer title
        title_box = FancyBboxPatch((0.7, y + height - 0.4), 3, 0.3,
                                  boxstyle="round,pad=0.05",
                                  facecolor=color, edgecolor='none', alpha=0.95)
        ax.add_patch(title_box)
        ax.text(2.2, y + height - 0.25, title, fontsize=11, fontweight='bold',
               ha='center', va='center', color='white')
        
        # Components
        for comp_name, comp_x in components:
            comp_box = FancyBboxPatch((comp_x - 1.3, y + 0.15), 2.6, height - 0.5,
                                     boxstyle="round,pad=0.08",
                                     facecolor='white', edgecolor=color,
                                     linewidth=2.5, alpha=0.95)
            ax.add_patch(comp_box)
            
            # Split text into lines if needed
            lines = comp_name.split('\n') if '\n' in comp_name else [comp_name]
            if len(lines) == 1:
                ax.text(comp_x, y + height/2, comp_name, fontsize=10, fontweight='600',
                       ha='center', va='center', color=color)
            else:
                for i, line in enumerate(lines):
                    ax.text(comp_x, y + height/2 + 0.15 - i*0.25, line,
                           fontsize=9, fontweight='600', ha='center', va='center', color=color)
    
    # CONNECTIONS (Arrows)
    connections = [
        # Client to Gateway
        (2, 11, 5.5, 10.4, COLORS['primary']),
        (9, 11, 9, 10.4, COLORS['primary']),
        (16, 11, 12.5, 10.4, COLORS['primary']),
        
        # Gateway to Application
        (5.5, 9.2, 2, 8.8, COLORS['secondary']),
        (9, 9.2, 7, 8.8, COLORS['secondary']),
        (12.5, 9.2, 12, 8.8, COLORS['secondary']),
        (12.5, 9.2, 16, 8.8, COLORS['secondary']),
        
        # Application to Service
        (2, 7, 3, 6.3, COLORS['success']),
        (7, 7, 9, 6.3, COLORS['success']),
        (12, 7, 9, 6.3, COLORS['success']),
        (16, 7, 15, 6.3, COLORS['success']),
        
        # Service to Data
        (3, 4.8, 5, 4.2, COLORS['warning']),
        (9, 4.8, 13, 4.2, COLORS['warning']),
        (15, 4.8, 13, 4.2, COLORS['warning']),
        
        # Service to External
        (9, 4.8, 5, 2.2, COLORS['danger'], '--'),
    ]
    
    for x1, y1, x2, y2, color, *style in connections:
        linestyle = style[0] if style else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color=color, lw=2.5,
                                 linestyle=linestyle, alpha=0.7))
    
    # LEGEND
    legend_box = FancyBboxPatch((14.5, 12.2), 3, 0.9, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=COLORS['dark'], linewidth=2)
    ax.add_patch(legend_box)
    ax.text(14.8, 12.9, '🔗 Data Flow', fontsize=11, fontweight='bold', color=COLORS['dark'])
    ax.plot([14.8, 15.3], [12.6, 12.6], color=COLORS['dark'], linewidth=2.5)
    ax.text(15.5, 12.6, '= REST API', fontsize=9, va='center')
    ax.plot([14.8, 15.3], [12.35, 12.35], color=COLORS['danger'], linewidth=2.5, linestyle='--')
    ax.text(15.5, 12.35, '= External Call', fontsize=9, va='center')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_System_Architecture.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none', pad_inches=0.3)
    plt.close()
    print("✅ System Architecture created successfully!")

# =============================================================================
# Main Execution
# =============================================================================
if __name__ == '__main__':
    print("=" * 70)
    print("🎨 GENERATING PROFESSIONAL MEDREC SYSTEM DIAGRAMS")
    print("=" * 70)
    print()
    
    create_erd()
    print()
    create_eerd()
    print()
    create_architecture()
    
    print()
    print("=" * 70)
    print("✅ ALL DIAGRAMS GENERATED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n📁 Output directory: {os.path.abspath(output_dir)}/")
    print("\n📊 Files created:")
    print("   • 01_ERD.png - Entity Relationship Diagram")
    print("   • 02_EERD.png - Enhanced ERD")
    print("   • 03_System_Architecture.png - System Architecture")
    print("\n✨ High-quality diagrams ready for presentation!")
    print("=" * 70)
