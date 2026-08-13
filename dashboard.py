import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"

def dapatkan_status_blynk(pin):
    """BACA status pin semasa dari Blynk Cloud (0 atau 1)"""
    url = f"https://sgp1.blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            return int(res.text)  # Pulangkan 0 atau 1
    except Exception:
        pass
    return 0

def kawal_blynk(pin, value):
    """HANTAR arahan ON/OFF ke Blynk Cloud"""
    url = f"https://sgp1.blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        res = requests.get(url, timeout=3)
        return res.status_code == 200
    except Exception:
        return False

# --- SETTING PAGE ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠", layout="centered")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.divider()

# --- INITIALIZE STATE (SYNC DENGAN BLYNK) ---
if "s1_state" not in st.session_state:
    # Semak status asal dari server Blynk bila first time buka
    st.session_state.s1_state = bool(dapatkan_status_blynk("V0"))

col1, col2, col3 = st.columns(3)

# --- SWITCH 1: LAMPU UTAMA ---
with col1:
    st.subheader("💡 Lampu Utama (V0)")
    
    # Toggle ikut status semasa Blynk
    suis_1 = st.toggle("Lampu 1", value=st.session_state.s1_state, key="s1")
    
    # Hanya hantar signal KALAU user ubah kedudukan suis
    if suis_1 != st.session_state.s1_state:
        status_baru = 1 if suis_1 else 0
        if kawal_blynk("V0", status_baru):
            st.session_state.s1_state = suis_1
            st.rerun()
        else:
            st.error("Gagal sambung ke Blynk")

    if st.session_state.s1_state:
        st.success("Lampu ON!")
    else:
        st.info("Lampu OFF")

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
st.info(f"📊 Jumlah peralatan aktif: **{sum([st.session_state.s1_state, suis_2, suis_3])}**")