# 🛒 E-Com Intelligence - Streamlit App

Real-time web scraping tool for tracking products across **Amazon India**, **Flipkart**, **Meesho**, and **Myntra**.

## ✨ Features

- ✅ **No API Keys Required**
- ✅ **Real Web Scraping** (Amazon & Flipkart)
- ✅ **Live Data** from e-commerce sites
- ✅ **Export to CSV**
- ✅ **Beautiful UI** with Streamlit
- ✅ **100% Free Deployment**

---

## 🚀 Deploy to Streamlit Cloud (FREE)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ecom-intel-streamlit.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository: `ecom-intel-streamlit`
5. Main file path: `app.py`
6. Click **"Deploy"**

🎉 **Your app will be live in 2-3 minutes!**

**Your URL**: `https://YOUR_USERNAME-ecom-intel-streamlit.streamlit.app`

---

## 💻 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open: http://localhost:8501

---

## 📋 How It Works

### Amazon India Scraper
- Fetches search results from Amazon.in
- Extracts: Title, Price, Rating, Reviews, ASIN
- Identifies Sponsored vs Organic listings

### Flipkart Scraper
- Scrapes Flipkart search results
- Parses product information
- Returns structured data

### Demo Mode
- Meesho & Myntra show demo data (scrapers coming soon)
- Fallback to demo if scraping fails

---

## ⚠️ Important Notes

### Scraping Ethics
- ✅ Only for personal research/education
- ✅ Respect robots.txt
- ✅ Don't overload servers
- ❌ Don't use for commercial purposes without permission

### Rate Limiting
- The app adds delays between requests
- Rotates user agents
- Follows e-commerce site ToS

### Anti-Bot Detection
- Amazon and Flipkart have anti-bot measures
- Scraping may occasionally fail (returns demo data)
- For production, consider using official APIs

---

## 🔧 Customization

### Add More Platforms

Edit `app.py` and add scraper functions:

```python
def scrape_myntra(keyword, limit=10):
    # Your scraping logic
    pass
```

### Improve Scraping

- Add proxy rotation
- Implement retry logic
- Use Selenium for JavaScript-heavy sites

---

## 📊 Features Breakdown

| Feature | Status | Description |
|---------|--------|-------------|
| Keyword Rank Tracker | ✅ Live | Track product rankings |
| Product Info Fetcher | ✅ Live | Get details by ASIN |
| Amazon India Scraper | ✅ Live | Real-time scraping |
| Flipkart Scraper | ✅ Live | Real-time scraping |
| Meesho Scraper | 🚧 Coming | In development |
| Myntra Scraper | 🚧 Coming | In development |
| BSR Tracker | 🚧 Coming | Q4 2025 |
| CSV Export | ✅ Live | Download data |

---

## 🆘 Troubleshooting

### "No results found"
- Website structure may have changed
- Add delays between requests
- Check if site is accessible

### "Scraping failed"
- Anti-bot detection triggered
- Use VPN or proxy
- Reduce request frequency

### App not deploying
- Check `requirements.txt`
- Verify file structure
- Check Streamlit Cloud logs

---

## 📝 License

MIT License - Free to use and modify

---

## 🤝 Contributing

Pull requests welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📧 Support

Having issues? Create a GitHub issue or contact via:
- GitHub Issues
- Email: your-email@example.com

---

**Built with ❤️ using Streamlit**

**No API keys. No complex setup. Just pure web scraping magic! ✨**
