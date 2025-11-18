# app.py
import streamlit as st
from newspaper import Article
from agent import analyze_article

st.set_page_config(
    page_title="AI News Analyzer", 
    layout="wide",
    page_icon="📰"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .analysis-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Analysis Settings")
    st.markdown("---")
    
    summary_length = st.selectbox(
        "**Summary Length:**",
        ["Short", "Medium", "Detailed"],
        help="Choose the level of detail for the summary"
    )
    
    language = st.selectbox(
        "**Output Language:**",
        ["English", "Hindi", "Bengali", "Tamil", "Telugu"],
        help="Select the language for the analysis output"
    )
    
    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("""
    This AI-powered tool analyzes news articles and provides:
    - **Smart Summaries**
    - **Sentiment Analysis**
    - **Key Keywords**
    - **Named Entities**
    
    Simply paste any news URL to get started.
    """)
    
    st.markdown("---")
    st.markdown("### 🔍 Tips")
    st.markdown("""
    - Use reputable news sources
    - Ensure the URL is accessible
    - For best results, use English articles
    """)

# Main content area
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-header">📰 AI News Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("**Transform news URLs into comprehensive AI-powered analysis**")

# URL input in main area
st.markdown("---")
url = st.text_input(
    "**Enter News Article URL:**",
    placeholder="https://example.com/news-article",
    help="Paste the complete URL of the news article you want to analyze"
)

# Extraction function
def extract_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text, article.title, article.top_image
    except Exception as e:
        st.sidebar.error(f"Extraction error: {str(e)}")
        return None, None, None

# Analyze button
if st.button("🚀 Analyze Article", type="primary", use_container_width=True):
    if not url.strip():
        st.error("❌ Please enter a valid URL.")
    else:
        with st.spinner("📥 Extracting article content..."):
            text, title, image = extract_text(url)

        if not text:
            st.error("❌ Could not extract the article. Please try another link or check if the URL is accessible.")
        else:
            # Display article header
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f'<h2 class="section-header">{title or "Article Analysis"}</h2>', unsafe_allow_html=True)
            
            if image:
                with col2:
                    st.image(image, width=150)
            
            # AI Analysis
            with st.spinner("🤖 Generating comprehensive analysis..."):
                result = analyze_article(text, summary_length, language)
            
            output = result["result"]
            
            # Parse and display results in cards
            try:
                # Summary Card
                st.markdown("## 📝 Executive Summary")
                summary_content = output.split("SENTIMENT:")[0].strip()
                st.markdown(f'<div class="analysis-card">{summary_content}</div>', unsafe_allow_html=True)
                
                # Sentiment Analysis Card
                st.markdown("## 🎭 Sentiment Analysis")
                sentiment_block = output.split("SENTIMENT:")[1]
                sentiment = sentiment_block.split("REASON:")[0].strip()
                reason = sentiment_block.split("REASON:")[1].split("KEYWORDS:")[0].strip()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="analysis-card"><h4>Sentiment</h4><p><strong>{sentiment}</strong></p></div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="analysis-card"><h4>Reasoning</h4><p>{reason}</p></div>', unsafe_allow_html=True)
                
                # Keywords Card
                st.markdown("## 🔑 Key Keywords")
                keywords_content = output.split("KEYWORDS:")[1].split("ENTITIES:")[0].strip()
                st.markdown(f'<div class="analysis-card">{keywords_content}</div>', unsafe_allow_html=True)
                
                # Entities Card
                st.markdown("## 🧍 Named Entities")
                entities_content = output.split("ENTITIES:")[1].strip()
                st.markdown(f'<div class="analysis-card">{entities_content}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Error parsing analysis results. Showing raw output:")
                st.write(output)
            
            # Footer with original article link
            st.markdown("---")
            st.markdown(f"### 📖 [Read Original Article]({url})")
            
            # Success message in sidebar
            st.sidebar.success("✅ Analysis completed successfully!")

# Footer in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        Built with Streamlit & AI
    </div>
    """,
    unsafe_allow_html=True
)