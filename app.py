import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Company Intelligence Platform", page_icon="🔍", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "search_count" not in st.session_state:
    st.session_state.search_count = 0

MAX_SEARCHES_PER_SESSION = 3

# --- HERO SECTION ---
st.markdown("""
<div style='text-align: center; padding: 30px 0; border-bottom: 1px solid #e0e0e0;'>
    <h1 style='font-size: 2.2em; margin-bottom: 15px; color: #1a1a1a; font-weight: 600;'>Enterprise-Grade Company Intelligence & OSINT</h1>
    <p style='font-size: 1em; color: #666; margin-bottom: 0; line-height: 1.6;'>
        Analyze any business URL to extract technology stacks, company contacts, and digital presence insights instantly.
    </p>
</div>
""", unsafe_allow_html=True)
st.write("")
# --- PROFESSIONAL SIDEBAR ---
with st.sidebar:
    st.title("Subscription & Usage")
    st.markdown("---")
    
    # Usage Statistics
    st.markdown("### Session Usage")
    remaining_searches = MAX_SEARCHES_PER_SESSION - st.session_state.search_count
    progress = st.session_state.search_count / MAX_SEARCHES_PER_SESSION
    st.progress(progress, text=f"Searches Used: {st.session_state.search_count}/{MAX_SEARCHES_PER_SESSION}")
    if remaining_searches > 0:
        st.caption(f"Remaining: {remaining_searches} search{'es' if remaining_searches != 1 else ''} this session")
    
    st.markdown("---")
    
    # Subscribe Button
    st.markdown("### Unlock Unlimited Access")
    st.link_button("Subscribe on RapidAPI", "https://rapidapi.com/pegate/api/company-insight-osint-api/pricing", use_container_width=True)
    
    st.markdown("---")
    
    # API Documentation
    st.markdown("### Resources")
    st.link_button("API Documentation", "https://rapidapi.com/pegate/api/company-insight-osint-api/details", use_container_width=True)
    
    st.markdown("---")
    
    # Pricing Tiers
    st.markdown("### Pricing Plans")
    with st.container(border=True):
        st.markdown("""
        **Free**  
        5 requests/month
        
        **Professional**  
        1,000 requests/month  
        $14.99/month
        
        **Enterprise**  
        5,000 requests/month  
        $49.00/month
        """)

# --- USER INPUT ---
# Display free demo counter
remaining_searches_main = MAX_SEARCHES_PER_SESSION - st.session_state.search_count
if remaining_searches_main > 0:
    st.caption(f"Demo Searches Remaining: {remaining_searches_main}")
else:
    st.caption("Demo Searches Remaining: 0")

col_input, col_button = st.columns([4, 1], gap="medium")
with col_input:
    target_url = st.text_input("Enter Company URL (e.g.: https://techcrunch.com):", placeholder="https://...", key="url_input")
with col_button:
    st.write("")  # Spacer for alignment
    
    # Check if search limit is reached
    search_limit_reached = st.session_state.search_count >= MAX_SEARCHES_PER_SESSION
    analyze_button = st.button(
        "Analyze Website", 
        use_container_width=True,
        disabled=search_limit_reached
    )

# Show warning if limit is reached
if search_limit_reached:
    st.warning("Demo limit reached. Subscribe for unlimited access.")
    st.markdown("[View Pricing Plans](https://rapidapi.com/pegate/api/company-insight-osint-api/pricing)")
# --- START ANALYSIS ---
if analyze_button:
    if target_url:
        with st.spinner("Analyzing website..."):
            
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
                    # Increment search counter on successful analysis
                    st.session_state.search_count += 1
                    
                    data = response.json()
                    st.success("Analysis completed.")
                    st.divider()
                    
                    # --- KEY METRICS SECTION ---
                    st.markdown("### Key Insights")
                    metric_col1, metric_col2, metric_col3 = st.columns(3, gap="medium")
                    
                    with metric_col1:
                        st.metric("Business Type", data.get("company_type", "Unknown"))
                    
                    with metric_col2:
                        st.metric("Industry", data.get("industry", "Unknown"))
                    
                    with metric_col3:
                        tech_count = len(data.get("tech_stack", []))
                        st.metric("Technologies", f"{tech_count} detected")
                    
                    st.divider()
                    
                    # --- AI SUMMARY ---
                    st.markdown("### Analysis Summary")
                    with st.container(border=True):
                        st.info(data.get("ai_summary", "Summary not available."))
                    st.divider()
                    
                    # --- CONTACT INTELLIGENCE & SOCIAL FOOTPRINT ---
                    st.markdown("### Intelligence Data")
                    intel_col1, intel_col2 = st.columns(2, gap="medium")
                    
                    with intel_col1:
                        st.markdown("#### Contact Information")
                        emails = data.get("emails", [])
                        with st.container(border=True):
                            if emails:
                                for email in emails:
                                    st.code(email, language="text")
                            else:
                                st.info("No contact emails found.")
                    
                    with intel_col2:
                        st.markdown("#### Digital Presence")
                        social_links = data.get("social_links", [])
                        with st.container(border=True):
                            if social_links:
                                for link in social_links:
                                    st.markdown(f"[{link[:50]}...](https://{link})" if len(link) > 50 else f"[{link}](https://{link})")
                            else:
                                st.info("No social media links found.")
                    
                    st.divider()
                    
                    # --- TECHNOLOGY STACK SECTION ---
                    st.markdown("### Technology Stack")
                    tech_data = data.get("tech_stack", [])
                    
                    with st.container(border=True):
                        if not tech_data:
                            st.info("No technology stack data available.")
                        else:
                            # Extract names from dict objects, or use the value as-is if string
                            tech_list = [t.get("name", str(t)) if isinstance(t, dict) else str(t) for t in tech_data]
                            
                            # Define professional color palette for pill-shaped tags
                            bg_colors = [
                                "#2c3e50", "#34495e", "#7f8c8d", "#95a5a6",
                                "#1a252f", "#3d4e5c", "#4a5f7a", "#56697e",
                                "#2a3f52", "#485a6f", "#1f3a4a", "#3d5064"
                            ]
                            
                            # Create professional pill-shaped tags using HTML/markdown
                            tags_html = ""
                            for i, tech in enumerate(tech_list):
                                bg_color = bg_colors[i % len(bg_colors)]
                                tags_html += f"""<span style='display: inline-block; background-color: {bg_color}; color: white; padding: 6px 12px; border-radius: 16px; margin: 4px 4px 4px 0; font-weight: 500; font-size: 12px; border: 1px solid #e0e0e0;'>{tech}</span>"""
                            
                            st.markdown(tags_html, unsafe_allow_html=True)
                            st.markdown(f"")
                            st.markdown(f"**Total:** {len(tech_list)} technologies detected")
                    
                    st.divider()
                    
                    # --- RAW JSON DATA FOR DEVELOPERS ---
                    with st.expander("Raw JSON Data"):
                        st.json(data)
                else:
                    st.error(f"Error occurred: {response.status_code}")
                    st.write(response.text)
            except Exception as e:
                st.error(f"A system error occurred: {e}")
    else:
        st.warning("Please enter a valid URL before starting the analysis.")
