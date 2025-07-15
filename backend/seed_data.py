import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db
from models import *

async def seed_database():
    """Seed the database with sample data"""
    
    print("🌱 Seeding database with sample data...")
    
    # Sample Categories
    categories = [
        CategoryCreate(
            name="OTT Platforms",
            description="Premium streaming subscriptions at discounted prices",
            icon="📺",
            image_url="https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop",
            seo_title="OTT Platform Subscriptions - Netflix, Amazon Prime, Disney+",
            seo_description="Get premium OTT subscriptions at up to 70% off. Netflix, Amazon Prime, Disney+, and more streaming services at discounted rates."
        ),
        CategoryCreate(
            name="Software & Tools",
            description="Professional software and creative tools",
            icon="💻",
            image_url="https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=500&h=300&fit=crop",
            seo_title="Software Subscriptions - Adobe, Microsoft Office, Canva Pro",
            seo_description="Premium software subscriptions for professionals. Adobe Creative Cloud, Microsoft Office, Canva Pro at unbeatable prices."
        ),
        CategoryCreate(
            name="VPN & Security",
            description="Secure browsing and privacy protection",
            icon="🔒",
            image_url="https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop",
            seo_title="VPN Subscriptions - ExpressVPN, NordVPN, CyberGhost",
            seo_description="Premium VPN services for secure browsing. ExpressVPN, NordVPN, CyberGhost at discounted rates."
        ),
        CategoryCreate(
            name="Professional Development",
            description="Career advancement and skill development",
            icon="🎓",
            image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&h=300&fit=crop",
            seo_title="Professional Development - LinkedIn Premium, Coursera, Udemy",
            seo_description="Advance your career with discounted professional development subscriptions. LinkedIn Premium, Coursera Plus, Udemy courses."
        ),
        CategoryCreate(
            name="Gaming & Entertainment",
            description="Gaming platforms and entertainment subscriptions",
            icon="🎮",
            image_url="https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=500&h=300&fit=crop",
            seo_title="Gaming Subscriptions - Steam, Xbox Game Pass, PlayStation Plus",
            seo_description="Premium gaming subscriptions at discounted prices. Steam, Xbox Game Pass, PlayStation Plus, and more gaming platforms."
        )
    ]
    
    for category in categories:
        await db.create_category(category)
    
    # Sample Products
    products = [
        # OTT Products
        ProductCreate(
            name="Netflix Premium 4K UHD",
            description="Enjoy unlimited streaming of movies, TV shows, and documentaries in stunning 4K quality. Share with up to 4 family members. Watch on any device - Smart TV, laptop, phone, or tablet. Access to exclusive Netflix Originals and latest releases.",
            short_description="Premium Netflix subscription with 4K streaming and 4 screens",
            category=CategoryType.OTT,
            subcategory="Streaming",
            original_price=649.0,
            discounted_price=199.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "4K Ultra HD streaming",
                "4 simultaneous screens",
                "Unlimited downloads",
                "No ads",
                "Access to Netflix Originals",
                "Works on all devices"
            ],
            image_url="https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=500&h=300&fit=crop",
            gallery_images=[
                "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&h=600&fit=crop",
                "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=800&h=600&fit=crop"
            ],
            is_featured=True,
            is_bestseller=True,
            stock_quantity=100,
            seo_title="Netflix Premium 4K Subscription - 70% Off | Premium Subscriptions",
            seo_description="Get Netflix Premium 4K subscription at 70% off. Unlimited streaming, 4 screens, no ads. Instant delivery via WhatsApp.",
            seo_keywords=["netflix premium", "netflix 4k", "netflix subscription", "streaming service", "netflix discount"]
        ),
        ProductCreate(
            name="Amazon Prime Video",
            description="Stream thousands of movies, TV shows, and award-winning Amazon Originals. Get access to exclusive content, early releases, and ad-free viewing. Perfect for movie nights and binge-watching.",
            short_description="Amazon Prime Video streaming with exclusive content",
            category=CategoryType.OTT,
            subcategory="Streaming",
            original_price=499.0,
            discounted_price=149.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "Unlimited streaming",
                "Amazon Originals",
                "Download for offline viewing",
                "Multiple device support",
                "HD quality streaming",
                "No ads"
            ],
            image_url="https://images.unsplash.com/photo-1489599510843-b4c9e1b5ef10?w=500&h=300&fit=crop",
            is_featured=True,
            stock_quantity=150,
            seo_title="Amazon Prime Video Subscription - 70% Off | Stream Movies & TV Shows",
            seo_description="Amazon Prime Video subscription at 70% discount. Watch exclusive content, movies, and TV shows. Instant account delivery.",
            seo_keywords=["amazon prime video", "prime video subscription", "streaming service", "amazon originals", "movies online"]
        ),
        ProductCreate(
            name="Disney+ Premium",
            description="Watch Disney, Pixar, Marvel, Star Wars, and National Geographic content. Perfect for families with kids. Enjoy classic Disney movies, latest Marvel series, and exclusive content.",
            short_description="Disney+ subscription with Marvel, Star Wars, and Disney content",
            category=CategoryType.OTT,
            subcategory="Streaming",
            original_price=799.0,
            discounted_price=249.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "Disney, Pixar, Marvel content",
                "Star Wars universe",
                "National Geographic",
                "4K and HDR streaming",
                "Download for offline viewing",
                "Multiple profiles"
            ],
            image_url="https://images.unsplash.com/photo-1543536448-d209d2d13a1c?w=500&h=300&fit=crop",
            is_bestseller=True,
            stock_quantity=80,
            seo_title="Disney+ Premium Subscription - Marvel, Star Wars & Disney Movies",
            seo_description="Disney+ subscription with Marvel, Star Wars, and Disney content. Perfect for families. 4K streaming at discounted prices.",
            seo_keywords=["disney plus", "disney+ subscription", "marvel movies", "star wars", "disney movies", "family streaming"]
        ),
        
        # Software Products
        ProductCreate(
            name="Adobe Creative Cloud All Apps",
            description="Complete creative suite with Photoshop, Illustrator, Premiere Pro, After Effects, and 20+ creative apps. Perfect for designers, photographers, and video editors. Includes cloud storage and premium fonts.",
            short_description="Complete Adobe Creative Cloud suite with all applications",
            category=CategoryType.SOFTWARE,
            subcategory="Design",
            original_price=4999.0,
            discounted_price=1299.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "20+ Creative Apps",
                "Photoshop, Illustrator, Premiere Pro",
                "100GB cloud storage",
                "Premium fonts",
                "Stock photos and videos",
                "Mobile apps included"
            ],
            image_url="https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=500&h=300&fit=crop",
            is_featured=True,
            stock_quantity=50,
            seo_title="Adobe Creative Cloud All Apps - 74% Off | Photoshop, Illustrator, Premiere Pro",
            seo_description="Adobe Creative Cloud complete suite at 74% discount. Photoshop, Illustrator, Premiere Pro, and 20+ apps. Professional creative tools.",
            seo_keywords=["adobe creative cloud", "photoshop", "illustrator", "premiere pro", "design software", "video editing"]
        ),
        ProductCreate(
            name="Microsoft Office 365 Personal",
            description="Complete Microsoft Office suite with Word, Excel, PowerPoint, Outlook, and 1TB OneDrive storage. Perfect for students and professionals. Access on multiple devices.",
            short_description="Microsoft Office 365 with Word, Excel, PowerPoint, and 1TB storage",
            category=CategoryType.SOFTWARE,
            subcategory="Productivity",
            original_price=2499.0,
            discounted_price=599.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "Word, Excel, PowerPoint",
                "1TB OneDrive storage",
                "Outlook email",
                "Works on 5 devices",
                "Premium templates",
                "24/7 support"
            ],
            image_url="https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500&h=300&fit=crop",
            is_bestseller=True,
            stock_quantity=120,
            seo_title="Microsoft Office 365 Personal - 76% Off | Word, Excel, PowerPoint",
            seo_description="Microsoft Office 365 Personal at 76% discount. Word, Excel, PowerPoint, and 1TB OneDrive storage. Perfect for productivity.",
            seo_keywords=["microsoft office 365", "ms office", "word excel powerpoint", "productivity software", "office suite"]
        ),
        ProductCreate(
            name="Canva Pro",
            description="Professional design tool with premium templates, stock photos, and advanced features. Perfect for social media, marketing, and business designs. Create stunning graphics effortlessly.",
            short_description="Canva Pro with premium templates and design tools",
            category=CategoryType.SOFTWARE,
            subcategory="Design",
            original_price=1499.0,
            discounted_price=399.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "100,000+ premium templates",
                "Millions of stock photos",
                "Brand kit and fonts",
                "Background remover",
                "Resize designs instantly",
                "Team collaboration"
            ],
            image_url="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500&h=300&fit=crop",
            is_featured=True,
            stock_quantity=200,
            seo_title="Canva Pro Subscription - 73% Off | Premium Design Templates",
            seo_description="Canva Pro subscription at 73% discount. Access premium templates, stock photos, and professional design tools. Perfect for businesses.",
            seo_keywords=["canva pro", "design tool", "graphic design", "social media design", "business graphics", "templates"]
        ),
        
        # VPN Products
        ProductCreate(
            name="ExpressVPN Premium",
            description="Ultra-fast VPN with military-grade encryption. Access blocked content, protect your privacy, and browse anonymously. Works on all devices with 24/7 customer support.",
            short_description="Premium VPN service with military-grade encryption",
            category=CategoryType.VPN,
            subcategory="Security",
            original_price=999.0,
            discounted_price=299.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "Military-grade encryption",
                "3000+ servers worldwide",
                "No-logs policy",
                "24/7 customer support",
                "Works on 5 devices",
                "Money-back guarantee"
            ],
            image_url="https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop",
            is_bestseller=True,
            stock_quantity=80,
            seo_title="ExpressVPN Premium - 70% Off | Ultra-Fast VPN Service",
            seo_description="ExpressVPN Premium at 70% discount. Ultra-fast VPN with military-grade encryption. 3000+ servers, no-logs policy.",
            seo_keywords=["expressvpn", "vpn service", "online privacy", "secure browsing", "vpn subscription", "internet security"]
        ),
        ProductCreate(
            name="NordVPN Premium",
            description="Advanced VPN with double encryption and threat protection. Access geo-restricted content and browse securely. Includes password manager and file encryption.",
            short_description="Advanced VPN with double encryption and threat protection",
            category=CategoryType.VPN,
            subcategory="Security",
            original_price=799.0,
            discounted_price=249.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "Double VPN encryption",
                "Threat protection",
                "5200+ servers",
                "Password manager",
                "File encryption",
                "6 devices simultaneously"
            ],
            image_url="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=500&h=300&fit=crop",
            stock_quantity=100,
            seo_title="NordVPN Premium - 69% Off | Double VPN Encryption",
            seo_description="NordVPN Premium at 69% discount. Double VPN encryption, threat protection, and 5200+ servers. Advanced security features.",
            seo_keywords=["nordvpn", "vpn service", "double encryption", "threat protection", "secure vpn", "online security"]
        ),
        
        # Professional Development
        ProductCreate(
            name="LinkedIn Premium Career",
            description="Advanced LinkedIn features for career growth. See who viewed your profile, get insights on job applications, and access exclusive career advice. Perfect for job seekers and professionals.",
            short_description="LinkedIn Premium with career insights and job search tools",
            category=CategoryType.PROFESSIONAL,
            subcategory="Career",
            original_price=1999.0,
            discounted_price=599.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "See who viewed your profile",
                "InMail credits",
                "Job insights",
                "Salary insights",
                "Online courses",
                "Applicant insights"
            ],
            image_url="https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=500&h=300&fit=crop",
            is_featured=True,
            stock_quantity=90,
            seo_title="LinkedIn Premium Career - 70% Off | Professional Networking",
            seo_description="LinkedIn Premium Career at 70% discount. Advanced features for career growth, job insights, and professional networking.",
            seo_keywords=["linkedin premium", "career development", "job search", "professional networking", "linkedin career", "job insights"]
        ),
        ProductCreate(
            name="Coursera Plus",
            description="Unlimited access to 7,000+ courses from top universities and companies. Get certificates, specializations, and professional degrees. Perfect for skill development and career advancement.",
            short_description="Unlimited access to 7,000+ courses and certificates",
            category=CategoryType.PROFESSIONAL,
            subcategory="Education",
            original_price=3999.0,
            discounted_price=1499.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "7,000+ courses",
                "University certificates",
                "Professional certificates",
                "Specializations",
                "Unlimited access",
                "Mobile app"
            ],
            image_url="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500&h=300&fit=crop",
            is_bestseller=True,
            stock_quantity=70,
            seo_title="Coursera Plus - 63% Off | Unlimited Access to 7,000+ Courses",
            seo_description="Coursera Plus at 63% discount. Unlimited access to 7,000+ courses from top universities. Professional certificates and specializations.",
            seo_keywords=["coursera plus", "online courses", "certificates", "skill development", "professional development", "university courses"]
        ),
        
        # Gaming Products
        ProductCreate(
            name="Steam Wallet Credits",
            description="Add funds to your Steam account to purchase games, DLC, and in-game items. Instant delivery and works worldwide. Perfect for gamers who want to save on Steam purchases.",
            short_description="Steam Wallet credits for game purchases",
            category=CategoryType.GAMING,
            subcategory="Gaming",
            original_price=1000.0,
            discounted_price=799.0,
            duration_options=["₹500", "₹1000", "₹2000", "₹5000"],
            features=[
                "Instant delivery",
                "Works worldwide",
                "No expiration",
                "Buy games and DLC",
                "In-game purchases",
                "Secure transactions"
            ],
            image_url="https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=500&h=300&fit=crop",
            stock_quantity=500,
            seo_title="Steam Wallet Credits - 20% Off | Instant Delivery",
            seo_description="Steam Wallet credits at 20% discount. Instant delivery, works worldwide. Perfect for purchasing games and DLC on Steam.",
            seo_keywords=["steam wallet", "steam credits", "gaming", "steam games", "game purchases", "steam discount"]
        ),
        ProductCreate(
            name="Spotify Premium",
            description="Ad-free music streaming with offline downloads. Access 70+ million songs, podcasts, and playlists. High-quality audio and unlimited skips. Perfect for music lovers.",
            short_description="Ad-free music streaming with offline downloads",
            category=CategoryType.OTT,
            subcategory="Music",
            original_price=399.0,
            discounted_price=99.0,
            duration_options=["1 month", "3 months", "6 months", "1 year"],
            features=[
                "Ad-free listening",
                "Offline downloads",
                "High-quality audio",
                "Unlimited skips",
                "70+ million songs",
                "Podcasts included"
            ],
            image_url="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500&h=300&fit=crop",
            is_bestseller=True,
            stock_quantity=300,
            seo_title="Spotify Premium - 75% Off | Ad-Free Music Streaming",
            seo_description="Spotify Premium at 75% discount. Ad-free music streaming, offline downloads, and high-quality audio. 70+ million songs.",
            seo_keywords=["spotify premium", "music streaming", "offline music", "ad-free music", "spotify subscription", "music app"]
        )
    ]
    
    for product in products:
        await db.create_product(product)
    
    # Sample Blog Posts
    blog_posts = [
        BlogPostCreate(
            title="Top 10 OTT Platforms to Watch in 2025",
            content="""
            # Top 10 OTT Platforms to Watch in 2025

            The streaming industry continues to evolve rapidly, with new platforms emerging and existing ones enhancing their offerings. Here are the top OTT platforms that are dominating the market in 2025.

            ## 1. Netflix - The Global Leader

            Netflix remains the undisputed leader in the streaming space with over 250 million subscribers worldwide. Their investment in original content has paid off tremendously, with hits like "Stranger Things," "The Crown," and numerous international series.

            **Why Netflix Leads:**
            - Massive content library
            - Strong original programming
            - Global availability
            - Advanced recommendation algorithm
            - Multiple subscription tiers

            ## 2. Amazon Prime Video - The Complete Package

            Amazon Prime Video offers more than just streaming. It's part of the larger Amazon Prime ecosystem, providing value through multiple services.

            **Key Features:**
            - Included with Amazon Prime membership
            - Free shipping on Amazon orders
            - Prime Music included
            - Exclusive Amazon Originals
            - Sports content through Prime Video Sports

            ## 3. Disney+ - Family Entertainment King

            Disney+ has captured the family entertainment market with its extensive catalog of Disney, Pixar, Marvel, Star Wars, and National Geographic content.

            **What Makes Disney+ Special:**
            - Unmatched family content
            - Marvel Cinematic Universe
            - Star Wars universe
            - High-quality 4K content
            - Affordable pricing

            ## 4. Apple TV+ - Quality Over Quantity

            Apple TV+ focuses on high-quality original content rather than a massive library. Their strategy of fewer, better shows has been successful.

            **Apple TV+ Advantages:**
            - Premium original content
            - High production values
            - Integration with Apple ecosystem
            - Affordable pricing
            - No ads

            ## 5. HBO Max - Premium Content

            HBO Max (now Max) continues to be the go-to platform for premium, adult-oriented content and blockbuster movies.

            **HBO Max Strengths:**
            - Premium HBO content
            - Warner Bros. movies
            - DC superhero content
            - Adult-oriented programming
            - Same-day movie releases

            ## Conclusion

            The OTT landscape in 2025 is more competitive than ever. Each platform offers unique value propositions, and the best choice depends on your viewing preferences and budget. Many users find value in subscribing to multiple platforms, especially with the discounted rates available through premium subscription shops.

            ## Getting Started

            If you're looking to subscribe to any of these platforms at discounted rates, check out our [premium subscription deals](/products) where you can save up to 70% on your favorite streaming services.
            """,
            excerpt="Discover the top OTT platforms dominating 2025 with their unique features, content libraries, and what makes them worth subscribing to.",
            author="Tech Editorial Team",
            featured_image="https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=800&h=400&fit=crop",
            category="Streaming",
            tags=["OTT", "Streaming", "Netflix", "Amazon Prime", "Disney+", "2025"],
            is_published=True,
            is_featured=True,
            seo_title="Top 10 OTT Platforms 2025 - Complete Guide to Streaming Services",
            seo_description="Discover the best OTT platforms in 2025. Compare Netflix, Amazon Prime, Disney+, Apple TV+, and more. Find the perfect streaming service for your needs.",
            seo_keywords=["OTT platforms 2025", "streaming services", "Netflix vs Amazon Prime", "best streaming platforms", "OTT comparison"]
        ),
        BlogPostCreate(
            title="How to Save Money on Software Subscriptions",
            content="""
            # How to Save Money on Software Subscriptions

            Software subscriptions can quickly add up, especially for professionals and businesses. Here are proven strategies to reduce your software costs without compromising on functionality.

            ## 1. Bundle Subscriptions

            Many software companies offer bundle deals that provide significant savings compared to individual subscriptions.

            **Popular Bundles:**
            - Adobe Creative Cloud (20+ apps)
            - Microsoft 365 (Office + OneDrive + Teams)
            - Google Workspace (Gmail + Drive + Docs)

            ## 2. Annual vs Monthly Payments

            Most software companies offer substantial discounts for annual subscriptions compared to monthly payments.

            **Typical Savings:**
            - Adobe Creative Cloud: 16% annual discount
            - Microsoft 365: 15% annual discount
            - Canva Pro: 20% annual discount

            ## 3. Student and Educational Discounts

            Many software companies offer significant discounts for students and educators.

            **Educational Discounts Available:**
            - Adobe Creative Cloud: 60% off for students
            - Microsoft 365: Free for students
            - Canva Pro: Free for educators

            ## 4. Free Alternatives

            Consider free alternatives that might meet your needs:

            **Free Software Options:**
            - GIMP (Photoshop alternative)
            - LibreOffice (Microsoft Office alternative)
            - DaVinci Resolve (Premiere Pro alternative)

            ## 5. Subscription Sharing (Where Legal)

            Some subscriptions allow multiple users, making sharing cost-effective.

            **Family/Team Plans:**
            - Adobe Creative Cloud (Team plans)
            - Microsoft 365 Family (6 users)
            - Canva Pro (Team features)

            ## 6. Premium Subscription Shops

            Legitimate subscription resellers often offer significant discounts on popular software.

            **Benefits:**
            - Up to 70% savings
            - Instant delivery
            - Genuine subscriptions
            - Customer support

            ## 7. Trial Periods and Promotions

            Take advantage of free trials and promotional offers.

            **Trial Strategies:**
            - Use free trials for short-term projects
            - Watch for promotional discounts
            - Sign up for newsletters for exclusive offers

            ## 8. Assess Your Actual Needs

            Regularly review your subscriptions to ensure you're not paying for unused features.

            **Questions to Ask:**
            - Do I use all features?
            - Are there cheaper alternatives?
            - Can I downgrade to a basic plan?

            ## Conclusion

            With careful planning and strategic purchasing, you can significantly reduce your software subscription costs while maintaining access to the tools you need. The key is to evaluate your needs, explore alternatives, and take advantage of legitimate discount opportunities.
            """,
            excerpt="Learn proven strategies to reduce software subscription costs without compromising functionality. Discover bundles, discounts, and smart purchasing tips.",
            author="Finance Team",
            featured_image="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop",
            category="Software",
            tags=["Software", "Savings", "Subscriptions", "Budget", "Productivity"],
            is_published=True,
            seo_title="Save Money on Software Subscriptions - 8 Proven Strategies",
            seo_description="Learn how to save money on software subscriptions. Discover discounts, bundles, and alternatives to reduce costs while maintaining productivity.",
            seo_keywords=["software subscription savings", "cheap software", "software discounts", "subscription bundles", "save money software"]
        ),
        BlogPostCreate(
            title="VPN Guide: Why You Need One and How to Choose",
            content="""
            # VPN Guide: Why You Need One and How to Choose

            In today's digital world, online privacy and security are more important than ever. A VPN (Virtual Private Network) is essential for protecting your data and maintaining anonymity online.

            ## What is a VPN?

            A VPN creates a secure, encrypted connection between your device and a server, masking your real IP address and encrypting your internet traffic.

            ## Why You Need a VPN

            ### 1. Online Privacy Protection
            - Hide your browsing activity from ISPs
            - Prevent tracking by advertisers
            - Maintain anonymity online

            ### 2. Security on Public WiFi
            - Protect data on unsecured networks
            - Prevent man-in-the-middle attacks
            - Secure online banking and shopping

            ### 3. Access Geo-Restricted Content
            - Bypass regional restrictions
            - Access streaming content from other countries
            - Overcome censorship

            ### 4. Prevent ISP Throttling
            - Avoid bandwidth throttling
            - Maintain consistent internet speeds
            - Protect against selective slowdowns

            ## How to Choose the Right VPN

            ### 1. Security Features
            Look for these essential security features:
            - AES-256 encryption
            - No-logs policy
            - Kill switch
            - DNS leak protection

            ### 2. Server Network
            Consider:
            - Number of servers
            - Geographic coverage
            - Server speed and reliability

            ### 3. Device Compatibility
            Ensure support for:
            - Windows, Mac, Linux
            - iOS and Android
            - Router compatibility
            - Browser extensions

            ### 4. Speed and Performance
            Important factors:
            - Minimal speed loss
            - Consistent performance
            - Unlimited bandwidth

            ## Top VPN Providers 2025

            ### 1. ExpressVPN
            - Fastest speeds
            - 3000+ servers
            - Excellent security
            - 24/7 support

            ### 2. NordVPN
            - Double VPN encryption
            - Threat protection
            - 5200+ servers
            - Affordable pricing

            ### 3. CyberGhost
            - User-friendly interface
            - Specialized servers
            - Strong privacy features
            - Good value for money

            ## VPN Myths Debunked

            ### Myth 1: "VPNs Slow Down Internet"
            **Reality:** Quality VPNs have minimal impact on speed.

            ### Myth 2: "Free VPNs Are Good Enough"
            **Reality:** Free VPNs often compromise security and privacy.

            ### Myth 3: "VPNs Are Only for Tech Experts"
            **Reality:** Modern VPNs are user-friendly and easy to use.

            ## Getting Started

            1. **Choose a reputable VPN provider**
            2. **Select an appropriate subscription plan**
            3. **Download and install the app**
            4. **Connect to a server**
            5. **Enjoy secure browsing**

            ## Conclusion

            A VPN is an essential tool for online privacy and security. With the right VPN, you can browse safely, access restricted content, and protect your personal data. Choose a provider that offers strong security, good performance, and reliable customer support.

            Ready to get started? Check out our [VPN subscription deals](/category/vpn) with discounts up to 70% off premium VPN services.
            """,
            excerpt="Complete guide to VPNs: why you need one, how to choose the right provider, and tips for staying secure online in 2025.",
            author="Security Team",
            featured_image="https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=800&h=400&fit=crop",
            category="Security",
            tags=["VPN", "Privacy", "Security", "Online Safety", "Guide"],
            is_published=True,
            is_featured=True,
            seo_title="VPN Guide 2025 - Why You Need One and How to Choose the Best VPN",
            seo_description="Complete VPN guide for 2025. Learn why you need a VPN, how to choose the right provider, and protect your online privacy and security.",
            seo_keywords=["VPN guide", "best VPN 2025", "VPN security", "online privacy", "VPN comparison", "how to choose VPN"]
        )
    ]
    
    for blog_post in blog_posts:
        await db.create_blog_post(blog_post)
    
    print("✅ Database seeded successfully!")
    print("📊 Created:")
    print("   - 5 Categories")
    print("   - 12 Products")
    print("   - 3 Blog Posts")
    print("\n🚀 Your premium subscription marketplace is ready!")

if __name__ == "__main__":
    asyncio.run(seed_database())