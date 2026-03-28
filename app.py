import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Company Intelligence Platform", page_icon="🔍", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "search_count" not in st.session_state:
    st.session_state.search_count = 0
if "global_rate_limit_hit" not in st.session_state:
    st.session_state.global_rate_limit_hit = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

MAX_SEARCHES_PER_SESSION = 3

# --- HERO SECTION ---
st.title("Company Insight & OSINT API")
st.markdown("Real-time lead enrichment and technical analysis powered by AI.")

# --- PROFESSIONAL SIDEBAR ---
with st.sidebar:
    st.title("Subscription & Usage")
    st.markdown("---")
    
    st.markdown("### Session Usage")
    remaining_searches = MAX_SEARCHES_PER_SESSION - st.session_state.search_count
    progress = st.session_state.search_count / MAX_SEARCHES_PER_SESSION
    st.progress(progress, text=f"Searches Used: {st.session_state.search_count}/{MAX_SEARCHES_PER_SESSION}")
    st.write(f"Remaining: {remaining_searches} search{'es' if remaining_searches != 1 else ''} this session")
    
    st.markdown("---")
    st.markdown("### Unlock Unlimited Access")
    st.link_button("Subscribe on RapidAPI", "https://rapidapi.com/pegate/api/company-insight-osint-api/pricing", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Resources")
    st.link_button("API Documentation", "https://rapidapi.com/pegate/api/company-insight-osint-api/details", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### Pricing Plans")
    with st.container(border=True):
        st.markdown("""
        **Free** 5 requests/month
        
        **Professional** 1,000 requests/month  
        $14.99/month
        
        **Enterprise** 5,000 requests/month  
        $49.00/month
        """)

# --- USER INPUT ---
remaining_searches_main = MAX_SEARCHES_PER_SESSION - st.session_state.search_count
if remaining_searches_main > 0:
    st.markdown(f"<p style='font-size: 12px; color: #999;'>Demo searches remaining: {remaining_searches_main}/{MAX_SEARCHES_PER_SESSION}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='font-size: 12px; color: #999;'>Demo searches remaining: 0</p>", unsafe_allow_html=True)

col_input, col_button = st.columns([4, 1], gap="medium")
with col_input:
    target_url = st.text_input("Enter Company URL (e.g.: https://techcrunch.com):", placeholder="https://...", key="url_input")
with col_button:
    st.write("")
    local_limit_reached = st.session_state.search_count >= MAX_SEARCHES_PER_SESSION
    global_limit_hit = st.session_state.global_rate_limit_hit
    button_disabled = local_limit_reached or global_limit_hit
    
    analyze_button = st.button("Analyze Website", use_container_width=True, disabled=button_disabled)

# Warning messages
if local_limit_reached and not global_limit_hit:
    st.warning("You have reached the 3-search limit for this demo session. Please subscribe on RapidAPI for more access.")
    st.link_button("Subscribe on RapidAPI", "https://rapidapi.com/pegate/api/company-insight-osint-api/pricing", use_container_width=True)
elif global_limit_hit:
    st.error("Global API rate limit reached. The service is currently unavailable due to high demand. Please try again later or subscribe for dedicated access.")
    st.link_button("Subscribe on RapidAPI", "https://rapidapi.com/pegate/api/company-insight-osint-api/pricing", use_container_width=True)

# --- START ANALYSIS (API CALL) ---
if analyze_button:
    if target_url:
        with st.spinner("Analyzing website..."):
            api_url = "https://company-insight-osint-api.p.rapidapi.com/analyze"
            querystring = {"url": target_url, "lang": "en"}
            
            headers = {
                "x-rapidapi-key": st.secrets["RAPIDAPI_KEY"],
                "x-rapidapi-host": "company-insight-osint-api.p.rapidapi.com"
            }

            try:
                response = requests.get(api_url, headers=headers, params=querystring)
                if response.status_code == 200:
                    # SADECE VERİYİ STATE'E KAYDEDİYORUZ, BURADA ASLA ÇİZİM YAPMIYORUZ!
                    st.session_state.search_count += 1
                    st.session_state.analysis_data = response.json()
                else:
                    if response.status_code == 429 or "Monthly limit reached" in response.text:
                        st.session_state.global_rate_limit_hit = True
                    else:
                        st.error(f"Error occurred: {response.status_code}")
                        st.write(response.text)
            except Exception as e:
                st.error(f"A system error occurred: {e}")
    else:
        st.warning("Please enter a valid URL before starting the analysis.")

# --- RENDER RESULTS (State üzerinden güvenli çizim yapılır) ---
if st.session_state.analysis_data is not None:
    data = st.session_state.analysis_data
    
    if data.get("success") is False:
        st.error(f"Analysis Failed: {data.get('error', 'The site might be blocking bot access or is unreachable.')}")
        with st.expander("Raw Error Data"):
            st.json(data)
    else:
        st.success("Analysis completed.")
        st.divider()
        
        st.markdown("### Key Insights")
        metric_col1, metric_col2, metric_col3 = st.columns(3, gap="medium")
        
        with metric_col1:
            st.metric("Business Type", data.get("company_type") or "Unknown")
        
        with metric_col2:
            st.metric("Industry", data.get("industry") or "Unknown")
        
        with metric_col3:
            tech_data = data.get("tech_stack") or []
            st.metric("Technologies", f"{len(tech_data)} detected")
        
        st.divider()
        
        st.markdown("### Analysis Summary")
        with st.container(border=True):
            st.info(data.get("ai_summary") or "Summary not available.")
        st.divider()
        
        st.markdown("### Intelligence Data")
        intel_col1, intel_col2 = st.columns(2, gap="medium")
        
        with intel_col1:
            st.markdown("#### Contact Information")
            emails = data.get("emails") or []
            with st.container(border=True):
                if emails:
                    for email in emails:
                        st.code(email, language="text")
                else:
                    st.info("No contact emails found.")
        
        with intel_col2:
            st.markdown("#### Digital Presence")
            social_links = data.get("social_links") or []
            with st.container(border=True):
                if social_links:
                    for link in social_links:
                        st.markdown(f"[{link[:50]}...](https://{link})" if len(link) > 50 else f"[{link}](https://{link})")
                else:
                    st.info("No social media links found.")
        
        st.divider()
        
        st.markdown("### Technology Stack")
        with st.container(border=True):
            if not tech_data:
                st.info("No technology stack data available.")
            else:
                tech_list = [t.get("name", str(t)) if isinstance(t, dict) else str(t) for t in tech_data]
                bg_colors = [
                    "#2c3e50", "#34495e", "#7f8c8d", "#95a5a6",
                    "#1a252f", "#3d4e5c", "#4a5f7a", "#56697e",
                    "#2a3f52", "#485a6f", "#1f3a4a", "#3d5064"
                ]
                tags_html = ""
                for i, tech in enumerate(tech_list):
                    bg_color = bg_colors[i % len(bg_colors)]
                    tags_html += f"""<span style='display: inline-block; background-color: {bg_color}; color: white; padding: 6px 12px; border-radius: 16px; margin: 4px 4px 4px 0; font-weight: 500; font-size: 12px; border: 1px solid #e0e0e0;'>{tech}</span>"""
                
                st.markdown(tags_html, unsafe_allow_html=True)
                st.markdown("")
                st.markdown(f"**Total:** {len(tech_list)} technologies detected")
        
        st.divider()
        with st.expander("Raw JSON Data"):
            st.json(data)

# --- GLOBAL RATE LIMIT YÖNETİMİ ---
if st.session_state.global_rate_limit_hit:
    st.warning("Today's free global demo limit has been reached due to high demand. To continue testing, you can subscribe to our \"Free Tier\" (5 requests/month) directly on RapidAPI for your own personal use!")
    st.link_button("Subscribe on RapidAPI", "https://rapidapi.com/pegate/api/company-insight-osint-api/pricing", use_container_width=True)
