import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import time
 
# New import for timer 
# ---------------- Page Config ----------------
st.set_page_config(page_title="🌍 India Air Quality ", layout="wide")

# ---------------- Premium Cyber-Glow UI Design ----------------
def apply_premium_theme():
    st.markdown(
        """
        <style>
        /* Base Background with Professional Image & Dark Overlay */
        .stApp {
            background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80") no-repeat fixed;
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Animated Glowing Border for Cards */
        @keyframes border-glow {
            0% { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0, 210, 255, 0.2); }
            50% { border-color: #3a7bd5; box-shadow: 0 0 25px rgba(58, 123, 213, 0.5); }
            100% { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0, 210, 255, 0.2); }
        }
        
        /* Basic styling for the tab container */
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background-color: transparent;
        }

        /* Styling for all tabs (Inactive state) */
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px 10px 0px 0px;
            color: white !important;
            border: none;
            padding: 0px 25px;
            transition: all 0.3s ease-in-out;
        }

        /* THE GLOW EFFECT (Active/Selected state) */
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%) !important;
            box-shadow: 0px 0px 25px rgba(0, 210, 255, 0.5) !important;
            color: white !important;
            font-weight: bold !important;
            border-bottom: 4px solid #ff4b4b !important;
        }

        /* Subtle glow on Hover */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(0, 210, 255, 0.1);
            color: #00d2ff !important;
            box-shadow: 0px 0px 10px rgba(0, 210, 255, 0.2);
        }

        /* Home Page Welcome Card (Premium Design) */
        .home-card {
            background: rgba(255, 255, 255, 0.03);
            padding: 45px;
            border-radius: 25px;
            border: 2px solid #00d2ff;
            animation: border-glow 4s infinite ease-in-out;
            backdrop-filter: blur(15px);
            margin-bottom: 30px;
        }

        /* Prediction Result Glow Card */
        .prediction-box {
            background: rgba(0, 210, 255, 0.05);
            padding: 30px;
            border-radius: 20px;
            border: 1px solid #00d2ff;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 210, 255, 0.2);
            margin-top: 20px;
        }

        /* Health Impact Card */
        .health-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #00d2ff;
            margin-top: 15px;
        }
        
        /* KPI Metrics with Neumorphic Glow */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.04) !important;
            border-radius: 20px !important;
            border: 1px solid rgba(0, 210, 255, 0.3) !important;
            padding: 25px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8) !important;
            transition: 0.4s ease;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-8px);
            background: rgba(0, 210, 255, 0.08) !important;
            box-shadow: 0 0 25px rgba(0, 210, 255, 0.4) !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(5, 5, 5, 0.98) !important;
            border-right: 1px solid rgba(0, 210, 255, 0.2);
        }

        /* Metric Value Glow */
        div[data-testid="stMetricValue"] > div {
            color: #00d2ff !important;
            text-shadow: 0 0 10px rgba(0, 210, 255, 0.8);
            font-size: 2.5rem !important;
            font-weight: 800 !important;
        }

        .section-header {
            color: #00d2ff !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
        }

        /* Scrollbar Customization */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { background: #00d2ff; border-radius: 10px; }

        </style>
        """,
        unsafe_allow_html=True
    )

apply_premium_theme()
# ---------------- Premium Tab Animation & Styling ----------------
st.markdown("""
    <style>
    /* main tab container */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* tab style */
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        padding: 0px 20px;
        border: none;
    }

    /* animation */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 210, 255, 0.1);
        color: #00d2ff;
        transform: translateY(-3px);
        text-shadow: 0px 0px 10px rgba(0, 210, 255, 0.5);
    }

    /*  (Active) */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        box-shadow: 0px 5px 15px rgba(0, 210, 255, 0.4);
        transform: scale(1.05);
    }

    /* tab*/
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }
    
    /* tab panel */
    .stTabs [data-baseweb="tab-panel"] {
        animation: fadeIn 0.8s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- Sidebar ----------------
st.sidebar.markdown("<h1 style='color: #00d2ff; font-size: 25px;'> Data Control Center⭐</h1>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Upload CSV Dataset", type=["csv"])
default_path = r"D:\Desktop\Group Project\india_air_quality.csv"  # Ensure this path is correct and the file exists

# ---------------- Load Data ----------------
try:
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Dataset Linked")
    else:
        data = pd.read_csv(default_path)
        st.sidebar.info("📂Active Dataset")
except:
    st.sidebar.warning("⚠️ CSV Connection Failed")
    data = pd.DataFrame()

# ---------------- Clean ----------------
if not data.empty:
    data.columns = data.columns.str.strip()
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

# ---------------- Filters ----------------
st.sidebar.markdown("---")
if not data.empty and "City" in data.columns:
    cities = ["All Cities"] + sorted(data["City"].dropna().unique())
    selected_city = st.sidebar.selectbox("Location Filter", cities)
else:
    selected_city = "All Cities"

if not data.empty and "Date" in data.columns:
    min_date, max_date = data["Date"].min(), data["Date"].max()
    date_range = st.sidebar.date_input("Time Range", [min_date, max_date])
else:
    date_range = None

pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "AQI"]
available_pollutants = [p for p in pollutants if p in data.columns]
pollutant = st.sidebar.selectbox("Metric for Time-Series", available_pollutants) if available_pollutants else None

city_data = data.copy()
if not data.empty:
    if selected_city != "All Cities" and "City" in data.columns:
        city_data = city_data[city_data["City"] == selected_city]
    if date_range and len(date_range) == 2 and "Date" in data.columns:
        city_data = city_data[(city_data["Date"] >= pd.to_datetime(date_range[0])) & 
                    (city_data["Date"] <= pd.to_datetime(date_range[1]))]


# ---------------- SESSION STATE ----------------
if "current_tab_index" not in st.session_state:
    st.session_state.current_tab_index = 0

if "auto_rotate" not in st.session_state:
    st.session_state.auto_rotate = False

if "paused" not in st.session_state:
    st.session_state.paused = False

if "last_switch" not in st.session_state:
    st.session_state.last_switch = time.time()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("🔄 Auto-Display Settings")
    st.session_state.auto_rotate = st.checkbox(
        "Auto-Rotation (10s)",
        value=st.session_state.auto_rotate
    )
    
    if st.session_state.auto_rotate:
        st.info("⏱️ Tabs will rotate every 10 seconds automatically.")
    else:
        st.success("🖱️ Manual Mode: Click tabs freely.")

            
 # ---------------- TABS DEFINITION ----------------
tab_home, tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs([
    "🏠 Home", "📊 Analytics", "📈 Trends",
    "🗺 Spatial Map", "🤖 AI Prediction","💬Smart Assistant", "📄 Dataset"
])

# ---------------- NEW AUTO TAB SWITCH (JS ONLY) ----------------
if st.session_state.auto_rotate:
    # Use timer to switch tabs every 10 seconds
    js_carousel = """
    <script>
    if (window.tabInterval) {
        clearInterval(window.tabInterval);
    }

    window.tabInterval = setInterval(function() {
        const tabs = window.parent.document.querySelectorAll('button[data-baseweb="tab"]');
        if (tabs.length > 0) {
            let activeIndex = -1;
            
            // Find the currently selected tab
            tabs.forEach((tab, index) => {
                if (tab.getAttribute('aria-selected') === 'true') {
                    activeIndex = index;
                }
            });

            // click the next tab
            let nextIndex = (activeIndex + 1) % tabs.length;
            tabs[nextIndex].click();
        }
    }, 10000); // 10,000 milliseconds = 10 seconds
    </script>
    """
    st.components.v1.html(js_carousel, height=0)
else:
    # Auto-rotation is off, ensure any existing intervals are cleared
    st.components.v1.html("<script>if(window.tabInterval){clearInterval(window.tabInterval);}</script>", height=0)


# ---------------- 🏠 Home Page ----------------
with tab_home:
    st.markdown("<h1 style='text-align: center;'>🌍 India Air Quality Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #00d2ff !important;'>Advanced Atmospheric Monitoring System</p>", unsafe_allow_html=True)
    st.write("---")
    
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f"""
        <div class="home-card">
            <h2>Welcome to the AQI Analytics Portal</h2>
            <p>This platform provides real-time environmental insights across major Indian cities. 
            Leveraging advanced Data Science and Machine Learning, we monitor air pollutants to help 
            policy makers and citizens breathe cleaner air.</p>
            <ul>
                <li><b>Real-time Tracking:</b> Monitor PM2.5, PM10, and NO2 levels.</li>
                <li><b>AI Predictions:</b> Estimate AQI using RandomForest regression models.</li>
                <li><b>Spatial Mapping:</b> Visualize pollution hotspots across the country.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 **Quick Tip:** Use the sidebar to upload your own dataset or filter by specific cities.")
        
    with col_h2:
        if not city_data.empty:
            st.metric("Coverage Scope", selected_city)
            st.metric("Data Volatility", f"{len(city_data)} Samples")
            if "AQI" in city_data.columns:
                avg_aqi = round(city_data["AQI"].mean(), 1)
                st.metric("Avg AQI Index", avg_aqi)

    # --- Live AQI Widget for Selected City ---
    st.write("---")
    if not city_data.empty and "AQI" in city_data.columns:
        latest_aqi = city_data["AQI"].iloc[-1]
        st.markdown(f"""
            <div style="background: rgba(0, 210, 255, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #00d2ff; text-align: center;">
                <h3 style="margin: 0; color: white;">📍 Current Live Status: {selected_city}</h3>
                <h1 style="margin: 10px 0; color: #00d2ff;">AQI: {latest_aqi}</h1>
                <p style="margin: 0; color: #e0e0e0;">Real-time monitoring active for this region.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- FAQ Section with Visual Icons ---
    st.markdown("<h2 style='color: #00d2ff; margin-top: 30px;'>🌍 Air Quality & Pollution: Common FAQs</h2>", unsafe_allow_html=True)

    # FAQ 1 - Icon: 📊
    with st.expander(" 1. What is AQI and how is it measured in India?"):
        st.write("""
        **Answer:** AQI stands for Air Quality Index. It is a tool used to communicate how polluted the air currently is or how polluted it is forecast to become. 
        In India, the National Air Quality Index tracks eight major pollutants: $PM_{10}$, $PM_{2.5}$, $NO_2$, $SO_2$, $CO$, $O_3$, $NH_3$, and $Pb$. 
        The index ranges from 0 to 500, where higher values indicate greater health risks.
        """)

    # FAQ 2 - Icon: ❄️
    with st.expander(" 2. Why does air quality worsen in North India during winter?"):
        st.write("""
        **Answer:** Several factors contribute to this seasonal spike. A meteorological phenomenon called **Temperature Inversion** traps pollutants close to the ground. 
        Additionally, the burning of crop residues (stubble burning) in neighboring states, lower wind speeds, and increased use of biomass for heating significantly 
        increase pollution levels during these months.
        """)

    # FAQ 3 - Icon: 🔬
    with st.expander(" 3. What is the difference between $PM_{2.5}$ and $PM_{10}$?"):
        st.write("""
        **Answer:** These refer to Particulate Matter based on their diameter.
        * **$PM_{10}$:** Particles with a diameter of 10 micrometers or less (e.g., dust, pollen).
        * **$PM_{2.5}$:** Fine particles with a diameter of 2.5 micrometers or less (e.g., combustion particles). 
        These are more dangerous as they can penetrate deep into the lungs and enter the bloodstream.
        """)

    # FAQ 4 - Icon: 🏭
    with st.expander(" 4. What are the primary sources of air pollution in Indian cities?"):
        st.write("""
        **Answer:** The major contributors include:
        * 🚗 **Transport:** Emissions from cars, trucks, and two-wheelers.
        * 🏭 **Industry:** Power plants and manufacturing units.
        * 🏗️ **Construction:** Dust from massive infrastructure projects.
        * 🗑️ **Waste Burning:** Open burning of municipal solid waste.
        """)

    # FAQ 5 - Icon: 😷
    with st.expander(" 5. How can citizens protect themselves when air quality is 'Poor' or 'Severe'?"):
        st.write("""
        **Answer:** When AQI levels are high, individuals should:
        * 🏃‍♂️ Minimize prolonged or heavy outdoor exertion.
        * 🏠 Keep windows closed to prevent outdoor air from entering.
        * 😷 Use **N95 or P100 respirators (masks)** if going outside is necessary.
        * 🌬️ Use indoor air purifiers with **HEPA filters**.
        """)

    # --- Call to Action ---
    st.write("---")
    st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3 style="color: white;">Ready to see the insights?</h3>
            <p style="color: #00d2ff; font-size: 18px;"><b>🚀 Explore the Data</b> to see the trends yourself and understand how air quality impacts your city!</p>
        </div>
    """, unsafe_allow_html=True)
    
# ---------------- 📊 Analytics (Combined with Chartboard) ----------------
with tab1:
    st.markdown("<h2 style='color:#00d2ff;'>📊 Performance Indicators & Insights</h2>", unsafe_allow_html=True)
    
    # --- Part 1: KPIs ---
    c1, c2, c3 = st.columns(3)
    def safe_mean(col):
        return round(city_data[col].mean(), 2) if not city_data.empty and col in city_data.columns else "N/A"
    
    c1.metric("PM2.5 (μg/m³)", safe_mean("PM2.5"))
    c2.metric("PM10 (μg/m³)", safe_mean("PM10"))
    c3.metric("AQI (Index Value)", safe_mean("AQI"))
    st.write("---")

    if not city_data.empty:
        # --- Part 2: National Comparison (Only when 'All Cities' is selected) ---
        if selected_city == "All Cities" and "City" in data.columns and "AQI" in data.columns:
            st.subheader("🌍 National Comparison")
            city_avg = city_data.groupby("City")["AQI"].mean().reset_index()
            st.plotly_chart(px.bar(city_avg, x="City", y="AQI", color="AQI", color_continuous_scale="Turbo", template="plotly_dark"), use_container_width=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("### 🔥 Top 5 High Pollution")
                st.plotly_chart(px.bar(city_avg.sort_values("AQI", ascending=False).head(5), x="City", y="AQI", color="AQI", color_continuous_scale="Reds", template="plotly_dark"), use_container_width=True)
            with col_b:
                st.markdown("### 🟢 Top 5 Cleanest")
                st.plotly_chart(px.bar(city_avg.sort_values("AQI").head(5), x="City", y="AQI", color="AQI", color_continuous_scale="Greens", template="plotly_dark"), use_container_width=True)

            st.subheader("⚖️ Benchmarking Tool")
            comp1, comp2 = st.columns(2)
            city1 = comp1.selectbox("City Alpha", city_avg["City"])
            city2 = comp2.selectbox("City Beta", city_avg["City"])
            st.plotly_chart(px.bar(city_avg[city_avg["City"].isin([city1, city2])], x="City", y="AQI", color="City", template="plotly_dark"), use_container_width=True)

        # --- Part 3: Region Analysis (When a specific city is selected) ---
        elif not city_data.empty:
            st.subheader(f"📍 Region Analysis: {selected_city}")
            if all(col in city_data.columns for col in ["PM2.5", "PM10", "AQI"]):
                p_df = pd.DataFrame({"Pollutant": ["PM2.5", "PM10", "AQI"], "Avg": [city_data["PM2.5"].mean(), city_data["PM10"].mean(), city_data["AQI"].mean()]})
                st.plotly_chart(px.bar(p_df, x="Pollutant", y="Avg", color="Avg", color_continuous_scale="Viridis", template="plotly_dark"), use_container_width=True)

        # --- Part 4: Integration of Chartboard (Distribution & Scatter) ---
        st.write("---")
        st.markdown("<h3 style='color:#00d2ff;'>📌 Visual Distribution & Correlation</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        # Chart 1: AQI Distribution Histogram
        with col1:
            st.subheader("📊 AQI Distribution")
            st.plotly_chart(
                px.histogram(
                    city_data.dropna(subset=["AQI"]),
                    x="AQI",
                    nbins=30,
                    color="City",
                    color_discrete_sequence=px.colors.sequential.Turbo,
                    template="plotly_dark"
                ),
                use_container_width=True
            )

        # Chart 2: PM2.5 vs AQI Scatter
        with col2:
            st.subheader("🌫 PM2.5 vs AQI")
            scatter_df = city_data.dropna(subset=["PM2.5", "AQI", "PM10"])
            if not scatter_df.empty:
                st.plotly_chart(
                    px.scatter(
                        scatter_df,
                        x="PM2.5",
                        y="AQI",
                        color="City",
                        size="PM10",
                        template="plotly_dark"
                    ),
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Not enough valid data for scatter plot.")

        # --- Part 5: Correlation Heatmap ---
        st.write("---")
        st.subheader("🧊 Variable Correlation Matrix")
        num_data = city_data.select_dtypes(include="number")
        if not num_data.empty:
            st.plotly_chart(px.imshow(num_data.corr(), text_auto=True, color_continuous_scale="RdBu_r", template="plotly_dark"), use_container_width=True)# ---------------- Trends ----------------
with tab2:
    st.subheader("📈 AQI Over Time")
    if "Date" in city_data.columns and "AQI" in city_data.columns:
            time_df = city_data.dropna(subset=["Date", "AQI"])
            st.plotly_chart(
                px.line(
                    time_df,
                    x="Date",
                    y="AQI",
                    color="City",
                    template="plotly_dark",
                    color_discrete_sequence=["#00d2ff"]
                ),
                use_container_width=True
            )
# ---------------- 🗺 Geospatial & Festival Analysis (Tab 3) ----------------
with tab3:
    if not data.empty and "City" in data.columns:
        # --- Section 1: Geospatial Hotspots (Original Map Code) ---
        st.subheader("🗺 Geospatial AQI Hotspots")
        st.write("Visualizing average air quality index across major geographical locations.")
        
        # Aggregating data for the map
        map_df = city_data.groupby("City")["AQI"].mean().reset_index()
        
        # Coordinates for mapping
        coords = {
            "Delhi": [28.61, 77.23], 
            "Mumbai": [19.07, 72.87], 
            "Kolkata": [22.57, 88.36],
            "Bengaluru": [12.97, 77.59],
            "Chennai": [13.08, 80.27],
            "Hyderabad": [17.38, 78.48],
            "Ahmedabad": [23.02, 72.57]
        }
        
        map_df["lat"] = map_df["City"].map(lambda x: coords.get(x, [20, 77])[0])
        map_df["lon"] = map_df["City"].map(lambda x: coords.get(x, [20, 77])[1])
        
        fig_map = px.scatter_mapbox(
            map_df, 
            lat="lat", 
            lon="lon", 
            size="AQI", 
            color="AQI", 
            color_continuous_scale="Plasma", 
            zoom=3,
            hover_name="City"
        )
        fig_map.update_layout(mapbox_style="carto-darkmatter", template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("---") 

        # --- Section 2: Holiday & Festival Pollution Trends ---
        st.subheader("🎉 Holiday & Festival Pollution Trends")
        st.write("Tracking air quality fluctuations during major national festivals.")

        if "Date" in city_data.columns and "AQI" in city_data.columns:
            fest_df = city_data.copy()
            fest_df['Date'] = pd.to_datetime(fest_df['Date'])
            
            # Line Chart
            fig_fest = px.line(
                fest_df.sort_values("Date"), 
                x="Date", 
                y="AQI", 
                color="City",
                title="AQI Variation During Festival Timelines",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            # Festival dates
            festivals = {
                'Diwali': ['2015-11-11', '2016-10-30', '2017-10-19', '2018-11-07', '2019-10-27', '2020-11-14'],
                'Holi': ['2015-03-06', '2016-03-24', '2017-03-13', '2018-03-02', '2019-03-21', '2020-03-09']
            }

            # Fix: Adding vertical lines using formatted strings to avoid Timestamp addition error
            for fest_name, dates in festivals.items():
                for d in dates:
                    target_date = pd.to_datetime(d)
                    if target_date >= fest_df['Date'].min() and target_date <= fest_df['Date'].max():
                        fig_fest.add_vline(
                            x=target_date.timestamp() * 1000, # Convert to milliseconds for Plotly
                            line_width=1.5, 
                            line_dash="dash", 
                            line_color="#FFA500",
                            annotation_text="Event", 
                            annotation_position="top left"
                        )
            
            st.plotly_chart(fig_fest, use_container_width=True)
            
            st.info("""
                **Analysis Insight:** The orange dashed lines mark major festival periods. 
                Spikes often indicate increased pollution during these specific timelines.
            """)
    else:
        st.error("Insufficient data for analysis.")

# ---------------- 🤖 Prediction (UPGRADED UI WITH ANATOMY) ----------------
with tab4:
    st.markdown("<h3 class='section-header'>🤖 AI AQI Predictor & Body Impact</h3>", unsafe_allow_html=True)
    needed = ["PM2.5", "PM10", "NO2", "SO2", "CO", "AQI"]

    if all(col in city_data.columns for col in needed):
        df = city_data[needed].dropna()
        if len(df) < 10:
            st.warning("⚠️ Not enough data for prediction in this region.")
        else:
            # Model Training
            X = df[["PM2.5", "PM10", "NO2", "SO2", "CO"]]
            y = df["AQI"]

            model = RandomForestRegressor()
            model.fit(X, y)

            y_pred = model.predict(X)
            score = r2_score(y, y_pred)
            st.markdown(f"<p style='color:#00d2ff;'>Model Confidence (R²): <b>{round(score,2)}</b></p>", unsafe_allow_html=True)

            # Feature Importance Chart
            importance = pd.DataFrame({"Feature": X.columns, "Importance": model.feature_importances_})
            fig_imp = px.bar(importance, x="Feature", y="Importance", color="Importance", 
                             color_continuous_scale="blues", template="plotly_dark", title="Pollutant Impact Factor")
            st.plotly_chart(fig_imp, use_container_width=True)

            # Sliders for Prediction
            st.markdown("<h4 style='color:#3a7bd5;'>Set Pollutant Levels</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                pm25 = st.slider("PM2.5", 0, 500, 50)
                so2 = st.slider("SO2", 0, 200, 20)
            with col2:
                pm10 = st.slider("PM10", 0, 500, 80)
                co = st.slider("CO", 0, 10, 1)
            with col3:
                no2 = st.slider("NO2", 0, 200, 30)

            # Prediction Execution
            if st.button("🚀 Execute Prediction"):
                pred = model.predict([[pm25, pm10, no2, so2, co]])
                st.session_state['pred_val'] = round(pred[0], 2)

            # --- Result Display & Health Impact Section ---
            if 'pred_val' in st.session_state:
                pred_val = st.session_state['pred_val']

                # AQI Result Display Box
                st.markdown(f"""
                <div class="prediction-box" style="background: rgba(0, 210, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #00d2ff; margin-bottom: 20px;">
                    <h2 style='color: white; margin: 0;'>Estimated AQI Result</h2>
                    <h1 style='color: #00d2ff; font-size: 50px; margin: 10px 0;'>{pred_val}</h1>
                </div>
                """, unsafe_allow_html=True)

                # Adjusted Status Messages (Poor and Severe Separated)
                if pred_val <= 50: 
                    st.success("🟢 Quality: Good")
                elif pred_val <= 100: 
                    st.info("🔵 Quality: Satisfactory")
                elif pred_val <= 200:
                    st.warning("🟡 Quality: Moderate")
                elif pred_val <= 300:
                    st.error("🟠 Quality: Poor")
                else: 
                    st.error("🔴 Quality: Severe")

                # ---------------- Health Impact Section ----------------
                st.markdown("---") 
                st.markdown("<h4 style='color:#00d2ff; margin-top:30px;'>🩺 Health Impact Analysis</h4>", unsafe_allow_html=True)

                # 1. Image Paths
                img_good = r"D:\Desktop\Group Project\good.jpeg"
                img_Satisfactory = r"D:\Desktop\Group Project\satisfactory.jpeg"
                img_moderate = r"D:\Desktop\Group Project\moderate.jpeg"
                img_Poor = r"D:\Desktop\Group Project\poor.jpeg"
                img_severe = r"D:\Desktop\Group Project\sever.jpeg"

                # 2. Impact Logic (Poor and Severe Separated)
                if pred_val <= 50:
                    impact_data = {"status": "Good", "effect": "Minimal impact. Organs are safe.", "advice": "Enjoy your outdoor activities.", "color": "#28a745"}
                    img_path = img_good
                    brain, heart, lungs = "Healthy ✅", "Normal ✅", "Clear ✅"

                elif pred_val <= 100:
                    impact_data = {"status": "Satisfactory", "effect": "Minor discomfort to sensitive people.", "advice": "Sensitive people should reduce exertion.", "color": "#17a2b8"}
                    img_path = img_Satisfactory
                    brain, heart, lungs = "Healthy ✅", "Normal ✅", "Clear ✅"

                elif pred_val <= 200:
                    impact_data = {"status": "Moderate", "effect": "Breathing discomfort to children and elderly.", "advice": "Consider reducing intense outdoor exercise.", "color": "#ffc107"}
                    img_path = img_moderate
                    brain, heart, lungs = "Mild Inflammation ⚠️", "Strained ⚠️", "Minor Irritation ⚠️"

                elif pred_val <= 300:
                    impact_data = {"status": "Poor", "effect": "Discomfort on prolonged exposure and breathing issues.", "advice": "Avoid long outdoor exertion; wear a mask.", "color": "#fd7e14"}
                    img_path = img_Poor 
                    brain, heart, lungs = "High Risk 🔴", "Cardiovascular Threat 🔴", "Severely Impacted 🔴"

                else:
                    impact_data = {"status": "Severe", "effect": "Seriously impacts healthy people. Respiratory danger.", "advice": "Stay indoors. Use air purifiers and medical masks.", "color": "#dc3545"}
                    img_path = img_severe
                    brain, heart, lungs = "Critical Risk 🚨", "Extreme Heart Strain 🚨", "Severe Respiratory Damage 🚨"

                # 3. Layout: Columns
                col_photo, col_info = st.columns([1, 1.8])

                with col_photo:
                    try:
                        st.image(img_path, use_container_width=True, caption=f"Status: {impact_data['status']}")
                    except:
                        st.error(f"Error: Image path not found at {img_path}")

                with col_info:
                    st.markdown(f"""
                    <div style="border-left: 10px solid {impact_data['color']}; background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px;">
                        <h5 style="color: {impact_data['color']}; margin-top:0;">Current Status: {impact_data['status']}</h5>
                        <p style="color: white; margin-bottom: 5px;"><b>Potential Health Effect:</b> {impact_data['effect']}</p>
                        <p style="color: #00d2ff; margin-bottom: 0px;"><b>💡 Precautionary Advice:</b> {impact_data['advice']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<h5 style='color:white; margin-top:15px;'>Organ Alert Status:</h5>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
                        <p style="color: white; margin-bottom: 5px; font-size: 14px;">🧠 <b>Brain:</b> {brain}</p>
                        <p style="color: white; margin-bottom: 5px; font-size: 14px;">🫀 <b>Heart:</b> {heart}</p>
                        <p style="color: white; margin-bottom: 0px; font-size: 14px;">🫁 <b>Lungs:</b> {lungs}</p>
                    </div>
                    """, unsafe_allow_html=True)

    else:
        st.warning("Required pollutant columns missing from dataset.")
        
# ---------------- FINAL AQI CHATBOT (CSV + FLOATING UI) ----------------

import pandas as pd
import streamlit as st

with tab5:
    # Load CSV file
    df = pd.read_csv("AQI of City.csv")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    def get_ai_response(user_input):
        user_input = user_input.lower()

        # 🔹 AQI number meaning
        words = user_input.split()
        for word in words:
            if word.isdigit():
                aqi = int(word)
                if aqi <= 50:
                    status = "Good"
                elif aqi <= 100:
                    status = "Satisfactory"
                elif aqi <= 200:
                    status = "Moderate"
                elif aqi <= 300:
                    status = "Poor"
                else:
                    status = "Very Poor"

                return f"AQI {aqi} means {status} air quality. Take precautions accordingly."

        # 🔹 City AQI
        for index, row in df.iterrows():
            city = str(row["City"]).lower()
            # SAFE conversion of AQI
            try:
                aqi = int(row["AQI"])
            except (ValueError, TypeError):
                aqi = 0  # fallback if AQI is not numeric

            if city in user_input:
                if aqi <= 50:
                    status = "Good"
                elif aqi <= 100:
                    status = "Satisfactory"
                elif aqi <= 200:
                    status = "Moderate"
                elif aqi <= 300:
                    status = "Poor"
                else:
                    status = "Very Poor"

                return f"The AQI of {city.title()} is {aqi}, which is {status} air quality."

        # 🔹 Basic AQI info
        if "aqi" in user_input:
            return "AQI (Air Quality Index) measures how polluted the air is."

        # 🔹 Pollution basics
        elif "pollution" in user_input:
            return "Air pollution is caused by vehicles, industries, dust and burning fuels."

        elif "solution" in user_input or "control" in user_input:
            return "To reduce pollution: use public transport, plant trees, and avoid burning waste."

        # 🔹 Health impacts
        elif "health impact" in user_input or "effects" in user_input:
            return "Air pollution can cause asthma, lung disease, heart problems and irritation."

        elif "health" in user_input:
            return "Air pollution can cause asthma, breathing problems and heart diseases."

        elif "symptoms" in user_input:
            return "Symptoms include coughing, throat irritation, breathing difficulty and eye irritation."

        elif "long term" in user_input:
            return "Long-term exposure can cause chronic lung disease and heart problems."

        elif "short term" in user_input:
            return "Short-term exposure causes irritation and breathing issues."

        # 🔹 Sensitive groups
        elif "child" in user_input or "children" in user_input:
            return "Children are highly sensitive to pollution. Keep them indoors during high AQI."

        elif "elderly" in user_input or "old" in user_input:
            return "Elderly people should avoid outdoor exposure and use masks."

        elif "pregnant" in user_input:
            return "Pregnant women should avoid polluted air for safety."

        # 🔹 Protection
        elif "protect" in user_input or "protection" in user_input:
            return "Use masks, avoid outdoor exposure, use air purifiers and stay indoors."

        elif "mask" in user_input:
            return "N95 masks help protect from harmful particles."

        elif "exercise" in user_input:
            return "Avoid outdoor exercise during high pollution."

        elif "indoor air" in user_input:
            return "Improve indoor air with ventilation and plants."

        # 🔹 Pollutants
        elif "pm2.5" in user_input:
            return "PM2.5 are tiny harmful particles that enter deep into lungs."

        elif "pm10" in user_input:
            return "PM10 are larger particles affecting upper respiratory system."

        elif "so2" in user_input or "sulphur dioxide" in user_input:
            return "SO2 is produced by burning fuels and irritates lungs."

        elif "co" in user_input or "carbon monoxide" in user_input:
            return "CO is a harmful gas that reduces oxygen in the body."

        elif "no2" in user_input:
            return "NO2 comes from vehicles and damages lungs."

        elif "o3" in user_input or "ozone" in user_input:
            return "Ozone causes coughing and throat irritation."

        # 🔹 AQI safety
        elif "safe aqi" in user_input:
            return "AQI below 50 is safe."

        elif "dangerous aqi" in user_input:
            return "AQI above 300 is hazardous."

        return "Ask me about AQI, cities, pollution, or health."


    # Show chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask about Air Quality...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        reply = get_ai_response(user_input)

        st.session_state.messages.append({"role": "assistant", "content": reply})

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Dataset ----------------
with tab6:
    st.dataframe(city_data, use_container_width=True)
    st.download_button("📥 Export Report as CSV", city_data.to_csv(index=False), "AQI_Report.csv")

st.markdown("<p style='text-align: center; opacity: 0.6;'>Professional India AQI Dashboard v2.0 | Built with Streamlit & AI</p>", unsafe_allow_html=True)