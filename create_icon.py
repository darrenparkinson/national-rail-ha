#!/usr/bin/env python3
"""
Script to create an optimized icon for the Home Assistant add-on
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_addon_icon():
    """Create an optimized icon for the add-on"""
    
    # Create a 128x128 icon with National Rail colors
    size = (128, 128)
    icon = Image.new('RGBA', size, (0, 48, 135, 0))  # National Rail blue with transparency
    
    # Create a simple train icon
    draw = ImageDraw.Draw(icon)
    
    # Draw a train symbol
    # Main body
    draw.rectangle([20, 40, 108, 88], fill=(220, 36, 31), outline=(255, 209, 0), width=3)  # Red with yellow border
    
    # Windows
    draw.rectangle([30, 50, 45, 65], fill=(255, 255, 255))
    draw.rectangle([55, 50, 70, 65], fill=(255, 255, 255))
    draw.rectangle([80, 50, 95, 65], fill=(255, 255, 255))
    
    # Wheels
    draw.ellipse([25, 75, 40, 90], fill=(0, 0, 0))
    draw.ellipse([88, 75, 103, 90], fill=(0, 0, 0))
    
    # Add "NR" text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font = ImageFont.load_default()
    
    # Add "NR" text in white
    draw.text((50, 95), "NR", fill=(255, 255, 255), font=font, anchor="mm")
    
    # Save the icon
    icon_path = "national-rail-departure-board/icon.png"
    icon.save(icon_path, "PNG")
    print(f"✅ Created optimized icon: {icon_path}")
    
    return icon_path

if __name__ == "__main__":
    create_addon_icon() 