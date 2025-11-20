########################################################
# 1. Import the necessary libraries
########################################################
import streamlit as st
import plotly.graph_objects as go 
from ai.agent import call_ai
from ai.prompts import SYSTEM_PROMPT

########################################################
# 2. Set the page config
########################################################
st.set_page_config(
    page_title="AXIS | Data Intelligence",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- INJECT CUSTOM CSS (Orbital Luxury Visual Layer) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        color: #EAEAEA;
    }
    /* Background: Deep Space Navy Gradient */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1c2541 0%, #0B1026 100%);
    }
    /* Inputs: Glassmorphism */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(11, 16, 38, 0.8);
        color: #EAEAEA;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 10px;
    }
    /* Buttons: Gold Outline */
    .stButton > button {
        border: 1px solid #D4AF37;
        color: #D4AF37;
        background-color: transparent;
        border-radius: 20px; 
        padding-left: 20px;
        padding-right: 20px;
    }
    .stButton > button:hover {
        background-color: #D4AF37;
        color: #0B1026;
    }
    /* Titles */
    h1 {
        font-weight: 300 !important;
        letter-spacing: 0.1rem !important;
    }
    /* Secure Status Badge */
    .status-badge {
        display: inline-block;
        padding: 5px 15px;
        border: 1px solid #D4AF37;
        border-radius: 20px;
        color: #D4AF37;
        font-size: 0.8em;
        letter-spacing: 0.1em;
        background: rgba(212, 175, 55, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER: Style Charts (Multi-Color Palette) ---
# AXIS GRAPH COLOR PALETTE: Gold, Cyan, Orchid, Orange, Silver
import plotly.graph_objects as go

# --- AXIS GRAPH COLOR PALETTE ---
AXIS_COLORS = ['#D4AF37', '#00FFFF', '#C874FF', '#FF8C00', '#C0C0C0'] 

def style_chart(fig):
    if not isinstance(fig, go.Figure):
        return fig
    
    # 1. Layout Adjustments (Transparency and Fonts)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#EAEAEA',
        font_family='Montserrat',
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=False),
    )
    
    # 2. Trace Color Cycling (Applying the new palette)
    if fig.data:
        for i, trace in enumerate(fig.data):
            # Cycle through the AXIS_COLORS palette for single colors
            color = AXIS_COLORS[i % len(AXIS_COLORS)]
            
            # --- CORRECTED LOGIC ---
            if trace.type == 'pie':
                # FIX: Pie charts MUST use the plural 'colors' property set to a list
                trace.marker.colors = AXIS_COLORS
            
            elif trace.type == 'bar':
                # Bar charts use the singular 'color' property on the trace, 
                # often initialized to the trace itself.
                trace.marker.color = color
                
            elif trace.type == 'scatter':
                # Scatter (line) charts use the singular 'color' property
                trace.line.color = color
                trace.marker.color = color
            # --- END CORRECTED LOGIC ---

    return fig


# Branding Header
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>A X I S</h1>", unsafe_allow_html=True)

########################################################
# 3. Ensure session state keys exist
########################################################
if "connection_string" not in st.session_state:
    st.session_state["connection_string"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "messages_ai" not in st.session_state:
    st.session_state["messages_ai"] = []
if "messages_streamlit" not in st.session_state:
    st.session_state["messages_streamlit"] = []

########################################################
# 4. Handle connection input
########################################################
if not st.session_state["connection_string"]:
    
    # Persona Greeting
    st.markdown("<div style='text-align: center; margin-bottom: 20px; font-size: 1.1em;'>Hello. I am Axis. Please connect your database so I can assist you.</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # SECURITY CHANGE: Using st.text_input with type='password' to mask input
        connection_input = st.text_input(
            "Connection Key",
            placeholder="mysql+pymysql://user:password@localhost:3306/db_name",
            label_visibility="collapsed",
            type="password" 
        )

        if st.button("Connect", use_container_width=True):
            if connection_input.strip():
                st.session_state["connection_string"] = connection_input.strip()
                
                # AXIS INITIAL GREETING (Genius Assistant Persona)
                initial_msg = "I am connected to the database. How can I help you today?"
                
                st.session_state["messages_ai"] = [
                    {"role": "system", "content": SYSTEM_PROMPT()},
                    {"role": "assistant", "content": initial_msg}
                ]
                st.session_state["messages_streamlit"] = [
                    {"role": "assistant", "content": {"type": "text", "text": initial_msg}}
                ]
                st.success("Connection verified.")
                st.rerun()
            else:
                st.error("Please enter a valid connection string.")

else:
    ########################################################
    # 5. Display current connection and chat interface
    ########################################################
    
    # SECURITY CHANGE: Replaced connection string display with Status Badge
    st.markdown(f"""
        <div style='opacity: 0.8; font-size: 0.8em; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;'>
            <span class="status-badge">🟢 SECURE DATA UPLINK ESTABLISHED</span>
        </div>
    """, unsafe_allow_html=True)

    # Disconnect logic
    with st.sidebar:
        if st.button("Disconnect"):
            st.session_state["connection_string"] = None
            st.session_state["messages_ai"] = []
            st.session_state["messages_streamlit"] = []
            st.rerun()

    ########################################################
    # 6. Display the conversation history
    ########################################################
    for msg in st.session_state["messages_streamlit"]:
        # Avatar: Axis (💠) vs User (None)
        avatar = "💠" if msg["role"] == "assistant" else None
        
        if msg.get("role") == "assistant":
            content = msg.get("content", {})
            if content.get("type") == "text":
                st.chat_message(msg["role"], avatar=avatar).write(content["text"])
            elif content.get("type") == "dataframe":
                with st.chat_message(msg["role"], avatar=avatar):
                    with st.expander("View Query Logic"):
                        st.code(content["sql_query"], language="sql")
                    st.dataframe(content["dataframe"])
            elif content.get("type") == "chart":
                with st.chat_message(msg["role"], avatar=avatar):
                    with st.expander("View Query Logic"):
                        st.code(content["sql_query"], language="sql")
                    # Styling the chart on the fly
                    styled_fig = style_chart(content["chart"])
                    st.plotly_chart(styled_fig, use_container_width=True)
                
        elif msg.get("role") == "user":
            st.chat_message(msg["role"]).write(msg["content"])


    ########################################################
    # 7. Send a new message
    ########################################################

    # User Prompt
    prompt = st.chat_input("Ask Axis...")

    if prompt:
        # Add user message
        st.session_state["messages_ai"].append({"role": "user", "content": prompt})
        st.session_state["messages_streamlit"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get response from your agent
        with st.spinner("Thinking..."):
            response = call_ai(st.session_state["messages_ai"])

        # Add assistant response
        st.session_state["messages_ai"].append(response['ai'])
        st.session_state["messages_streamlit"].append(response['streamlit'])
       
        # Display assistant response
        msg = response['streamlit']
        avatar = "💠"
        
        if msg["role"] == "assistant":
            content = msg["content"]
            if content.get("type") == "text":
                st.chat_message(msg["role"], avatar=avatar).write(content["text"])
            elif content.get("type") == "dataframe":
                with st.chat_message(msg["role"], avatar=avatar):
                    with st.expander("View Query Logic"):
                        st.code(content["sql_query"], language="sql")
                    st.dataframe(content["dataframe"])
            elif content.get("type") == "chart":
                with st.chat_message(msg["role"], avatar=avatar):
                    with st.expander("View Query Logic"):
                        st.code(content["sql_query"], language="sql")
                    styled_fig = style_chart(content["chart"])
                    st.plotly_chart(styled_fig, use_container_width=True)
                    st.markdown(f"**Chart Explanation:** {content.get('explanation', '')}")
                
        elif msg.get("role") == "user":
            st.chat_message(msg["role"]).write(msg["content"])