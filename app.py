import streamlit as st
from fpdf import FPDF
from Expert_system import run_diet_expert_system

# --- 1. Page Configuration ---
st.set_page_config(page_title="Vitaplan Diet System", layout="centered")

# --- Function to Generate PDF ---
def create_pdf(diet_type, reason, plan_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="VITAPLAN DIET SYSTEM - YOUR PERSONAL PLAN", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Diet Type: {diet_type}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Why this plan?", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, txt=reason)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Suggested Meal Plan:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, txt=plan_text)
    return pdf.output(dest='S')

# --- 2. CSS Design ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #2e026d, #15162c, #4e44ce, #2e026d);
        background-size: 400% 400%;
        color: white;
    }
    .welcome-text {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 60px !important;
        font-weight: 800;
        background: linear-gradient(to right, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .header-text { color: #00dbde; font-size: 35px; font-weight: bold; text-align: center; }
    .stButton>button {
        background: linear-gradient(45deg, #7b2ff7, #2196f3);
        color: white; border: none; border-radius: 50px;
        font-weight: bold; font-size: 20px; width: 100%;
    }
    label, p, .stMarkdown { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Page Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# --- PAGE 1: Welcome ---
if st.session_state.page == 'welcome':
    st.markdown('<h1 class="welcome-text">WELCOME TO <br> VITAPLAN DIET SYSTEM</h1>', unsafe_allow_html=True)
    if st.button("🚀 ENTER"):
        st.session_state.page = 'info'
        st.rerun()

# --- PAGE 2: Info ---
elif st.session_state.page == 'info':
    st.markdown('<h2 class="header-text">🌟 Health Knowledge Hub 🌟</h2>', unsafe_allow_html=True)
    st.write("Balanced nutrition fuels your dreams and gives you energy!")
    if st.button("📝 NEXT: ENTER DATA"):
        st.session_state.page = 'data'
        st.rerun()

# --- PAGE 3: Data ---
elif st.session_state.page == 'data':
    st.markdown('<h2 class="header-text" style="color: #fc00ff;">⚙️ PERSONAL METRICS</h2>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    h = c1.number_input("Height (cm)", 0, 250, 0)
    w = c2.number_input("Weight (kg)", 0, 250, 0)
    
    g = st.selectbox("Your Goal", ["Select Goal", "Weight Loss", "Weight Gain", "Maintenance"])
    a = st.selectbox("Activity Level", ["Select Activity", "Low", "Moderate", "Very Active"])
    c = st.text_input("Medical Condition", placeholder="e.g., Diabetes, PCOS, None")

    if st.button("🔥 GENERATE MY PLAN"):
        if h == 0 or w == 0 or g == "Select Goal":
            st.error("Please fill in all data.")
        else:
            u_data = {"weight": w, "height": h, "goal": g, "condition": c, "activity": a}
            res = run_diet_expert_system(u_data)
            
            st.divider()
            st.success(f"Diet Type: {res['diet_type']}")
            st.info(f"BMI: {res['bmi']} | Reasoning: {res['reasoning']}")
            
            st.write("#### Meals:")
            for m in res['suggested_meals']: st.write(m)
            
            st.write("#### Exercises:")
            for ex in res['suggested_exercises']: st.write(ex)
            
            st.warning(f"Advice: {res['general_advice']}")

            p_text = "Meals:\n" + "\n".join(res['suggested_meals']) + "\n\nExercises:\n" + "\n".join(res['suggested_exercises'])
            p_raw = create_pdf(res['diet_type'], res['reasoning'], p_text)
            # نقوم بتحويل bytearray إلى bytes ليرضى عنها streamlit
            p_bytes = bytes(p_raw) 

            st.download_button(
                label="📥 Download PDF", 
                data=p_bytes, 
                file_name="Plan.pdf", 
                mime="application/pdf"
)
    
    if st.button("🏠 BACK TO HOME"):
        st.session_state.page = 'welcome'
        st.rerun()