import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="VitaCode OSINT AI", page_icon="🕵️‍♂️", layout="wide")

# --- TITLE AND DESCRIPTION ---
st.title("🕵️‍♂️ Company Insight & OSINT AI")
st.markdown("**Enter a B2B company URL and let AI analyze it in seconds.**")
st.markdown("*Powered by RapidAPI & Gemini AI | Built by Samed*")
st.divider()

# --- DEVELOPER PORTAL SIDEBAR ---
with st.sidebar:
    st.title("🚀 Get Full Access")
    st.markdown("---")
    
    # Subscribe Button
    st.markdown("### 📊 Subscribe to Unlock")
    st.link_button("🔗 Subscribe on RapidAPI", "https://rapidapi.com/pegate/api/company-insight-osint-api/pricing", use_container_width=True)
    
    st.markdown("---")
    
    # API Documentation
    st.markdown("### 📚 Developer Resources")
    st.link_button("📖 API Documentation", "https://rapidapi.com/pegate/api/company-insight-osint-api/details", use_container_width=True)
    
    st.markdown("---")
    
    # Pricing Tiers
    st.markdown("### 💰 Pricing Tiers")
    with st.container(border=True):
        st.markdown("""
        **Free Plan**  
        5 requests/month
        
        **Pro Plan** 💎  
        1,000 requests/month  
        _$14.99/month_
        
        **Ultra Plan** 🚀  
        5,000 requests/month  
        _$49.00/month_
        """)

# --- USER INPUT ---
col_input, col_button = st.columns([4, 1], gap="medium")
with col_input:
    target_url = st.text_input("Enter Company URL (e.g.: https://techcrunch.com):", placeholder="https://...", key="url_input")
with col_button:
    st.write("")  # Spacer for alignment
    analyze_button = st.button("🚀 Start Analysis", use_container_width=True)
# --- START ANALYSIS ---
if analyze_button:
    if target_url:
        with st.spinner("Analyzing company data and generating insights... (This may take 10-15 seconds)"):
            
            # RapidAPI Endpoint
            api_url = "https://company-insight-osint-api.p.rapidapi.com/analyze"
            querystring = {"url": target_url, "lang": "en"}
            
            headers = {
                "x-rapidapi-key": st.secrets["RAPIDAPI_KEY"],
                "x-rapidapi-host": "company-insight-osint-api.p.rapidapi.com"
            }

            try:
                response = requests.get(api_url, headers=headers, params=querystring)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Analysis completed successfully!")
                    st.divider()
                    
                    # --- KEY METRICS SECTION ---
                    st.markdown("### 📈 Key Metrics")
                    metric_col1, metric_col2, metric_col3 = st.columns(3, gap="medium")
                    
                    with metric_col1:
                        st.metric("🏢 Business Model", data.get("company_type", "Unknown"))
                    
                    with metric_col2:
                        st.metric("🌍 Industry", data.get("industry", "Unknown"))
                    
                    with metric_col3:
                        tech_count = len(data.get("tech_stack", []))
                        st.metric("💻 Technologies", f"{tech_count} tools")
                    
                    st.divider()
                    
                    # --- AI SUMMARY ---
                    st.markdown("### 📊 AI Summary")
                    st.info(data.get("ai_summary", "Summary not available."))
                    st.divider()
                    
                    # --- CONTACT INTELLIGENCE & SOCIAL FOOTPRINT ---
                    st.markdown("### 🤝 Business Intelligence")
                    intel_col1, intel_col2 = st.columns(2, gap="medium")
                    
                    with intel_col1:
                        st.markdown("#### 📧 Contact Intelligence")
                        emails = data.get("emails", [])
                        with st.container(border=True):
                            if emails:
                                for email in emails:
                                    st.code(email, language="text")
                            else:
                                st.info("No contact emails found.")
                    
                    with intel_col2:
                        st.markdown("#### 🔗 Social Footprint")
                        social_links = data.get("social_links", [])
                        with st.container(border=True):
                            if social_links:
                                for link in social_links:
                                    st.markdown(f"🌐 [{link[:50]}...](https://{link})" if len(link) > 50 else f"🌐 [{link}](https://{link})")
                            else:
                                st.info("No social media links found.")
                    
                    st.divider()
                    
                    # --- TECHNOLOGY STACK SECTION ---
                    st.markdown("### 💻 Technology Stack")
                    tech_data = data.get("tech_stack", [])
                    
                    with st.container(border=True):
                        if not tech_data:
                            st.info("No technology stack data available.")
                        else:
                            # Extract names from dict objects, or use the value as-is if string
                            tech_list = [t.get("name", str(t)) if isinstance(t, dict) else str(t) for t in tech_data]
                            
                            # Display as colored tags
                            colors = ["🔵", "🟢", "🟠", "🟣", "🔴", "🟡", "⚪", "🟤"]
                            tags_html = ""
                            for i, tech in enumerate(tech_list):
                                color = colors[i % len(colors)]
                                tags_html += f"{color} `{tech}`  "
                            st.markdown(tags_html)
                            
                            st.markdown(f"**Total:** {len(tech_list)} technologies detected")
                    
                    st.divider()
                    
                    # --- RAW JSON DATA FOR DEVELOPERS ---
                    with st.expander("👨‍💻 Raw JSON Data (For Developers)"):
                        st.json(data)
                else:
                    st.error(f"❌ Error occurred: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"A system error occurred: {e}")
    else:
        st.warning("Please enter a valid URL before starting the analysis.")