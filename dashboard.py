import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
# Pastikan Auth Token ni SAMA dengan yang kat Arduino IDE
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT80giEz8x"

def kawal_blynk(pin, value):
    """Fungsi untuk hantar arahan ON/OFF ke Blynk Cloud API"""
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            # Pop-up error kalau token tak sah / server response code lain
            st.toast(f"❌ Error Blynk ({response.status_code})")
            return False
    except Exception as e:
        # Pop-up error kalau tiada sambungan internet
        st.toast(f"⚠️ Masalah Rangkaian: {e}")
        return False

# --- SETTING PAGE STREAMLIT ---
st.set_page_config(
    page_title="Smart Home Ain",
    page_icon="🏠",
    layout="centered"
)

# --- HEADER DASHBOARD ---
st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.divider()

# --- DASHBOARD LAYOUT (3 SWITCH) ---
col1, col2, col3 = st.columns(3)

# --- SWITCH 1: LAMPU UTAMA (V1) ---
with col1:
    st.subheader("💡 Lampu (V1)")
    suis_1 = st.toggle("Lampu 1", key="s1")
    
    if suis_1:
        if kawal_blynk("v1", 1):
            st.success("Lampu ON")
        else:
            st.warning("Gagal sambung")
    else:
        if kawal_blynk("v1", 0):
            st.error("Lampu OFF")
        else:
            st.warning("Gagal sambung")

# --- SWITCH 2: DAPUR ---
with col2:
    st.subheader("🍳 Dapur")
    suis_2 = st.toggle("Lampu 2", key="s2")
    if suis_2:
        st.success("ON")
    else:
        st.error("OFF")

# --- SWITCH 3: KIPAS ---
with col3:
    st.subheader("🌀 Kipas")
    suis_3 = st.toggle("Kipas Siling", key="s3")
    if suis_3:
        st.success("ON")
    else:
        st.error("OFF")

st.divider()

# --- FOOTER STATUS ---
jumlah_aktif = sum([suis_1, suis_2, suis_3])
st.info(f"📊 Jumlah peralatan aktif: **{jumlah_aktif}**")