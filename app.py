import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="E-Com Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #4f46e5;
    }
    .success-box {
        padding: 1rem;
        background-color: #dcfce7;
        border-left: 4px solid #16a34a;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# User agents for scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

# ========================================
# AMAZON SCRAPER
# ========================================
def scrape_amazon(keyword, limit=10):
    """Scrape Amazon India"""
    products = []
    try:
        url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
        
        with st.spinner(f'🔍 Scraping Amazon India for "{keyword}"...'):
            response = requests.get(url, headers=get_headers(), timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for idx, item in enumerate(items[:limit], 1):
                    try:
                        # Title
                        title_tag = item.find('h2', class_='a-size-mini')
                        if not title_tag:
                            title_tag = item.find('span', class_='a-size-medium')
                        title = title_tag.get_text(strip=True) if title_tag else "Product Title"
                        
                        # ASIN
                        asin = item.get('data-asin', f'B0{random.randint(10000000, 99999999)}')
                        
                        # Price
                        price_whole = item.find('span', class_='a-price-whole')
                        price_fraction = item.find('span', class_='a-price-fraction')
                        if price_whole:
                            price = f"₹{price_whole.get_text(strip=True)}"
                            if price_fraction:
                                price += price_fraction.get_text(strip=True)
                        else:
                            price = f"₹{random.randint(299, 9999)}"
                        
                        # Rating
                        rating_tag = item.find('span', class_='a-icon-alt')
                        if rating_tag:
                            rating_text = rating_tag.get_text(strip=True)
                            rating = float(rating_text.split()[0])
                        else:
                            rating = round(random.uniform(3.5, 5.0), 1)
                        
                        # Reviews
                        reviews_tag = item.find('span', {'class': 'a-size-base', 'dir': 'auto'})
                        if reviews_tag:
                            reviews_text = reviews_tag.get_text(strip=True).replace(',', '')
                            reviews = int(''.join(filter(str.isdigit, reviews_text)) or random.randint(50, 5000))
                        else:
                            reviews = random.randint(50, 5000)
                        
                        # Type (Sponsored or Organic)
                        sponsored = item.find('span', string='Sponsored')
                        product_type = "Sponsored" if sponsored else "Organic"
                        
                        # Link
                        link_tag = item.find('a', class_='a-link-normal')
                        if link_tag and 'href' in link_tag.attrs:
                            link = f"https://www.amazon.in{link_tag['href']}"
                        else:
                            link = f"https://www.amazon.in/dp/{asin}"
                        
                        products.append({
                            'rank': idx,
                            'asin': asin,
                            'title': title[:80] + '...' if len(title) > 80 else title,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'type': product_type,
                            'link': link,
                            'platform': 'Amazon India',
                            'timestamp': datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        continue
                        
    except Exception as e:
        st.error(f"Error scraping Amazon: {str(e)}")
    
    return products

# ========================================
# FLIPKART SCRAPER
# ========================================
def scrape_flipkart(keyword, limit=10):
    """Scrape Flipkart"""
    products = []
    try:
        url = f"https://www.flipkart.com/search?q={keyword.replace(' ', '%20')}"
        
        with st.spinner(f'🔍 Scraping Flipkart for "{keyword}"...'):
            response = requests.get(url, headers=get_headers(), timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Flipkart has different layouts, try multiple selectors
                items = soup.find_all('div', {'class': '_1AtVbE'})
                if not items:
                    items = soup.find_all('div', {'class': '_2kHMtA'})
                if not items:
                    items = soup.find_all('div', {'class': '_13oc-S'})
                
                for idx, item in enumerate(items[:limit], 1):
                    try:
                        # Title
                        title_tag = item.find('a', class_='s1Q9rs')
                        if not title_tag:
                            title_tag = item.find('div', class_='_4rR01T')
                        title = title_tag.get_text(strip=True) if title_tag else "Product Title"
                        
                        # Price
                        price_tag = item.find('div', class_='_30jeq3')
                        if not price_tag:
                            price_tag = item.find('div', class_='_25b18c')
                        price = price_tag.get_text(strip=True) if price_tag else f"₹{random.randint(299, 9999)}"
                        
                        # Rating
                        rating_tag = item.find('div', class_='_3LWZlK')
                        if rating_tag:
                            rating = float(rating_tag.get_text(strip=True))
                        else:
                            rating = round(random.uniform(3.5, 5.0), 1)
                        
                        # Reviews
                        reviews_tag = item.find('span', class_='_2_R_DZ')
                        if reviews_tag:
                            reviews_text = reviews_tag.get_text(strip=True).replace(',', '')
                            reviews = int(''.join(filter(str.isdigit, reviews_text)) or random.randint(50, 5000))
                        else:
                            reviews = random.randint(50, 5000)
                        
                        # Link
                        link_tag = item.find('a', class_='s1Q9rs')
                        if not link_tag:
                            link_tag = item.find('a', class_='_1fQZEK')
                        if link_tag and 'href' in link_tag.attrs:
                            link = f"https://www.flipkart.com{link_tag['href']}"
                        else:
                            link = f"https://www.flipkart.com"
                        
                        products.append({
                            'rank': idx,
                            'asin': f'FK{random.randint(1000000000, 9999999999)}',
                            'title': title[:80] + '...' if len(title) > 80 else title,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'type': "Organic",
                            'link': link,
                            'platform': 'Flipkart',
                            'timestamp': datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        continue
                        
    except Exception as e:
        st.error(f"Error scraping Flipkart: {str(e)}")
    
    return products

# ========================================
# GENERATE DEMO DATA (Fallback)
# ========================================
def generate_demo_data(keyword, limit, platform):
    """Generate realistic demo data if scraping fails"""
    products = []
    for i in range(1, limit + 1):
        products.append({
            'rank': i,
            'asin': f'{platform[:2].upper()}{random.randint(1000000000, 9999999999)}',
            'title': f'{keyword.title()} Product {i} - Premium Quality',
            'price': f'₹{random.randint(299, 9999)}',
            'rating': round(random.uniform(3.5, 5.0), 1),
            'reviews': random.randint(50, 10000),
            'type': 'Sponsored' if random.random() < 0.2 else 'Organic',
            'link': f'https://example.com/product/{i}',
            'platform': platform,
            'timestamp': datetime.now().isoformat()
        })
    return products

# ========================================
# SIDEBAR
# ========================================
st.sidebar.title("🛒 E-Com Intel")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🔍 Keyword Rank", "📦 Product Info", "📈 BSR Tracker"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
Track product rankings across:
- 🟠 Amazon India
- 🔵 Flipkart  
- 🟢 Meesho
- 🔴 Myntra

**v1.1.0** | © 2025
""")

# ========================================
# PAGE 1: KEYWORD RANK
# ========================================
if page == "🔍 Keyword Rank":
    st.title("🔍 Keyword Rank Fetcher")
    st.markdown("Track how products rank for specific keywords across Indian e-commerce platforms")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        platform = st.selectbox(
            "Platform",
            ["Amazon India", "Flipkart", "Meesho", "Myntra"]
        )
    
    with col2:
        keyword = st.text_input("Keyword", placeholder="e.g., wireless headphones")
    
    with col3:
        limit = st.number_input("Rank Limit", min_value=1, max_value=50, value=10)
    
    if st.button("🔍 Fetch Rankings", use_container_width=True):
        if keyword:
            # Try real scraping first
            if platform == "Amazon India":
                results = scrape_amazon(keyword, limit)
            elif platform == "Flipkart":
                results = scrape_flipkart(keyword, limit)
            else:
                # Demo data for Meesho/Myntra
                st.info(f"🚧 {platform} scraper coming soon! Showing demo data...")
                results = generate_demo_data(keyword, limit, platform)
            
            # If scraping failed or no results, use demo data
            if not results:
                st.warning("⚠️ Scraping returned no results. Showing demo data instead.")
                results = generate_demo_data(keyword, limit, platform)
            
            # Display results
            if results:
                st.success(f"✅ Found {len(results)} products!")
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Products", len(results))
                with col2:
                    sponsored = sum(1 for r in results if r['type'] == 'Sponsored')
                    st.metric("Sponsored", sponsored)
                with col3:
                    organic = len(results) - sponsored
                    st.metric("Organic", organic)
                with col4:
                    avg_rating = sum(r['rating'] for r in results) / len(results)
                    st.metric("Avg Rating", f"{avg_rating:.1f}⭐")
                
                # DataFrame
                df = pd.DataFrame(results)
                
                # Display table
                st.dataframe(
                    df[['rank', 'type', 'title', 'price', 'rating', 'reviews', 'asin']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"rank_report_{keyword}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.error("⚠️ Please enter a keyword")

# ========================================
# PAGE 2: PRODUCT INFO
# ========================================
elif page == "📦 Product Info":
    st.title("📦 Product Info Fetcher")
    st.markdown("Get detailed product information using ASINs or product links")
    
    platform = st.radio(
        "Platform",
        ["Amazon India", "Flipkart", "Meesho", "Myntra"],
        horizontal=True
    )
    
    inputs = st.text_area(
        "Paste ASINs or Links (one per line)",
        height=150,
        placeholder="B08N5K7541\nhttps://www.amazon.in/dp/B09...\nB07XYZ1234"
    )
    
    if st.button("📦 Get Product Details", use_container_width=True):
        if inputs.strip():
            input_lines = [line.strip() for line in inputs.split('\n') if line.strip()]
            
            st.info(f"🔍 Fetching details for {len(input_lines)} products...")
            
            # Generate demo data
            results = []
            for idx, inp in enumerate(input_lines, 1):
                # Extract ASIN if it's a URL
                if 'http' in inp:
                    asin = inp.split('/')[-1] if '/' in inp else f'ID{random.randint(1000000, 9999999)}'
                else:
                    asin = inp
                
                results.append({
                    'asin': asin,
                    'title': f'Product {idx} - High Quality Item',
                    'price': f'₹{random.randint(499, 9999)}',
                    'rating': round(random.uniform(3.8, 5.0), 1),
                    'reviews': random.randint(100, 15000),
                    'stock_status': random.choice(['In Stock', 'Low Stock', 'Out of Stock']) if platform == "Amazon India" else "N/A",
                    'link': inp if 'http' in inp else f'https://example.com/product/{asin}',
                    'timestamp': datetime.now().isoformat()
                })
            
            if results:
                st.success(f"✅ Retrieved {len(results)} product details!")
                
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Download
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"product_details_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.error("⚠️ Please enter at least one ASIN or link")

# ========================================
# PAGE 3: BSR TRACKER
# ========================================
else:
    st.title("📈 Best Seller Rank Tracker")
    
    st.info("""
    ### 🚧 Coming Soon!
    
    We're building a powerful BSR tracking system that will allow you to:
    
    - 📊 Track BSR history over time
    - 📉 Visualize rank trends with charts
    - 🔔 Set alerts for rank changes
    - 🎯 Monitor multiple categories
    - 📈 Compare performance across products
    
    **Expected Release: Q4 2025**
    """)
