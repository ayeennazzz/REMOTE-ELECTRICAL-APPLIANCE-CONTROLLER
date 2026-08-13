import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"

def kawal_blynk(pin, value):
    """Hantar arahan ON/OFF ke Blynk Cloud API"""
    urls = [
        f"https://sgp1.blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}",
        f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    ]
    
    for url in urls:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return True
        except Exception:
            continue
            
    return False

# --- SETTING PAGE ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠", layout="centered")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.divider()

col1, col2, col3 = st.columns(3)

# --- SWITCH 1: LAMPU UTAMA (KITA GUNA V0 SEKARANG!) ---
with col1:
    st.subheader("💡 Lampu Utama (V0)")
    suis_1 = st.toggle("Lampu 1", key="s1")
    
    if suis_1:
        if kawal_blynk("V0", 1): # <--- SEKARANG V0!
            st.success("Lampu ON!")
        else:
            st.error("Gagal sambung ke Blynk")
    else:
        if kawal_blynk("V0", 0): # <--- SEKARANG V0!
            st.info("Lampu OFF")
        else:
            st.error("Gagal sambung ke Blynk")

with col2:
    st.subheader("🍳 Dapur")
    suis_2 = st.toggle("Lampu 2", key="s2")
    if suis_2:
        st.success("ON")
    else:
        st.info("OFF")

with col3:
    st.subheader("🌀 Kipas")
    suis_3 = st.toggle("Kipas Siling", key="s3")
    if suis_3:
        st.success("ON")
    else:
        st.info("OFF")

st.divider()
st.info(f"📊 Jumlah peralatan aktif: **{sum([suis_1, suis_2, suis_3])}**")