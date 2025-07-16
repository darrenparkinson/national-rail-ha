#!/usr/bin/env python3
"""
Test script to verify Home Assistant add-on structure
"""

import os
import yaml
import json

def test_addon_structure():
    """Test if the add-on structure is correct"""
    print("Testing Home Assistant add-on structure...")
    
    # Check if add-on directory exists
    addon_dir = "national-rail-departure-board"
    if not os.path.exists(addon_dir):
        print("❌ Add-on directory not found")
        return False
    
    print(f"✅ Add-on directory found: {addon_dir}")
    
    # Check required files
    required_files = [
        "config.yaml",
        "Dockerfile",
        "requirements.txt",
        "app.py"
    ]
    
    for file in required_files:
        file_path = os.path.join(addon_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            return False
    
    # Check config.yaml structure
    config_path = os.path.join(addon_dir, "config.yaml")
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        required_config_fields = [
            'name', 'version', 'slug', 'description', 'arch', 
            'startup', 'init', 'ports', 'webui', 'ingress', 
            'ingress_port', 'panel_icon', 'homeassistant_api',
            'schema', 'options'
        ]
        
        for field in required_config_fields:
            if field in config:
                print(f"✅ config.yaml has {field}")
            else:
                print(f"❌ config.yaml missing {field}")
                return False
        
        print("✅ config.yaml structure is correct")
        
    except Exception as e:
        print(f"❌ Error reading config.yaml: {e}")
        return False
    
    # Check static files
    static_dir = os.path.join(addon_dir, "static")
    if os.path.exists(static_dir):
        print("✅ static directory found")
        
        css_dir = os.path.join(static_dir, "css")
        js_dir = os.path.join(static_dir, "js")
        images_dir = os.path.join(static_dir, "images")
        
        if os.path.exists(css_dir):
            print("✅ css directory found")
        if os.path.exists(js_dir):
            print("✅ js directory found")
        if os.path.exists(images_dir):
            print("✅ images directory found")
    else:
        print("❌ static directory missing")
        return False
    
    # Check templates
    templates_dir = os.path.join(addon_dir, "templates")
    if os.path.exists(templates_dir):
        print("✅ templates directory found")
        
        index_html = os.path.join(templates_dir, "index.html")
        if os.path.exists(index_html):
            print("✅ index.html found")
        else:
            print("❌ index.html missing")
            return False
    else:
        print("❌ templates directory missing")
        return False
    
    print("\n🎉 Add-on structure is valid!")
    return True

if __name__ == "__main__":
    test_addon_structure() 