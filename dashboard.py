import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "wIox1rws2c9kenuLFQJjgJKv0zYre1sx"
# BLYNK_URL = "https://blynk.cloud/external/api" # URL Standard Blynk

def kawal_blynk(pin, value):
    """Fungsi untuk hantar arahan ON/OFF ke Blynk"""
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        return False

# --- SETTING PAGE ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal rumah anda di sini.")
st.divider()

# --- DASHBOARD LAYOUT (3 SWITCH) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💡 Lampu Utama (Pin V1)")
    # Bila suis diubah, dia hantar 1 (ON) atau 0 (OFF) ke Virtual Pin V1 Blynk
    suis_1 = st.toggle("Lampu 1", key="s1")
    if suis_1:
        kawal_blynk("v1", 1)
        st.success("ON")
    else:
        kawal_blynk("v1", 0)
        st.error("OFF")

with col2:
    st.subheader("🍳 Dapur")
    suis_2 = st.toggle("Lampu 2", key="s2")
    # Boleh tambah v2 nanti bila hardware dah ready
    if suis_2:
        st.success("ON")
    else:
        st.error("OFF")

with col3:
    st.subheader("🌀 Kipas")
    suis_3 = st.toggle("Kipas Siling", key="s3")
    # Boleh tambah v3 nanti
    if suis_3:
        st.success("ON")
    else:
        st.error("OFF")

st.divider()
st.info(f"Jumlah peralatan aktif: {sum([suis_1, suis_2, suis_3])}")