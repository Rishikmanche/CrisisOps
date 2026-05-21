# 🛡️ CrisisOps — DisasterGuard AI

**Real-time AI-powered disaster detection and response command center.**



---

## 🚀 Features

- **AI-Powered Analysis** — Uses Google Gemini to classify and assess disaster reports in real-time
- **Interactive Map** — Live geospatial visualization of active incidents using Folium
- **Priority Feed** — Severity-ranked incident feed with real-time updates
- **Data Sources** — Aggregated satellite and social media feed scanning
- **Smart Filtering** — AI distinguishes real threats from noise automatically

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI/ML | Google Gemini API |
| Maps | Folium + Streamlit-Folium |
| Data | Pandas, Feedparser |
| Language | Python |

## 📁 Project Structure

```
CrisisOps/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # API keys (not tracked)
├── components/
│   ├── map_view.py         # Interactive map component
│   └── data_feed.py        # Data sources tab
├── data/
│   └── simulator.py        # Fake report generator
└── utils/
    └── gemini_brain.py     # Gemini AI analysis engine
```

## ⚡ Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/Rishikmanche/CrisisOps.git
   cd CrisisOps
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   echo "GEMINI_API_KEY=your_key_here" > .env
   ```
   Get a key from [Google AI Studio](https://aistudio.google.com/apikey)

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📄 License

MIT
https://crisisops.streamlit.app
