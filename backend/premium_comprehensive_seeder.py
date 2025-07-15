#!/usr/bin/env python3
"""
Comprehensive Premium Product Seeder
Seeds database with complete product catalog from premium subscription sites
"""

import asyncio
import uuid
from datetime import datetime
from models import Product, Review, CategoryType, ProductStatus
from database import db

def generate_uuid():
    return str(uuid.uuid4())

# Premium Product Catalog - Complete Collection
PREMIUM_PRODUCTS = [
    # OTT PLATFORMS - Indian & International
    {
        "name": "JioHotstar Premium",
        "description": "Stream unlimited content with JioHotstar Premium. Enjoy live sports, latest movies, and exclusive shows in 4K quality. Access to Disney+ content, live cricket matches, and premium originals.",
        "short_description": "Premium streaming with Disney+ content, live sports, and 4K quality",
        "category": CategoryType.OTT,
        "subcategory": "Indian OTT",
        "original_price": 1499,
        "discounted_price": 1100,
        "duration_options": ["12 months"],
        "features": [
            "Disney+ Premium Content",
            "Live Sports & Cricket",
            "4K Ultra HD Streaming",
            "Offline Download",
            "Multiple Device Support",
            "Ad-Free Experience"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0016_0-1750775538206.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 100,
        "seo_title": "JioHotstar Premium 12 Months - Disney+ Content & Live Sports",
        "seo_description": "Get JioHotstar Premium 12 months subscription with Disney+ content, live sports, and 4K streaming at discounted price.",
        "seo_keywords": ["jiohotstar", "disney+", "live sports", "4k streaming", "premium subscription"],
        "rating": 4.8,
        "total_reviews": 1247,
        "total_sales": 3456
    },
    {
        "name": "Zee5 Premium HD",
        "description": "Experience premium entertainment with Zee5 HD. Watch latest movies, web series, and live TV in high definition. Access to regional content in multiple languages.",
        "short_description": "Premium HD streaming with regional content and live TV",
        "category": CategoryType.OTT,
        "subcategory": "Indian OTT",
        "original_price": 899,
        "discounted_price": 349,
        "duration_options": ["12 months"],
        "features": [
            "HD Quality Streaming",
            "Regional Content",
            "Live TV Channels",
            "Original Web Series",
            "Multiple Languages",
            "Offline Download"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0021_0-1726517098979.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 150,
        "seo_title": "Zee5 Premium HD 12 Months - Regional Content & Live TV",
        "seo_description": "Get Zee5 Premium HD 12 months subscription with regional content and live TV at 61% discount.",
        "seo_keywords": ["zee5", "premium hd", "regional content", "live tv", "web series"],
        "rating": 4.6,
        "total_reviews": 892,
        "total_sales": 2341
    },
    {
        "name": "Zee5 Premium 4K",
        "description": "Ultimate streaming experience with Zee5 4K. Enjoy crystal clear 4K content, exclusive originals, and premium entertainment.",
        "short_description": "Ultra HD 4K streaming with exclusive content",
        "category": CategoryType.OTT,
        "subcategory": "Indian OTT",
        "original_price": 1949,
        "discounted_price": 1299,
        "duration_options": ["12 months"],
        "features": [
            "4K Ultra HD Quality",
            "Exclusive Originals",
            "Premium Content",
            "Multi-Device Support",
            "Dolby Audio",
            "Ad-Free Experience"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0022_0-1726517200283.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 75,
        "seo_title": "Zee5 Premium 4K 12 Months - Ultra HD Streaming",
        "seo_description": "Get Zee5 Premium 4K 12 months subscription with ultra HD quality and exclusive content.",
        "seo_keywords": ["zee5", "4k streaming", "ultra hd", "premium content", "exclusive originals"],
        "rating": 4.7,
        "total_reviews": 567,
        "total_sales": 1234
    },
    {
        "name": "Sony LIV Premium",
        "description": "Watch live sports, latest movies, and exclusive shows on Sony LIV Premium. Access to live cricket matches, WWE, and premium originals.",
        "short_description": "Premium streaming with live sports and exclusive content",
        "category": CategoryType.OTT,
        "subcategory": "Indian OTT",
        "original_price": 999,
        "discounted_price": 599,
        "duration_options": ["12 months"],
        "features": [
            "Live Sports & Cricket",
            "WWE Premium",
            "Latest Movies",
            "Exclusive Originals",
            "HD Quality",
            "Multiple Device Access"
        ],
        "image_url": "https://img.cdnx.in/396452/cat/401983_cat-1726859306704.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 120,
        "seo_title": "Sony LIV Premium 12 Months - Live Sports & WWE",
        "seo_description": "Get Sony LIV Premium 12 months subscription with live sports, WWE, and exclusive content at 40% discount.",
        "seo_keywords": ["sony liv", "live sports", "wwe", "cricket", "premium subscription"],
        "rating": 4.5,
        "total_reviews": 1089,
        "total_sales": 2876
    },
    {
        "name": "Netflix Premium 4K UHD",
        "description": "Stream unlimited movies and TV shows in Ultra HD 4K on Netflix Premium. Access to exclusive Netflix originals and global content library.",
        "short_description": "Ultra HD 4K streaming with Netflix originals",
        "category": CategoryType.OTT,
        "subcategory": "International OTT",
        "original_price": 649,
        "discounted_price": 399,
        "duration_options": ["1 month", "3 months", "6 months", "12 months"],
        "features": [
            "4K Ultra HD Quality",
            "Netflix Originals",
            "Multiple User Profiles",
            "Offline Download",
            "HDR Support",
            "Dolby Atmos Audio"
        ],
        "image_url": "https://logos-world.net/wp-content/uploads/2020/04/Netflix-Logo.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 200,
        "seo_title": "Netflix Premium 4K UHD - Unlimited Streaming",
        "seo_description": "Get Netflix Premium 4K UHD subscription with unlimited streaming and exclusive originals at discounted price.",
        "seo_keywords": ["netflix", "4k uhd", "premium subscription", "originals", "unlimited streaming"],
        "rating": 4.9,
        "total_reviews": 3456,
        "total_sales": 8765
    },
    {
        "name": "Amazon Prime Video",
        "description": "Stream thousands of movies and TV shows with Amazon Prime Video. Includes exclusive Amazon originals and blockbuster content.",
        "short_description": "Premium streaming with Amazon originals and blockbusters",
        "category": CategoryType.OTT,
        "subcategory": "International OTT",
        "original_price": 1499,
        "discounted_price": 999,
        "duration_options": ["12 months"],
        "features": [
            "Amazon Originals",
            "Blockbuster Movies",
            "Prime Benefits",
            "HD Quality",
            "Multiple Device Support",
            "Offline Download"
        ],
        "image_url": "https://m.media-amazon.com/images/G/01/digital/video/web/Logo-min.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 180,
        "seo_title": "Amazon Prime Video 12 Months - Originals & Blockbusters",
        "seo_description": "Get Amazon Prime Video 12 months subscription with exclusive originals and blockbuster movies.",
        "seo_keywords": ["amazon prime", "video streaming", "originals", "blockbusters", "prime benefits"],
        "rating": 4.7,
        "total_reviews": 2134,
        "total_sales": 5432
    },
    {
        "name": "Disney+ Hotstar VIP",
        "description": "Watch Disney+ content, live sports, and latest movies on Disney+ Hotstar VIP. Access to Marvel, Star Wars, and Disney originals.",
        "short_description": "Disney+ content with live sports and Marvel originals",
        "category": CategoryType.OTT,
        "subcategory": "International OTT",
        "original_price": 899,
        "discounted_price": 599,
        "duration_options": ["12 months"],
        "features": [
            "Disney+ Originals",
            "Marvel Content",
            "Star Wars",
            "Live Sports",
            "Latest Movies",
            "Kids Content"
        ],
        "image_url": "https://img.hotstar.com/image/upload/v1656431456/web-images/logo-d-plus.svg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 160,
        "seo_title": "Disney+ Hotstar VIP 12 Months - Marvel & Star Wars",
        "seo_description": "Get Disney+ Hotstar VIP 12 months subscription with Marvel, Star Wars, and Disney originals.",
        "seo_keywords": ["disney+", "hotstar", "marvel", "star wars", "disney originals"],
        "rating": 4.8,
        "total_reviews": 1876,
        "total_sales": 4321
    },
    {
        "name": "YouTube Premium",
        "description": "Ad-free YouTube experience with YouTube Premium. Download videos, background play, and access to YouTube Music.",
        "short_description": "Ad-free YouTube with downloads and background play",
        "category": CategoryType.OTT,
        "subcategory": "International OTT",
        "original_price": 129,
        "discounted_price": 89,
        "duration_options": ["1 month", "3 months", "6 months", "12 months"],
        "features": [
            "Ad-Free Experience",
            "Background Play",
            "Video Downloads",
            "YouTube Music",
            "Original Content",
            "Multiple Device Support"
        ],
        "image_url": "https://www.youtube.com/img/desktop/yt_1200.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 300,
        "seo_title": "YouTube Premium - Ad-Free & Downloads",
        "seo_description": "Get YouTube Premium subscription with ad-free experience, downloads, and YouTube Music access.",
        "seo_keywords": ["youtube premium", "ad-free", "downloads", "youtube music", "background play"],
        "rating": 4.6,
        "total_reviews": 2876,
        "total_sales": 6543
    },

    # PROFESSIONAL TOOLS
    {
        "name": "LinkedIn Business Premium",
        "description": "Accelerate your business growth with LinkedIn Business Premium. Advanced search, InMail credits, and business insights.",
        "short_description": "Advanced business tools with InMail and insights",
        "category": CategoryType.PROFESSIONAL,
        "subcategory": "Business",
        "original_price": 19949,
        "discounted_price": 3199,
        "duration_options": ["6 months"],
        "features": [
            "Advanced Search Filters",
            "InMail Credits",
            "Business Insights",
            "Who's Viewed Profile",
            "Salary Insights",
            "Lead Builder"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0019_0-1726516403347.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 50,
        "seo_title": "LinkedIn Business Premium 6 Months - Advanced Tools",
        "seo_description": "Get LinkedIn Business Premium 6 months subscription with advanced search, InMail credits, and business insights.",
        "seo_keywords": ["linkedin premium", "business", "inmail", "advanced search", "insights"],
        "rating": 4.7,
        "total_reviews": 567,
        "total_sales": 1234
    },
    {
        "name": "LinkedIn Career Premium",
        "description": "Boost your career with LinkedIn Career Premium. See who viewed your profile, get salary insights, and access premium features.",
        "short_description": "Career advancement tools with salary insights",
        "category": CategoryType.PROFESSIONAL,
        "subcategory": "Career",
        "original_price": 10099,
        "discounted_price": 1999,
        "duration_options": ["3 months"],
        "features": [
            "Who Viewed Profile",
            "Salary Insights",
            "InMail Messages",
            "Career Advice",
            "Premium Badge",
            "Advanced Search"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0023_0-1726517638813.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 75,
        "seo_title": "LinkedIn Career Premium 3 Months - Career Tools",
        "seo_description": "Get LinkedIn Career Premium 3 months subscription with career advancement tools and salary insights.",
        "seo_keywords": ["linkedin career", "premium", "salary insights", "career advice", "inmail"],
        "rating": 4.6,
        "total_reviews": 892,
        "total_sales": 2341
    },
    {
        "name": "Perplexity AI Pro",
        "description": "Unlock the power of AI with Perplexity AI Pro. Advanced AI search, unlimited queries, and premium AI models access.",
        "short_description": "Advanced AI search with unlimited queries",
        "category": CategoryType.PROFESSIONAL,
        "subcategory": "AI Tools",
        "original_price": 14999,
        "discounted_price": 999,
        "duration_options": ["12 months"],
        "features": [
            "Unlimited AI Queries",
            "Advanced AI Models",
            "Priority Support",
            "Research Tools",
            "No Rate Limits",
            "Premium Features"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0030_0-1726519411083.webp",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 100,
        "seo_title": "Perplexity AI Pro 12 Months - Advanced AI Search",
        "seo_description": "Get Perplexity AI Pro 12 months subscription with unlimited AI queries and advanced models at 93% discount.",
        "seo_keywords": ["perplexity ai", "ai search", "unlimited queries", "ai models", "research tools"],
        "rating": 4.9,
        "total_reviews": 1456,
        "total_sales": 3789
    },

    # AI TOOLS & SOFTWARE
    {
        "name": "Lovable Dev Pro",
        "description": "Professional development tools with Lovable Dev Pro. Advanced coding features, AI assistance, and premium development environment.",
        "short_description": "Advanced coding tools with AI assistance",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Development",
        "original_price": 26999,
        "discounted_price": 3499,
        "duration_options": ["12 months"],
        "features": [
            "AI Code Assistant",
            "Advanced Editor",
            "Code Completion",
            "Debug Tools",
            "Cloud Integration",
            "Premium Support"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0083_0-1750670326294.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 25,
        "seo_title": "Lovable Dev Pro 12 Months - AI Coding Assistant",
        "seo_description": "Get Lovable Dev Pro 12 months subscription with AI coding assistant and advanced development tools.",
        "seo_keywords": ["lovable dev", "ai coding", "development tools", "code assistant", "programming"],
        "rating": 4.5,
        "total_reviews": 234,
        "total_sales": 567
    },
    {
        "name": "V0.Dev Premium",
        "description": "Next-generation development platform with V0.Dev Premium. AI-powered code generation and advanced development features.",
        "short_description": "AI-powered code generation platform",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Development",
        "original_price": 19999,
        "discounted_price": 2999,
        "duration_options": ["12 months"],
        "features": [
            "AI Code Generation",
            "React Components",
            "Tailwind CSS",
            "Preview Mode",
            "Export Options",
            "Premium Templates"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0079_0-1750752280251.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 30,
        "seo_title": "V0.Dev Premium 12 Months - AI Code Generation",
        "seo_description": "Get V0.Dev Premium 12 months subscription with AI code generation and React components.",
        "seo_keywords": ["v0.dev", "ai code generation", "react components", "tailwind css", "development"],
        "rating": 4.6,
        "total_reviews": 345,
        "total_sales": 789
    },
    {
        "name": "Bolt.new Pro",
        "description": "Revolutionary development experience with Bolt.new Pro. Full-stack development in the browser with AI assistance.",
        "short_description": "Full-stack development in browser with AI",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Development",
        "original_price": 17999,
        "discounted_price": 1999,
        "duration_options": ["12 months"],
        "features": [
            "Browser-based IDE",
            "AI Code Assistant",
            "Full-stack Support",
            "Live Preview",
            "Cloud Deployment",
            "Collaboration Tools"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0077_0-1750752548237.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 40,
        "seo_title": "Bolt.new Pro 12 Months - Browser IDE with AI",
        "seo_description": "Get Bolt.new Pro 12 months subscription with browser-based IDE and AI code assistant.",
        "seo_keywords": ["bolt.new", "browser ide", "ai assistant", "full-stack", "development"],
        "rating": 4.4,
        "total_reviews": 456,
        "total_sales": 1023
    },
    {
        "name": "Blackbox AI Business Plan",
        "description": "Enterprise-grade AI coding assistant with Blackbox AI. Advanced code generation, debugging, and optimization tools.",
        "short_description": "Enterprise AI coding assistant",
        "category": CategoryType.SOFTWARE,
        "subcategory": "AI Tools",
        "original_price": 29999,
        "discounted_price": 299,
        "duration_options": ["3 months"],
        "features": [
            "AI Code Generation",
            "Advanced Debugging",
            "Code Optimization",
            "Multiple Languages",
            "Enterprise Support",
            "Team Collaboration"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0057_0-1750752797237.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 60,
        "seo_title": "Blackbox AI Business Plan 3 Months - Enterprise AI",
        "seo_description": "Get Blackbox AI Business Plan 3 months subscription with enterprise-grade AI coding assistant.",
        "seo_keywords": ["blackbox ai", "enterprise ai", "code generation", "debugging", "optimization"],
        "rating": 4.7,
        "total_reviews": 678,
        "total_sales": 1456
    },

    # PRODUCTIVITY TOOLS
    {
        "name": "QuillBot Premium",
        "description": "Advanced writing assistant with QuillBot Premium. Paraphrasing, grammar checking, and writing enhancement tools.",
        "short_description": "Advanced writing assistant and paraphrasing tool",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Writing",
        "original_price": 849,
        "discounted_price": 99,
        "duration_options": ["1 month"],
        "features": [
            "Advanced Paraphrasing",
            "Grammar Checker",
            "Plagiarism Detection",
            "Word Flipper",
            "Summarizer",
            "Citation Generator"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0055_0-1750775150278.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 200,
        "seo_title": "QuillBot Premium 1 Month - Writing Assistant",
        "seo_description": "Get QuillBot Premium 1 month subscription with advanced paraphrasing and grammar checking tools.",
        "seo_keywords": ["quillbot", "writing assistant", "paraphrasing", "grammar checker", "plagiarism"],
        "rating": 4.6,
        "total_reviews": 1234,
        "total_sales": 3456
    },
    {
        "name": "Rezi AI Subscription",
        "description": "AI-powered resume builder with Rezi AI. Create professional resumes with AI assistance and ATS optimization.",
        "short_description": "AI-powered resume builder with ATS optimization",
        "category": CategoryType.PROFESSIONAL,
        "subcategory": "Career",
        "original_price": 11999,
        "discounted_price": 999,
        "duration_options": ["12 months"],
        "features": [
            "AI Resume Builder",
            "ATS Optimization",
            "Multiple Templates",
            "Cover Letter Generator",
            "Interview Prep",
            "Career Insights"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0084_0-1751371083712.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 80,
        "seo_title": "Rezi AI Subscription 12 Months - Resume Builder",
        "seo_description": "Get Rezi AI Subscription 12 months with AI-powered resume builder and ATS optimization.",
        "seo_keywords": ["rezi ai", "resume builder", "ats optimization", "ai resume", "career tools"],
        "rating": 4.5,
        "total_reviews": 567,
        "total_sales": 1234
    },
    {
        "name": "Granola AI Pro",
        "description": "Smart meeting assistant with Granola AI Pro. AI-powered meeting transcription, note-taking, and insights.",
        "short_description": "AI meeting assistant with transcription and insights",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Productivity",
        "original_price": 19999,
        "discounted_price": 1499,
        "duration_options": ["12 months"],
        "features": [
            "AI Transcription",
            "Meeting Notes",
            "Action Items",
            "Insights Analytics",
            "Integration Tools",
            "Team Collaboration"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0081_0-1750751669380.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 45,
        "seo_title": "Granola AI Pro 12 Months - Meeting Assistant",
        "seo_description": "Get Granola AI Pro 12 months subscription with AI meeting assistant and transcription tools.",
        "seo_keywords": ["granola ai", "meeting assistant", "transcription", "notes", "ai insights"],
        "rating": 4.4,
        "total_reviews": 345,
        "total_sales": 678
    },
    {
        "name": "Linear Business Plan",
        "description": "Modern issue tracking with Linear Business Plan. Advanced project management, workflows, and team collaboration.",
        "short_description": "Modern issue tracking and project management",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Project Management",
        "original_price": 19999,
        "discounted_price": 1499,
        "duration_options": ["12 months"],
        "features": [
            "Issue Tracking",
            "Project Management",
            "Team Workflows",
            "Advanced Analytics",
            "Integration Tools",
            "Custom Fields"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0080_0-1750752137339.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 35,
        "seo_title": "Linear Business Plan 12 Months - Issue Tracking",
        "seo_description": "Get Linear Business Plan 12 months subscription with modern issue tracking and project management.",
        "seo_keywords": ["linear", "issue tracking", "project management", "workflows", "team collaboration"],
        "rating": 4.6,
        "total_reviews": 456,
        "total_sales": 891
    },
    {
        "name": "Superhuman AI Starter Plan",
        "description": "The fastest email experience with Superhuman AI. AI-powered email management, shortcuts, and productivity features.",
        "short_description": "AI-powered email management and productivity",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Email",
        "original_price": 19999,
        "discounted_price": 1499,
        "duration_options": ["12 months"],
        "features": [
            "AI Email Assistant",
            "Keyboard Shortcuts",
            "Email Scheduling",
            "Read Receipts",
            "Snippets",
            "Advanced Search"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0082_0-1750698669179.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": False,
        "stock_quantity": 50,
        "seo_title": "Superhuman AI Starter Plan 12 Months - Email AI",
        "seo_description": "Get Superhuman AI Starter Plan 12 months subscription with AI-powered email management.",
        "seo_keywords": ["superhuman", "ai email", "email management", "productivity", "shortcuts"],
        "rating": 4.7,
        "total_reviews": 678,
        "total_sales": 1234
    },
    {
        "name": "Beautiful.ai Pro",
        "description": "Create stunning presentations with Beautiful.ai Pro. AI-powered design, templates, and collaboration features.",
        "short_description": "AI-powered presentation design tool",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Design",
        "original_price": 2399,
        "discounted_price": 499,
        "duration_options": ["12 months"],
        "features": [
            "AI Design Assistant",
            "Smart Templates",
            "Brand Kit",
            "Collaboration Tools",
            "Export Options",
            "Analytics"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0053_0-1734791060061.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 90,
        "seo_title": "Beautiful.ai Pro 12 Months - AI Presentations",
        "seo_description": "Get Beautiful.ai Pro 12 months subscription with AI-powered presentation design and templates.",
        "seo_keywords": ["beautiful.ai", "ai presentations", "design tool", "templates", "collaboration"],
        "rating": 4.5,
        "total_reviews": 789,
        "total_sales": 1567
    },

    # CLOUD STORAGE & SERVICES
    {
        "name": "Google One",
        "description": "Expand your Google storage with Google One. Cloud storage, automatic backups, and premium features across Google services.",
        "short_description": "Google cloud storage with premium features",
        "category": CategoryType.SOFTWARE,
        "subcategory": "Cloud Storage",
        "original_price": 780,
        "discounted_price": 299,
        "duration_options": ["6 months"],
        "features": [
            "100GB+ Storage",
            "Automatic Backup",
            "Family Sharing",
            "Premium Support",
            "Advanced Security",
            "Google Photos Benefits"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0076_0-1750752671797.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 150,
        "seo_title": "Google One 6 Months - Cloud Storage & Premium Features",
        "seo_description": "Get Google One 6 months subscription with expanded cloud storage and premium Google services.",
        "seo_keywords": ["google one", "cloud storage", "google drive", "backup", "family sharing"],
        "rating": 4.6,
        "total_reviews": 1234,
        "total_sales": 2890
    },

    # EDUCATIONAL PLATFORMS
    {
        "name": "EdX Official Subscription",
        "description": "Learn from top universities with EdX Official Subscription. Access to verified certificates, unlimited courses, and premium content.",
        "short_description": "University courses with verified certificates",
        "category": CategoryType.EDUCATION,
        "subcategory": "Online Learning",
        "original_price": 29999,
        "discounted_price": 499,
        "duration_options": ["12 months"],
        "features": [
            "Verified Certificates",
            "Unlimited Courses",
            "University Content",
            "Expert Instructors",
            "Career Services",
            "Professional Development"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0056_0-1747490293455.jpg",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 70,
        "seo_title": "EdX Official Subscription 12 Months - University Courses",
        "seo_description": "Get EdX Official Subscription 12 months with unlimited university courses and verified certificates.",
        "seo_keywords": ["edx", "university courses", "verified certificates", "online learning", "education"],
        "rating": 4.8,
        "total_reviews": 1567,
        "total_sales": 3456
    },

    # DATING & SOCIAL
    {
        "name": "Tinder Gold",
        "description": "Premium dating experience with Tinder Gold. See who likes you, unlimited likes, and premium features.",
        "short_description": "Premium dating with unlimited likes and features",
        "category": CategoryType.SOCIAL_MEDIA,
        "subcategory": "Dating",
        "original_price": 899,
        "discounted_price": 399,
        "duration_options": ["1 month"],
        "features": [
            "See Who Likes You",
            "Unlimited Likes",
            "Super Likes",
            "Boost Feature",
            "Passport",
            "Rewind Feature"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0017_0-1749893135829.webp",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 120,
        "seo_title": "Tinder Gold 1 Month - Premium Dating Features",
        "seo_description": "Get Tinder Gold 1 month subscription with premium dating features and unlimited likes.",
        "seo_keywords": ["tinder gold", "premium dating", "unlimited likes", "dating app", "social"],
        "rating": 4.2,
        "total_reviews": 2345,
        "total_sales": 5678
    },
    {
        "name": "Tinder Plus",
        "description": "Enhanced dating experience with Tinder Plus. Unlimited likes, rewind, and passport features.",
        "short_description": "Enhanced dating with unlimited likes and passport",
        "category": CategoryType.SOCIAL_MEDIA,
        "subcategory": "Dating",
        "original_price": 199,
        "discounted_price": 99,
        "duration_options": ["1 month"],
        "features": [
            "Unlimited Likes",
            "Rewind Feature",
            "Passport",
            "Super Likes",
            "Boost",
            "Hide Age"
        ],
        "image_url": "https://img.cdnx.in/396452/SKU-0074_0-1749897412251.webp",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 140,
        "seo_title": "Tinder Plus 1 Month - Enhanced Dating Features",
        "seo_description": "Get Tinder Plus 1 month subscription with enhanced dating features and unlimited likes.",
        "seo_keywords": ["tinder plus", "enhanced dating", "unlimited likes", "passport", "dating app"],
        "rating": 4.1,
        "total_reviews": 1890,
        "total_sales": 4567
    },

    # MUSIC STREAMING
    {
        "name": "Spotify Premium",
        "description": "Premium music streaming with Spotify Premium. Ad-free music, offline downloads, and high-quality audio.",
        "short_description": "Ad-free music streaming with offline downloads",
        "category": CategoryType.OTT,
        "subcategory": "Music",
        "original_price": 119,
        "discounted_price": 79,
        "duration_options": ["1 month", "3 months", "6 months", "12 months"],
        "features": [
            "Ad-Free Music",
            "Offline Downloads",
            "High Quality Audio",
            "Unlimited Skips",
            "Podcast Access",
            "Multiple Device Support"
        ],
        "image_url": "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 250,
        "seo_title": "Spotify Premium - Ad-Free Music & Downloads",
        "seo_description": "Get Spotify Premium subscription with ad-free music streaming and offline downloads.",
        "seo_keywords": ["spotify premium", "ad-free music", "offline downloads", "music streaming", "high quality"],
        "rating": 4.8,
        "total_reviews": 4567,
        "total_sales": 9876
    },
    {
        "name": "Apple Music",
        "description": "Premium music streaming with Apple Music. Access to millions of songs, exclusive content, and spatial audio.",
        "short_description": "Premium music streaming with spatial audio",
        "category": CategoryType.OTT,
        "subcategory": "Music",
        "original_price": 99,
        "discounted_price": 69,
        "duration_options": ["1 month", "3 months", "6 months", "12 months"],
        "features": [
            "Millions of Songs",
            "Spatial Audio",
            "Exclusive Content",
            "Offline Downloads",
            "Lossless Audio",
            "Apple Integration"
        ],
        "image_url": "https://www.apple.com/apple-music/",
        "gallery_images": [],
        "is_featured": True,
        "is_bestseller": True,
        "stock_quantity": 200,
        "seo_title": "Apple Music - Premium Streaming & Spatial Audio",
        "seo_description": "Get Apple Music subscription with premium streaming, spatial audio, and exclusive content.",
        "seo_keywords": ["apple music", "premium music", "spatial audio", "exclusive content", "lossless"],
        "rating": 4.7,
        "total_reviews": 3456,
        "total_sales": 7890
    }
]

# Generate comprehensive reviews for each product
def generate_reviews(product_id, product_name, rating, num_reviews):
    reviews = []
    review_templates = [
        {
            "title": "Excellent service!",
            "content": f"{product_name} exceeded my expectations. Fast delivery and genuine subscription. Highly recommend!"
        },
        {
            "title": "Amazing value for money!",
            "content": f"{product_name} is working perfectly and the setup was instant. Great deal!"
        },
        {
            "title": "Great quality subscription",
            "content": f"Perfect experience with {product_name}. Professional seller and authentic product."
        },
        {
            "title": "Perfect experience!",
            "content": f"{product_name} delivered immediately and works exactly as described. Outstanding!"
        },
        {
            "title": "Outstanding service!",
            "content": f"{product_name} subscription is authentic and the price is unbeatable. Fantastic!"
        },
        {
            "title": "Fantastic deal!",
            "content": f"Quick delivery and excellent customer support for {product_name}. Superb quality!"
        },
        {
            "title": "Superb quality!",
            "content": f"The {product_name} subscription is genuine and works flawlessly. Incredible value!"
        },
        {
            "title": "Incredible value!",
            "content": f"{product_name} is working great and the service was professional. Top-notch!"
        },
        {
            "title": "Top-notch service!",
            "content": f"Fast, reliable, and exactly what I needed with {product_name}. Excellent purchase!"
        },
        {
            "title": "Excellent purchase!",
            "content": f"{product_name} delivered instantly and quality is premium. Highly satisfied!"
        }
    ]
    
    # Generate user names
    user_names = [
        "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Neha Singh", "Vikram Gupta",
        "Anjali Verma", "Rohit Jain", "Kavya Reddy", "Arjun Mehta", "Sonia Agarwal",
        "Rahul Singh", "Divya Sharma", "Karan Patel", "Riya Gupta", "Suresh Kumar"
    ]
    
    # Create reviews
    for i in range(min(num_reviews, len(review_templates))):
        template = review_templates[i]
        user_name = user_names[i % len(user_names)]
        
        # Convert float rating to int
        int_rating = int(rating)
        
        reviews.append(Review(
            id=generate_uuid(),
            product_id=product_id,
            user_id=generate_uuid(),
            user_name=user_name,
            rating=int_rating,
            title=template["title"],
            content=template["content"],
            is_verified=True,
            is_approved=True,
            created_at=datetime.utcnow()
        ))
    
    return reviews

async def seed_comprehensive_products():
    print("🚀 Starting comprehensive premium product seeding...")
    
    # Clear existing products
    await db.db.products.delete_many({})
    await db.db.reviews.delete_many({})
    
    total_products = 0
    categories_seeded = set()
    
    for product_data in PREMIUM_PRODUCTS:
        try:
            # Generate slug
            slug = product_data["name"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-")
            
            # Calculate discount percentage
            discount_percentage = int(((product_data["original_price"] - product_data["discounted_price"]) / product_data["original_price"]) * 100)
            
            # Create product
            product = Product(
                id=generate_uuid(),
                slug=slug,
                discount_percentage=discount_percentage,
                status=ProductStatus.ACTIVE,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                **product_data
            )
            
            # Insert product
            await db.db.products.insert_one(product.dict())
            
            # Generate and insert reviews
            reviews = generate_reviews(product_data["name"], product_data["rating"], product_data["total_reviews"])
            for review in reviews:
                await db.db.reviews.insert_one(review.dict())
            
            print(f"✅ Added: {product_data['name']}")
            print(f"   💰 Price: ₹{product_data['discounted_price']} (was ₹{product_data['original_price']})")
            print(f"   📊 Rating: {product_data['rating']}/5 ({product_data['total_reviews']} reviews)")
            print(f"   📦 Stock: {product_data['stock_quantity']}")
            print()
            
            total_products += 1
            categories_seeded.add(product_data["category"])
            
        except Exception as e:
            print(f"❌ Error adding {product_data['name']}: {e}")
            continue
    
    print(f"✅ Comprehensive seeding complete!")
    print(f"📊 Total products added: {total_products}")
    print(f"🏷️  Categories seeded: {', '.join(categories_seeded)}")
    print(f"🎯 Featured products: {len([p for p in PREMIUM_PRODUCTS if p['is_featured']])}")
    print(f"🏆 Bestsellers: {len([p for p in PREMIUM_PRODUCTS if p['is_bestseller']])}")
    print()
    print("🎉 Premium product database is ready for business!")

if __name__ == "__main__":
    asyncio.run(seed_comprehensive_products())