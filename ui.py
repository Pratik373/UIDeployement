import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Podcast Performance Predictor",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .header-style {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #3498db;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .pred-high {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4caf50;
    }
    .pred-medium {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #ffc107;
    }
    .pred-low {
        background-color: #ffebee;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #f44336;
    }
    .required-field {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # App header
    st.markdown('<p class="header-style">🎙️ Podcast Performance Predictor</p>', unsafe_allow_html=True)
    st.markdown("Predict listening time and success factors for podcast episodes")
    
    with st.expander("About this tool"):
        st.write("""
        This system uses machine learning to predict podcast performance based on:
        - Episode characteristics
        - Genre and content details
        - Host and guest popularity
        - Publication timing
        """)
    
    # Main form
    with st.form("podcast_form"):
        st.markdown('<p class="section-header">Podcast Information</p>', unsafe_allow_html=True)
        
        # Basic Details
        podcast_name = st.text_input("Podcast Name", value="Joke Junction", help="Enter podcast name")
        episode_title = st.text_input("Episode Title", value="Episode 26", help="Enter episode title")
        
        # Content Information
        st.markdown('<p class="section-header">Content Details</p>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            genre = st.selectbox(
                "Genre",
                options=["True Crime", "Comedy", "Education", "Technology", "Health", 
                         "News", "Music", "Sports"],
                index=1  # Default to Comedy
            )
        with col2:
            episode_length = st.number_input(
                "Episode Length (minutes)",
                min_value=1,
                value=119,
                step=1
            )
        with col3:
            episode_sentiment = st.selectbox(
                "Episode Sentiment",
                options=["Positive", "Neutral", "Negative"],
                index=0
            )
        
        # Host and Guest Information
        st.markdown('<p class="section-header">Host & Guest Details</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            host_popularity = st.slider(
                "Host Popularity (%)",
                min_value=0,
                max_value=100,
                value=67
            )
        with col2:
            guest_popularity = st.slider(
                "Guest Popularity (%)",
                min_value=0,
                max_value=100,
                value=76
            )
        
        # Publication Details
        st.markdown('<p class="section-header">Publication Details</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            publication_day = st.selectbox(
                "Publication Day",
                options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                index=5  # Default to Saturday
            )
        with col2:
            publication_time = st.selectbox(
                "Publication Time",
                options=["Morning", "Afternoon", "Evening", "Night"],
                index=1  # Default to Afternoon
            )
        
        # Advertising Information
        st.markdown('<p class="section-header">Advertising</p>', unsafe_allow_html=True)
        number_of_ads = st.slider(
            "Number of Ads in Episode",
            min_value=0,
            max_value=5,
            value=2
        )
        
        # Form submission
        submitted = st.form_submit_button(
            "🚀 Predict Listening Time",
            type="primary",
            use_container_width=True
        )
    
    # Results Section
    if submitted:
        with st.spinner("Analyzing podcast episode..."):
            # Simulate prediction (replace with actual model)
            listening_time = min(120, max(10, 
                           (episode_length * 0.7) + 
                           (host_popularity * 0.3) - 
                           (number_of_ads * 5)))
            
            # Determine prediction category
            if listening_time >= 60:
                pred_category = "high"
                pred_label = "High Engagement"
            elif listening_time >= 30:
                pred_category = "medium"
                pred_label = "Medium Engagement"
            else:
                pred_category = "low"
                pred_label = "Low Engagement"
            
            # Display results
            st.markdown('<p class="section-header">Prediction Results</p>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="pred-{pred_category}">
                <h3>Engagement Prediction: {pred_label}</h3>
                <p>Estimated listening time: <strong>{listening_time:.1f} minutes</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Key metrics
            st.subheader("Key Metrics")
            cols = st.columns(3)
            cols[0].metric("Episode Length", f"{episode_length} minutes")
            cols[1].metric("Host Popularity", f"{host_popularity}%")
            cols[2].metric("Number of Ads", number_of_ads)
            
            # Feature importance visualization
            st.subheader("Performance Factors")
            factors = {
                "Episode Length": episode_length * 0.5,
                "Host Popularity": host_popularity * 0.3,
                "Genre": 15 if genre in ["True Crime", "News"] else 10,
                "Publication Timing": 12 if publication_time == "Evening" else 8,
                "Number of Ads": - (number_of_ads * 3)
            }
            
            factors_df = pd.DataFrame({
                "Factor": list(factors.keys()),
                "Impact": list(factors.values())
            }).sort_values("Impact", ascending=False)
            
            st.bar_chart(factors_df.set_index("Factor"), height=300)

if __name__ == "__main__":
    main()