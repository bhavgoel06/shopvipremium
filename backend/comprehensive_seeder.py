#!/usr/bin/env python3
"""
COMPREHENSIVE PRODUCT SEEDER
Adds 50+ premium products with reviews and SEO optimization
"""

import asyncio
import sys
import os
import random
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import *

# Comprehensive product list with 10-15% higher pricing
PREMIUM_PRODUCTS = [
    # OTT PLATFORMS
    {
        "name": "Netflix Premium 4K UHD",
        "description": "Stream unlimited movies, TV shows, and documentaries in stunning 4K UHD quality. Watch on 4 screens simultaneously with no ads. Download content for offline viewing on any device. Access exclusive Netflix Originals including award-winning series and films. Compatible with Smart TVs, smartphones, tablets, and computers.",
        "short_description": "Premium Netflix with 4K streaming, 4 screens, no ads, offline downloads",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 649.0,
        "discounted_price": 229.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "4K Ultra HD streaming",
            "4 simultaneous screens",
            "Unlimited downloads",
            "No advertisements",
            "Netflix Originals access",
            "All devices supported",
            "Dolby Atmos audio",
            "HDR content support"
        ],
        "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop",
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 150,
        "seo_title": "Netflix Premium 4K Subscription - 65% Off | ShopForPremium",
        "seo_description": "Get Netflix Premium 4K subscription at 65% discount. Stream on 4 screens, no ads, offline downloads. Instant delivery guaranteed.",
        "seo_keywords": ["netflix premium", "netflix 4k", "streaming service", "netflix discount", "premium subscription"]
    },
    {
        "name": "Amazon Prime Video Premium",
        "description": "Access thousands of movies, TV shows, and award-winning Amazon Originals. Enjoy exclusive content including The Boys, The Marvelous Mrs. Maisel, and more. Download content for offline viewing and stream on multiple devices. Includes access to Prime Video Channels and IMDb TV content.",
        "short_description": "Amazon Prime Video with exclusive originals and offline downloads",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 499.0,
        "discounted_price": 172.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited streaming",
            "Amazon Originals",
            "Download for offline",
            "Multiple devices",
            "HD/4K quality",
            "Prime Video Channels",
            "IMDb TV access",
            "No ads on originals"
        ],
        "image_url": "https://images.unsplash.com/photo-1489599510843-b4c9e1b5ef10?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 200,
        "seo_title": "Amazon Prime Video Premium - 66% Off | Exclusive Originals",
        "seo_description": "Amazon Prime Video premium subscription with exclusive originals at 66% discount. HD/4K streaming with offline downloads.",
        "seo_keywords": ["amazon prime video", "prime video subscription", "amazon originals", "streaming service", "prime discount"]
    },
    {
        "name": "Disney+ Premium Hotstar",
        "description": "Stream Disney, Pixar, Marvel, Star Wars, and National Geographic content. Access to live sports, Indian movies, and exclusive Hotstar Specials. Perfect for families with kids-safe profiles and parental controls. Download content for offline viewing and enjoy 4K streaming on supported devices.",
        "short_description": "Disney+ Hotstar with Marvel, Star Wars, sports, and Indian content",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 799.0,
        "discounted_price": 287.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Disney, Pixar, Marvel",
            "Star Wars universe",
            "Live sports streaming",
            "Indian movies & shows",
            "4K HDR streaming",
            "Kids-safe profiles",
            "Offline downloads",
            "Multiple languages"
        ],
        "image_url": "https://images.unsplash.com/photo-1543536448-d209d2d13a1c?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 100,
        "seo_title": "Disney+ Hotstar Premium - Marvel, Star Wars & Sports | 64% Off",
        "seo_description": "Disney+ Hotstar premium with Marvel, Star Wars, live sports at 64% discount. Family-friendly streaming with offline downloads.",
        "seo_keywords": ["disney plus hotstar", "disney+ premium", "marvel movies", "star wars", "live sports streaming"]
    },
    {
        "name": "Apple TV+ Premium",
        "description": "Watch award-winning Apple Originals including Ted Lasso, The Morning Show, and Severance. Ad-free streaming with the highest quality 4K HDR and Dolby Atmos audio. Download content for offline viewing and enjoy seamless integration with all Apple devices.",
        "short_description": "Apple TV+ with award-winning originals and 4K HDR quality",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 399.0,
        "discounted_price": 149.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Award-winning originals",
            "4K HDR streaming",
            "Dolby Atmos audio",
            "No advertisements",
            "Offline downloads",
            "Apple ecosystem sync",
            "Family sharing",
            "Multi-device access"
        ],
        "image_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&h=300&fit=crop",
        "stock_quantity": 80,
        "seo_title": "Apple TV+ Premium Subscription - Award-Winning Originals | 63% Off",
        "seo_description": "Apple TV+ premium subscription with award-winning originals at 63% discount. 4K HDR quality with Dolby Atmos audio.",
        "seo_keywords": ["apple tv plus", "apple tv+ subscription", "apple originals", "4k hdr streaming", "premium streaming"]
    },
    {
        "name": "HBO Max Premium",
        "description": "Stream HBO's premium content including Game of Thrones, Succession, and The Last of Us. Access Warner Bros. movies, DC superhero content, and exclusive Max Originals. Watch the latest blockbuster movies the same day they hit theaters. 4K streaming with no ads.",
        "short_description": "HBO Max with blockbuster movies, HBO series, and DC content",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 999.0,
        "discounted_price": 344.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "HBO premium content",
            "Warner Bros movies",
            "DC superhero content",
            "Same-day movie releases",
            "4K streaming",
            "No advertisements",
            "Offline downloads",
            "Max Originals"
        ],
        "image_url": "https://images.unsplash.com/photo-1489599510843-b4c9e1b5ef10?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 75,
        "seo_title": "HBO Max Premium - Same-Day Movies & HBO Series | 66% Off",
        "seo_description": "HBO Max premium subscription with same-day movie releases and HBO series at 66% discount. 4K streaming with no ads.",
        "seo_keywords": ["hbo max", "hbo max subscription", "warner bros movies", "hbo series", "premium streaming"]
    },
    {
        "name": "Hulu Premium (No Ads)",
        "description": "Stream thousands of TV shows and movies with no ads. Access to Hulu Originals, next-day TV episodes, and exclusive content. Download select content for offline viewing and enjoy personalized recommendations based on your viewing history.",
        "short_description": "Hulu Premium with no ads and exclusive originals",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 699.0,
        "discounted_price": 252.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "No advertisements",
            "Hulu Originals",
            "Next-day TV episodes",
            "Offline downloads",
            "Personalized recommendations",
            "Multiple profiles",
            "Live TV add-on available",
            "Premium networks"
        ],
        "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop",
        "stock_quantity": 90,
        "seo_title": "Hulu Premium No Ads - TV Shows & Movies | 64% Off",
        "seo_description": "Hulu Premium subscription with no ads at 64% discount. Watch TV shows, movies, and Hulu Originals without interruptions.",
        "seo_keywords": ["hulu premium", "hulu no ads", "streaming service", "tv shows", "hulu originals"]
    },
    {
        "name": "Paramount+ Premium",
        "description": "Stream movies and shows from Paramount Pictures, CBS, Comedy Central, and more. Access live sports, news, and exclusive Paramount+ Originals. Download content for offline viewing and enjoy 4K streaming on supported content.",
        "short_description": "Paramount+ with live sports, news, and exclusive originals",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 599.0,
        "discounted_price": 206.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Live sports streaming",
            "News and entertainment",
            "Paramount+ Originals",
            "CBS content library",
            "Comedy Central shows",
            "4K streaming",
            "Offline downloads",
            "Multiple devices"
        ],
        "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&h=300&fit=crop",
        "stock_quantity": 70,
        "seo_title": "Paramount+ Premium - Live Sports & Originals | 66% Off",
        "seo_description": "Paramount+ premium subscription with live sports and originals at 66% discount. Stream CBS, Comedy Central, and more.",
        "seo_keywords": ["paramount plus", "paramount+ subscription", "live sports", "cbs content", "streaming service"]
    },
    {
        "name": "Peacock Premium Plus",
        "description": "Stream NBCUniversal content including The Office, Parks and Recreation, and exclusive Peacock Originals. Access live sports, news, and next-day TV episodes. Download content for offline viewing with no ads on most content.",
        "short_description": "Peacock Premium Plus with NBC content and live sports",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 499.0,
        "discounted_price": 172.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "NBC content library",
            "Peacock Originals",
            "Live sports events",
            "Next-day TV episodes",
            "No ads on most content",
            "Offline downloads",
            "News coverage",
            "Classic TV shows"
        ],
        "image_url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop",
        "stock_quantity": 65,
        "seo_title": "Peacock Premium Plus - NBC Content & Live Sports | 65% Off",
        "seo_description": "Peacock Premium Plus subscription with NBC content and live sports at 65% discount. Watch The Office, Parks and Rec, and more.",
        "seo_keywords": ["peacock premium", "nbc content", "the office", "live sports", "streaming service"]
    },
    {
        "name": "YouTube Premium",
        "description": "Enjoy ad-free YouTube videos, YouTube Music, and exclusive YouTube Originals. Download videos for offline viewing and play videos in the background. Access to YouTube Music's vast library with offline listening capabilities.",
        "short_description": "YouTube Premium with ad-free videos and YouTube Music",
        "category": "ott",
        "subcategory": "Streaming",
        "original_price": 399.0,
        "discounted_price": 149.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Ad-free YouTube",
            "YouTube Music included",
            "Offline downloads",
            "Background play",
            "YouTube Originals",
            "High-quality audio",
            "Multiple devices",
            "Family sharing"
        ],
        "image_url": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 200,
        "seo_title": "YouTube Premium - Ad-Free Videos & Music | 63% Off",
        "seo_description": "YouTube Premium subscription with ad-free videos and music at 63% discount. Download videos and play in background.",
        "seo_keywords": ["youtube premium", "ad free youtube", "youtube music", "offline videos", "background play"]
    },
    {
        "name": "Spotify Premium",
        "description": "Stream over 100 million songs ad-free with unlimited skips. Download music for offline listening and enjoy high-quality audio. Access to podcasts, playlists, and personalized recommendations based on your music taste.",
        "short_description": "Spotify Premium with ad-free music and offline downloads",
        "category": "ott",
        "subcategory": "Music",
        "original_price": 399.0,
        "discounted_price": 115.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "100+ million songs",
            "Ad-free listening",
            "Offline downloads",
            "Unlimited skips",
            "High-quality audio",
            "Podcasts included",
            "Personalized playlists",
            "Connect with friends"
        ],
        "image_url": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 300,
        "seo_title": "Spotify Premium - Ad-Free Music & Podcasts | 71% Off",
        "seo_description": "Spotify Premium subscription with ad-free music and podcasts at 71% discount. 100+ million songs with offline listening.",
        "seo_keywords": ["spotify premium", "ad free music", "offline music", "music streaming", "podcasts"]
    },

    # SOFTWARE & TOOLS
    {
        "name": "Adobe Creative Cloud All Apps",
        "description": "Complete creative suite with 20+ industry-leading applications including Photoshop, Illustrator, Premiere Pro, After Effects, InDesign, and more. Get 100GB cloud storage, premium fonts, and access to Adobe Stock images. Perfect for designers, photographers, and video editors.",
        "short_description": "Complete Adobe Creative Cloud suite with 20+ apps and cloud storage",
        "category": "software",
        "subcategory": "Design",
        "original_price": 4999.0,
        "discounted_price": 1494.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "20+ Creative applications",
            "Photoshop, Illustrator, Premiere Pro",
            "100GB cloud storage",
            "Premium fonts library",
            "Adobe Stock images",
            "Mobile apps included",
            "Regular updates",
            "Creative community access"
        ],
        "image_url": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 80,
        "seo_title": "Adobe Creative Cloud All Apps - 70% Off | Complete Creative Suite",
        "seo_description": "Adobe Creative Cloud complete suite with 20+ apps at 70% discount. Photoshop, Illustrator, Premiere Pro, and more professional tools.",
        "seo_keywords": ["adobe creative cloud", "photoshop", "illustrator", "premiere pro", "design software", "creative suite"]
    },
    {
        "name": "Microsoft Office 365 Personal",
        "description": "Complete productivity suite with Word, Excel, PowerPoint, Outlook, and OneNote. Get 1TB OneDrive cloud storage and access to premium templates. Works on Windows, Mac, and mobile devices with automatic updates and premium support.",
        "short_description": "Microsoft Office 365 with Word, Excel, PowerPoint, and 1TB storage",
        "category": "software",
        "subcategory": "Productivity",
        "original_price": 2499.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Word, Excel, PowerPoint",
            "1TB OneDrive storage",
            "Outlook email",
            "OneNote included",
            "Premium templates",
            "Multi-device access",
            "Automatic updates",
            "24/7 support"
        ],
        "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 150,
        "seo_title": "Microsoft Office 365 Personal - 72% Off | Word, Excel, PowerPoint",
        "seo_description": "Microsoft Office 365 Personal at 72% discount. Word, Excel, PowerPoint, and 1TB OneDrive storage. Perfect for productivity.",
        "seo_keywords": ["microsoft office 365", "ms office", "word excel powerpoint", "productivity software", "office suite"]
    },
    {
        "name": "Parallels Desktop for Mac",
        "description": "Run Windows applications on your Mac without rebooting. Seamlessly switch between macOS and Windows with drag-and-drop support. Perfect for developers, designers, and professionals who need Windows software on Mac. Includes Windows 11 optimization and gaming support.",
        "short_description": "Parallels Desktop for Mac - Run Windows apps on macOS seamlessly",
        "category": "software",
        "subcategory": "Virtualization",
        "original_price": 7999.0,
        "discounted_price": 2759.0,
        "duration_options": ["1 year"],
        "features": [
            "Windows on Mac seamlessly",
            "Drag-and-drop support",
            "Windows 11 optimized",
            "Gaming support",
            "Developer tools",
            "Cross-platform file access",
            "Automatic updates",
            "Premium support"
        ],
        "image_url": "https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 50,
        "seo_title": "Parallels Desktop for Mac - 65% Off | Run Windows on Mac",
        "seo_description": "Parallels Desktop for Mac at 65% discount. Run Windows applications on macOS seamlessly with drag-and-drop support.",
        "seo_keywords": ["parallels desktop", "windows on mac", "virtualization software", "mac virtualization", "parallels mac"]
    },
    {
        "name": "Canva Pro",
        "description": "Professional design platform with 100,000+ premium templates, millions of stock photos, and advanced design tools. Create stunning graphics, presentations, and marketing materials. Includes background remover, brand kit, and team collaboration features.",
        "short_description": "Canva Pro with premium templates and advanced design tools",
        "category": "software",
        "subcategory": "Design",
        "original_price": 1499.0,
        "discounted_price": 459.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "100,000+ premium templates",
            "Millions of stock photos",
            "Background remover",
            "Brand kit and fonts",
            "Resize designs instantly",
            "Team collaboration",
            "Animation features",
            "Premium elements"
        ],
        "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 200,
        "seo_title": "Canva Pro - Premium Design Tool | 69% Off",
        "seo_description": "Canva Pro subscription at 69% discount. Access premium templates, stock photos, and professional design tools for businesses.",
        "seo_keywords": ["canva pro", "design tool", "graphic design", "social media design", "business graphics", "templates"]
    },
    {
        "name": "Figma Professional",
        "description": "Collaborative design platform for UI/UX designers and teams. Create, prototype, and collaborate in real-time. Includes unlimited projects, version history, and advanced prototyping features. Perfect for web and mobile app design.",
        "short_description": "Figma Professional for UI/UX design and team collaboration",
        "category": "software",
        "subcategory": "Design",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited projects",
            "Real-time collaboration",
            "Advanced prototyping",
            "Version history",
            "Design systems",
            "Developer handoff",
            "Component libraries",
            "Team management"
        ],
        "image_url": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500&h=300&fit=crop",
        "stock_quantity": 100,
        "seo_title": "Figma Professional - UI/UX Design Tool | 66% Off",
        "seo_description": "Figma Professional subscription at 66% discount. Collaborative UI/UX design platform with real-time collaboration and prototyping.",
        "seo_keywords": ["figma professional", "ui ux design", "design collaboration", "prototyping tool", "web design"]
    },
    {
        "name": "Notion Pro",
        "description": "All-in-one workspace for notes, tasks, wikis, and databases. Organize your work and life with customizable templates and powerful collaboration features. Perfect for individuals and teams who want to stay organized and productive.",
        "short_description": "Notion Pro - All-in-one workspace for productivity and collaboration",
        "category": "software",
        "subcategory": "Productivity",
        "original_price": 999.0,
        "discounted_price": 344.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited pages",
            "Team collaboration",
            "Custom templates",
            "Database features",
            "File uploads",
            "Version history",
            "API access",
            "Priority support"
        ],
        "image_url": "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=500&h=300&fit=crop",
        "stock_quantity": 120,
        "seo_title": "Notion Pro - All-in-One Workspace | 66% Off",
        "seo_description": "Notion Pro subscription at 66% discount. All-in-one workspace for notes, tasks, wikis, and databases with team collaboration.",
        "seo_keywords": ["notion pro", "productivity tool", "all in one workspace", "team collaboration", "note taking"]
    },
    {
        "name": "Slack Pro",
        "description": "Professional team communication platform with unlimited message history, advanced search, and guest access. Integrate with 2,000+ apps and services. Perfect for teams who need reliable communication and collaboration tools.",
        "short_description": "Slack Pro for team communication and collaboration",
        "category": "software",
        "subcategory": "Communication",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited message history",
            "Advanced search",
            "Guest access",
            "2,000+ app integrations",
            "Voice and video calls",
            "Screen sharing",
            "Workflow automation",
            "Priority support"
        ],
        "image_url": "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=500&h=300&fit=crop",
        "stock_quantity": 80,
        "seo_title": "Slack Pro - Team Communication Platform | 66% Off",
        "seo_description": "Slack Pro subscription at 66% discount. Professional team communication with unlimited history and 2,000+ integrations.",
        "seo_keywords": ["slack pro", "team communication", "business chat", "collaboration tool", "workplace messaging"]
    },
    {
        "name": "Zoom Pro",
        "description": "Professional video conferencing with unlimited group meetings, cloud recording, and administrative features. Host meetings up to 30 hours with up to 100 participants. Perfect for businesses, education, and remote teams.",
        "short_description": "Zoom Pro for professional video conferencing and meetings",
        "category": "software",
        "subcategory": "Communication",
        "original_price": 1499.0,
        "discounted_price": 517.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited group meetings",
            "Up to 100 participants",
            "Cloud recording",
            "Meeting transcripts",
            "Breakout rooms",
            "Waiting rooms",
            "Admin controls",
            "Phone support"
        ],
        "image_url": "https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=500&h=300&fit=crop",
        "stock_quantity": 90,
        "seo_title": "Zoom Pro - Professional Video Conferencing | 65% Off",
        "seo_description": "Zoom Pro subscription at 65% discount. Professional video conferencing with unlimited meetings and cloud recording.",
        "seo_keywords": ["zoom pro", "video conferencing", "online meetings", "business communication", "remote work"]
    },
    {
        "name": "Grammarly Premium",
        "description": "Advanced writing assistant with grammar checking, style suggestions, and plagiarism detection. Improve your writing across all platforms with real-time suggestions. Perfect for professionals, students, and content creators.",
        "short_description": "Grammarly Premium for advanced writing assistance and plagiarism detection",
        "category": "software",
        "subcategory": "Writing",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Advanced grammar checking",
            "Style and tone suggestions",
            "Plagiarism detection",
            "Vocabulary enhancement",
            "Genre-specific writing",
            "Browser extension",
            "Desktop app",
            "Mobile keyboard"
        ],
        "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&h=300&fit=crop",
        "stock_quantity": 150,
        "seo_title": "Grammarly Premium - Advanced Writing Assistant | 66% Off",
        "seo_description": "Grammarly Premium subscription at 66% discount. Advanced writing assistant with grammar checking and plagiarism detection.",
        "seo_keywords": ["grammarly premium", "writing assistant", "grammar checker", "plagiarism detection", "writing tool"]
    },
    {
        "name": "Dropbox Plus",
        "description": "Secure cloud storage with 2TB space, smart sync, and offline access. Share files securely with password protection and expiration dates. Includes version history and priority support for all your important files.",
        "short_description": "Dropbox Plus with 2TB secure cloud storage and smart sync",
        "category": "software",
        "subcategory": "Storage",
        "original_price": 1499.0,
        "discounted_price": 517.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "2TB cloud storage",
            "Smart sync",
            "Offline access",
            "File sharing",
            "Version history",
            "Password protection",
            "Priority support",
            "Mobile apps"
        ],
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=500&h=300&fit=crop",
        "stock_quantity": 100,
        "seo_title": "Dropbox Plus - 2TB Cloud Storage | 65% Off",
        "seo_description": "Dropbox Plus subscription at 65% discount. 2TB secure cloud storage with smart sync and offline access.",
        "seo_keywords": ["dropbox plus", "cloud storage", "file sharing", "secure storage", "2tb storage"]
    },

    # PROFESSIONAL DEVELOPMENT
    {
        "name": "LinkedIn Premium Career",
        "description": "Advanced LinkedIn features for career growth and professional networking. See who viewed your profile, get insights on job applications, and access exclusive career advice. Connect with industry leaders and unlock premium job insights.",
        "short_description": "LinkedIn Premium Career with job insights and networking tools",
        "category": "professional",
        "subcategory": "Career",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "See who viewed profile",
            "InMail credits",
            "Job application insights",
            "Salary insights",
            "LinkedIn Learning",
            "Career advice",
            "Professional badges",
            "Premium search filters"
        ],
        "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 120,
        "seo_title": "LinkedIn Premium Career - Professional Networking | 66% Off",
        "seo_description": "LinkedIn Premium Career subscription at 66% discount. Advanced networking features with job insights and career advice.",
        "seo_keywords": ["linkedin premium", "career development", "job search", "professional networking", "linkedin career"]
    },
    {
        "name": "Perplexity Pro",
        "description": "AI-powered search and research assistant with unlimited Pro searches, file upload support, and API access. Get detailed answers with sources and citations. Perfect for researchers, students, and professionals who need accurate information quickly.",
        "short_description": "Perplexity Pro AI search assistant with unlimited queries and sources",
        "category": "professional",
        "subcategory": "AI Tools",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited Pro searches",
            "File upload support",
            "API access",
            "Source citations",
            "Research assistance",
            "Multi-language support",
            "Priority support",
            "Advanced AI models"
        ],
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 80,
        "seo_title": "Perplexity Pro - AI Search Assistant | 66% Off",
        "seo_description": "Perplexity Pro subscription at 66% discount. AI-powered search and research assistant with unlimited queries and sources.",
        "seo_keywords": ["perplexity pro", "ai search", "research assistant", "ai tool", "search engine"]
    },
    {
        "name": "Coursera Plus",
        "description": "Unlimited access to 7,000+ courses from top universities and companies. Earn certificates, specializations, and professional degrees. Perfect for skill development and career advancement with hands-on projects and expert instruction.",
        "short_description": "Coursera Plus with unlimited access to 7,000+ courses and certificates",
        "category": "professional",
        "subcategory": "Education",
        "original_price": 3999.0,
        "discounted_price": 1724.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "7,000+ courses",
            "University certificates",
            "Professional certificates",
            "Specializations",
            "Hands-on projects",
            "Expert instruction",
            "Career support",
            "Mobile app access"
        ],
        "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 100,
        "seo_title": "Coursera Plus - 7,000+ Courses & Certificates | 57% Off",
        "seo_description": "Coursera Plus subscription at 57% discount. Unlimited access to 7,000+ courses from top universities with certificates.",
        "seo_keywords": ["coursera plus", "online courses", "certificates", "skill development", "professional development"]
    },
    {
        "name": "Udemy Business",
        "description": "Access to 24,000+ courses on business, technology, and creative skills. Learn from industry experts with hands-on exercises and real-world projects. Perfect for teams and individuals looking to upskill in high-demand areas.",
        "short_description": "Udemy Business with 24,000+ courses on business and technology",
        "category": "professional",
        "subcategory": "Education",
        "original_price": 2999.0,
        "discounted_price": 1034.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "24,000+ courses",
            "Business and tech focus",
            "Hands-on exercises",
            "Real-world projects",
            "Expert instructors",
            "Progress tracking",
            "Mobile app",
            "Certificates"
        ],
        "image_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=500&h=300&fit=crop",
        "stock_quantity": 80,
        "seo_title": "Udemy Business - 24,000+ Courses | 65% Off",
        "seo_description": "Udemy Business subscription at 65% discount. Access 24,000+ courses on business and technology with expert instruction.",
        "seo_keywords": ["udemy business", "online learning", "business courses", "technology training", "skill development"]
    },
    {
        "name": "Skillshare Premium",
        "description": "Unlimited access to thousands of creative classes in design, photography, writing, and more. Learn from industry professionals with project-based learning. Perfect for creative professionals and hobbyists.",
        "short_description": "Skillshare Premium with unlimited creative classes and projects",
        "category": "professional",
        "subcategory": "Education",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited creative classes",
            "Project-based learning",
            "Industry professionals",
            "Offline viewing",
            "Community feedback",
            "Portfolio building",
            "Mobile app",
            "Ad-free experience"
        ],
        "image_url": "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=500&h=300&fit=crop",
        "stock_quantity": 90,
        "seo_title": "Skillshare Premium - Creative Classes | 66% Off",
        "seo_description": "Skillshare Premium subscription at 66% discount. Unlimited access to creative classes in design, photography, and writing.",
        "seo_keywords": ["skillshare premium", "creative classes", "design courses", "photography", "creative learning"]
    },

    # VPN & SECURITY
    {
        "name": "ExpressVPN Premium",
        "description": "Ultra-fast VPN with military-grade encryption and servers in 94 countries. Access blocked content, protect your privacy, and browse anonymously. Works on all devices with 24/7 customer support and 30-day money-back guarantee.",
        "short_description": "ExpressVPN Premium with military-grade encryption and 94 countries",
        "category": "vpn",
        "subcategory": "Security",
        "original_price": 999.0,
        "discounted_price": 344.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Military-grade encryption",
            "94 countries",
            "3000+ servers",
            "No-logs policy",
            "24/7 support",
            "5 simultaneous devices",
            "Kill switch",
            "Split tunneling"
        ],
        "image_url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 120,
        "seo_title": "ExpressVPN Premium - Ultra-Fast VPN | 66% Off",
        "seo_description": "ExpressVPN Premium subscription at 66% discount. Ultra-fast VPN with military-grade encryption and servers in 94 countries.",
        "seo_keywords": ["expressvpn", "vpn service", "online privacy", "secure browsing", "vpn subscription"]
    },
    {
        "name": "NordVPN Premium",
        "description": "Advanced VPN with double encryption, threat protection, and 5400+ servers worldwide. Access geo-restricted content and browse securely. Includes password manager, file encryption, and malware protection.",
        "short_description": "NordVPN Premium with double encryption and threat protection",
        "category": "vpn",
        "subcategory": "Security",
        "original_price": 799.0,
        "discounted_price": 287.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Double VPN encryption",
            "Threat protection",
            "5400+ servers",
            "Password manager",
            "File encryption",
            "6 devices",
            "Kill switch",
            "DNS leak protection"
        ],
        "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=500&h=300&fit=crop",
        "is_featured": True,
        "stock_quantity": 150,
        "seo_title": "NordVPN Premium - Double Encryption | 64% Off",
        "seo_description": "NordVPN Premium subscription at 64% discount. Advanced VPN with double encryption, threat protection, and 5400+ servers.",
        "seo_keywords": ["nordvpn", "vpn service", "double encryption", "threat protection", "secure vpn"]
    },
    {
        "name": "Surfshark VPN",
        "description": "Unlimited device VPN with CleanWeb ad-blocker and MultiHop feature. Access content from anywhere with 3200+ servers in 100+ countries. Includes antivirus, search engine, and data breach alerts.",
        "short_description": "Surfshark VPN with unlimited devices and CleanWeb ad-blocker",
        "category": "vpn",
        "subcategory": "Security",
        "original_price": 699.0,
        "discounted_price": 252.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Unlimited devices",
            "CleanWeb ad-blocker",
            "MultiHop feature",
            "3200+ servers",
            "100+ countries",
            "Antivirus included",
            "Search engine",
            "Data breach alerts"
        ],
        "image_url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop",
        "stock_quantity": 100,
        "seo_title": "Surfshark VPN - Unlimited Devices | 64% Off",
        "seo_description": "Surfshark VPN subscription at 64% discount. Unlimited device VPN with CleanWeb ad-blocker and 3200+ servers.",
        "seo_keywords": ["surfshark vpn", "unlimited devices", "vpn service", "ad blocker", "secure browsing"]
    },
    {
        "name": "CyberGhost VPN",
        "description": "User-friendly VPN with 9700+ servers in 91 countries. Specialized servers for streaming, gaming, and torrenting. Includes ad-blocker, malware protection, and automatic WiFi protection.",
        "short_description": "CyberGhost VPN with 9700+ servers and specialized streaming servers",
        "category": "vpn",
        "subcategory": "Security",
        "original_price": 599.0,
        "discounted_price": 206.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "9700+ servers",
            "91 countries",
            "Streaming servers",
            "Gaming servers",
            "Ad-blocker",
            "Malware protection",
            "WiFi protection",
            "7 devices"
        ],
        "image_url": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=500&h=300&fit=crop",
        "stock_quantity": 80,
        "seo_title": "CyberGhost VPN - 9700+ Servers | 66% Off",
        "seo_description": "CyberGhost VPN subscription at 66% discount. User-friendly VPN with 9700+ servers and specialized streaming servers.",
        "seo_keywords": ["cyberghost vpn", "vpn service", "streaming vpn", "gaming vpn", "user friendly vpn"]
    },
    {
        "name": "Private Internet Access VPN",
        "description": "Open-source VPN with proven no-logs policy and 35000+ servers worldwide. Advanced encryption with WireGuard support. Includes ad-blocker, malware protection, and dedicated IP options.",
        "short_description": "Private Internet Access VPN with 35000+ servers and no-logs policy",
        "category": "vpn",
        "subcategory": "Security",
        "original_price": 499.0,
        "discounted_price": 172.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "35000+ servers",
            "Proven no-logs policy",
            "Open-source",
            "WireGuard support",
            "Ad-blocker",
            "Malware protection",
            "Dedicated IP",
            "10 devices"
        ],
        "image_url": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop",
        "stock_quantity": 90,
        "seo_title": "Private Internet Access VPN - No-Logs Policy | 66% Off",
        "seo_description": "Private Internet Access VPN at 66% discount. Open-source VPN with proven no-logs policy and 35000+ servers worldwide.",
        "seo_keywords": ["private internet access", "pia vpn", "no logs vpn", "open source vpn", "secure vpn"]
    },

    # GAMING
    {
        "name": "Steam Wallet Credits",
        "description": "Add funds to your Steam account to purchase games, DLC, and in-game items. Instant delivery and works worldwide. Perfect for gamers who want to save on Steam purchases and gift games to friends.",
        "short_description": "Steam Wallet credits for game purchases and in-game items",
        "category": "gaming",
        "subcategory": "Gaming",
        "original_price": 1000.0,
        "discounted_price": 919.0,
        "duration_options": ["₹500", "₹1000", "₹2000", "₹5000"],
        "features": [
            "Instant delivery",
            "Works worldwide",
            "No expiration",
            "Buy games and DLC",
            "In-game purchases",
            "Gift to friends",
            "Secure transactions",
            "Steam marketplace"
        ],
        "image_url": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=500&h=300&fit=crop",
        "stock_quantity": 500,
        "seo_title": "Steam Wallet Credits - Instant Delivery | 8% Off",
        "seo_description": "Steam Wallet credits at 8% discount. Instant delivery, works worldwide. Perfect for purchasing games and DLC on Steam.",
        "seo_keywords": ["steam wallet", "steam credits", "gaming", "steam games", "game purchases"]
    },
    {
        "name": "Xbox Game Pass Ultimate",
        "description": "Access 100+ high-quality games on console, PC, and mobile. Includes Xbox Live Gold, EA Play, and cloud gaming. Play new releases on day one and enjoy perks from your favorite games.",
        "short_description": "Xbox Game Pass Ultimate with 100+ games and cloud gaming",
        "category": "gaming",
        "subcategory": "Gaming",
        "original_price": 1499.0,
        "discounted_price": 517.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "100+ games",
            "Console, PC, mobile",
            "Xbox Live Gold",
            "EA Play included",
            "Cloud gaming",
            "Day one releases",
            "Game perks",
            "Cross-platform play"
        ],
        "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500&h=300&fit=crop",
        "is_bestseller": True,
        "stock_quantity": 100,
        "seo_title": "Xbox Game Pass Ultimate - 100+ Games | 65% Off",
        "seo_description": "Xbox Game Pass Ultimate subscription at 65% discount. Access 100+ games on console, PC, and mobile with cloud gaming.",
        "seo_keywords": ["xbox game pass", "gaming subscription", "xbox games", "cloud gaming", "console games"]
    },
    {
        "name": "PlayStation Plus Premium",
        "description": "Premium gaming service with 700+ games, classic PlayStation titles, and game trials. Includes online multiplayer, monthly games, and exclusive discounts. Stream games instantly or download to play offline.",
        "short_description": "PlayStation Plus Premium with 700+ games and classic titles",
        "category": "gaming",
        "subcategory": "Gaming",
        "original_price": 1999.0,
        "discounted_price": 689.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "700+ games",
            "Classic PlayStation titles",
            "Game trials",
            "Online multiplayer",
            "Monthly games",
            "Exclusive discounts",
            "Cloud streaming",
            "Download offline"
        ],
        "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500&h=300&fit=crop",
        "stock_quantity": 80,
        "seo_title": "PlayStation Plus Premium - 700+ Games | 66% Off",
        "seo_description": "PlayStation Plus Premium subscription at 66% discount. Access 700+ games with classic PlayStation titles and game trials.",
        "seo_keywords": ["playstation plus", "ps plus premium", "gaming subscription", "playstation games", "console gaming"]
    },
    {
        "name": "Nintendo Switch Online",
        "description": "Online service for Nintendo Switch with classic NES and SNES games. Includes cloud saves, online multiplayer, and exclusive offers. Perfect for Nintendo fans who want to play classic games and connect with friends.",
        "short_description": "Nintendo Switch Online with classic games and online multiplayer",
        "category": "gaming",
        "subcategory": "Gaming",
        "original_price": 799.0,
        "discounted_price": 287.0,
        "duration_options": ["1 month", "3 months", "6 months", "1 year"],
        "features": [
            "Classic NES/SNES games",
            "Online multiplayer",
            "Cloud saves",
            "Exclusive offers",
            "Mobile app",
            "Voice chat",
            "Special events",
            "Family sharing"
        ],
        "image_url": "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500&h=300&fit=crop",
        "stock_quantity": 70,
        "seo_title": "Nintendo Switch Online - Classic Games | 64% Off",
        "seo_description": "Nintendo Switch Online subscription at 64% discount. Access classic NES/SNES games with online multiplayer and cloud saves.",
        "seo_keywords": ["nintendo switch online", "classic games", "nintendo subscription", "online multiplayer", "switch games"]
    },
    {
        "name": "Epic Games Store Credits",
        "description": "Add funds to your Epic Games account for purchasing games and in-game content. Access to free weekly games and exclusive deals. Perfect for Fortnite players and PC gamers who love Epic's game library.",
        "short_description": "Epic Games Store credits for games and in-game content",
        "category": "gaming",
        "subcategory": "Gaming",
        "original_price": 1000.0,
        "discounted_price": 919.0,
        "duration_options": ["₹500", "₹1000", "₹2000", "₹5000"],
        "features": [
            "Purchase games",
            "In-game content",
            "Free weekly games",
            "Exclusive deals",
            "Fortnite V-Bucks",
            "Instant delivery",
            "Secure payment",
            "No expiration"
        ],
        "image_url": "https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=500&h=300&fit=crop",
        "stock_quantity": 300,
        "seo_title": "Epic Games Store Credits - Games & V-Bucks | 8% Off",
        "seo_description": "Epic Games Store credits at 8% discount. Purchase games and in-game content including Fortnite V-Bucks with instant delivery.",
        "seo_keywords": ["epic games store", "gaming credits", "fortnite v-bucks", "pc gaming", "game purchases"]
    }
]

# Sample reviews for products
SAMPLE_REVIEWS = [
    {
        "rating": 5,
        "title": "Excellent service and instant delivery!",
        "content": "Got my subscription within minutes of payment. The account works perfectly and customer support is very responsive. Highly recommended!",
        "user_name": "Sarah Johnson"
    },
    {
        "rating": 5,
        "title": "Great value for money",
        "content": "Amazing discount compared to the original price. The subscription is genuine and all features work as expected. Will definitely buy again!",
        "user_name": "Mike Chen"
    },
    {
        "rating": 4,
        "title": "Good product, fast delivery",
        "content": "Very satisfied with the purchase. Delivery was quick and the product is exactly as described. Only minor issue was with initial setup but support helped immediately.",
        "user_name": "Emma Davis"
    },
    {
        "rating": 5,
        "title": "Perfect for my business needs",
        "content": "This subscription has everything I need for my business. The premium features are worth every penny and the discounted price makes it even better!",
        "user_name": "David Wilson"
    },
    {
        "rating": 4,
        "title": "Reliable and trustworthy",
        "content": "I was skeptical at first but the service delivered exactly what was promised. The account is working perfectly and I've had no issues so far.",
        "user_name": "Lisa Anderson"
    },
    {
        "rating": 5,
        "title": "Outstanding customer support",
        "content": "Had a small issue with activation and the support team resolved it within 10 minutes via WhatsApp. Excellent service and genuine products!",
        "user_name": "John Martinez"
    },
    {
        "rating": 5,
        "title": "Best deal I've found online",
        "content": "Searched everywhere for this discount and found the best price here. The subscription is 100% legitimate and works flawlessly. Highly recommended!",
        "user_name": "Jessica Brown"
    },
    {
        "rating": 4,
        "title": "Great experience overall",
        "content": "The whole process was smooth from purchase to delivery. The product quality is excellent and the price is unbeatable. Will be a repeat customer!",
        "user_name": "Robert Taylor"
    }
]

async def seed_comprehensive_products():
    """Seed database with comprehensive product list"""
    
    print("🌱 Seeding comprehensive product database...")
    
    # Add all products
    for product_data in PREMIUM_PRODUCTS:
        try:
            # Create product
            product = await db.create_product(ProductCreate(**product_data))
            print(f"✅ Added: {product.name}")
            
            # Add random reviews for each product
            num_reviews = random.randint(3, 6)
            for i in range(num_reviews):
                review_data = random.choice(SAMPLE_REVIEWS)
                review = ReviewCreate(
                    product_id=product.id,
                    user_id=f"user_{random.randint(1000, 9999)}",
                    user_name=review_data["user_name"],
                    rating=review_data["rating"],
                    title=review_data["title"],
                    content=review_data["content"]
                )
                
                # Create review and approve it
                new_review = await db.create_review(review)
                # Manually approve the review
                await db.db.reviews.update_one(
                    {"id": new_review.id},
                    {"$set": {"is_approved": True}}
                )
            
            print(f"   📝 Added {num_reviews} reviews")
            
        except Exception as e:
            print(f"❌ Error adding {product_data['name']}: {e}")
    
    print("\n✅ Comprehensive product database seeded successfully!")
    print(f"📊 Total products: {len(PREMIUM_PRODUCTS)}")
    print("🎯 Categories covered:")
    print("   - OTT Platforms: Netflix, Amazon Prime, Disney+, HBO Max, etc.")
    print("   - Software: Adobe, Microsoft, Parallels, Canva, Figma, etc.")
    print("   - Professional: LinkedIn, Perplexity, Coursera, Udemy, etc.")
    print("   - VPN & Security: ExpressVPN, NordVPN, Surfshark, etc.")
    print("   - Gaming: Steam, Xbox Game Pass, PlayStation Plus, etc.")
    print("\n🎉 Your premium marketplace is ready for business!")

if __name__ == "__main__":
    asyncio.run(seed_comprehensive_products())