import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"

def kawal_blynk(pin, value):
    """Fungsi untuk hantar arahan ON/OFF ke Blynk Cloud API"""
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            st.toast(f"❌ Error Blynk ({response.status_code})")
            return False
    except Exception as e:
        st.toast(f"⚠️ Masalah Rangkaian: {e}")
        return False

# --- SETTING PAGE STREAMLIT ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠", layout="centered")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.divider()

col1, col2, col3 = st.columns(3)

# --- SWITCH 1: LAMPU UTAMA (V1 -> HURUF BESAR) ---
with col1:
    st.subheader("💡 Lampu (V1)")
    suis_1 = st.toggle("Lampu 1", key="s1")
    
    if suis_1:
        if kawal_blynk("V1", 1):  # <--- GUNA "V1" (HURUF BESAR)
            st.success("Lampu ON")
        else:
            st.warning("Gagal sambung")
    else:
        if kawal_blynk("V1", 0):  # <--- GUNA "V1" (HURUF BESAR)
            st.error("Lampu OFF")
        else:
            st.warning("Gagal sambung")

with col2:
    st.subheader("🍳 Dapur")
    suis_2 = st.toggle("Lampu 2", key="s2")
    if suis_2:
        st.success("ON")
    else:
        st.error("OFF")

with col3:
    st.subheader("🌀 Kipas")
    suis_3 = st.toggle("Kipas Siling", key="s3")
    if suis_3:
        st.success("ON")
    else:
        st.error("OFF")

st.divider()
jumlah_aktif = sum([suis_1, suis_2, suis_3])
st.info(f"📊 Jumlah peralatan aktif: **{jumlah_aktif}**")