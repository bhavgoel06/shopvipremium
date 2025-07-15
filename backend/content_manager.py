#!/usr/bin/env python3
"""
CONTENT MANAGER
Easy tool to update website content without coding
"""

import json
import os

CONTENT_FILE = "/app/frontend/src/content/site_content.json"

def load_content():
    """Load current content"""
    with open(CONTENT_FILE, 'r') as f:
        return json.load(f)

def save_content(content):
    """Save updated content"""
    with open(CONTENT_FILE, 'w') as f:
        json.dump(content, f, indent=2)

def update_homepage_hero(title=None, subtitle=None, primary_button=None, secondary_button=None):
    """Update homepage hero section"""
    content = load_content()
    
    if title:
        content["homepage"]["hero"]["title"] = title
    if subtitle:
        content["homepage"]["hero"]["subtitle"] = subtitle
    if primary_button:
        content["homepage"]["hero"]["primary_button"] = primary_button
    if secondary_button:
        content["homepage"]["hero"]["secondary_button"] = secondary_button
    
    save_content(content)
    print("✅ Homepage hero updated successfully!")

def update_contact_info(email=None, phone=None, whatsapp=None):
    """Update contact information"""
    content = load_content()
    
    if email:
        content["contact"]["email"] = email
    if phone:
        content["contact"]["phone"] = phone
    if whatsapp:
        content["contact"]["whatsapp"] = whatsapp
    
    save_content(content)
    print("✅ Contact information updated successfully!")

def show_current_content():
    """Show current content"""
    content = load_content()
    
    print("\n📄 CURRENT WEBSITE CONTENT")
    print("=" * 50)
    
    print("\n🏠 HOMEPAGE HERO:")
    print(f"Title: {content['homepage']['hero']['title']}")
    print(f"Subtitle: {content['homepage']['hero']['subtitle']}")
    print(f"Primary Button: {content['homepage']['hero']['primary_button']}")
    print(f"Secondary Button: {content['homepage']['hero']['secondary_button']}")
    
    print("\n📞 CONTACT INFO:")
    print(f"Email: {content['contact']['email']}")
    print(f"Phone: {content['contact']['phone']}")
    print(f"WhatsApp: {content['contact']['whatsapp']}")
    
    print("\n💡 ABOUT:")
    print(f"Title: {content['about']['title']}")
    print(f"Mission: {content['about']['mission']}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""
📝 CONTENT MANAGER
=================

Usage: python content_manager.py <command> [options]

Commands:
  show                    - Show current content
  update-hero            - Update homepage hero section
  update-contact         - Update contact information
  
Examples:
  python content_manager.py show
  python content_manager.py update-hero
  python content_manager.py update-contact
        """)
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_content()
    
    elif command == "update-hero":
        print("\n🏠 UPDATE HOMEPAGE HERO")
        print("=" * 30)
        print("(Press Enter to keep current value)")
        
        title = input("New title: ").strip()
        subtitle = input("New subtitle: ").strip()
        primary_button = input("Primary button text: ").strip()
        secondary_button = input("Secondary button text: ").strip()
        
        update_homepage_hero(
            title if title else None,
            subtitle if subtitle else None,
            primary_button if primary_button else None,
            secondary_button if secondary_button else None
        )
    
    elif command == "update-contact":
        print("\n📞 UPDATE CONTACT INFO")
        print("=" * 30)
        print("(Press Enter to keep current value)")
        
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        whatsapp = input("WhatsApp: ").strip()
        
        update_contact_info(
            email if email else None,
            phone if phone else None,
            whatsapp if whatsapp else None
        )
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()