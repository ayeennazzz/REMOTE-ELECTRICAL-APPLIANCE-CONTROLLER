import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT80giEz8x"

def kawal_blynk(pin, value):
    """Fungsi untuk hantar arahan ON/OFF ke Blynk dengan fallback server"""
    # Senarai server Blynk mengikut region (Asia / Global / US)
    servers = [
        "https://blynk.cloud/external/api",
        "https://sgp1.blynk.cloud/external/api",  # Server Asia (Malaysia selalu guna ni)
        "https://ny3.blynk.cloud/external/api"
    ]
    
    success = False
    for server in servers:
        url = f"{server}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                success = True
                break  # Berjaya hantar, keluar dari loop
        except Exception:
            continue
            
    return success

# --- SETTING PAGE ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal rumah anda di sini.")
st.divider()

# --- DASHBOARD LAYOUT (3 SWITCH) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💡 Lampu Utama (V1)")
    suis_1 = st.toggle("Lampu 1", key="s1")
    if suis_1:
        if kawal_blynk("v1", 1):
            st.success("Lampu ON!")
        else:
            st.warning("Gagal sambung ke Blynk")
    else:
        if kawal_blynk("v1", 0):
            st.error("Lampu OFF!")
        else:
            st.warning("Gagal sambung ke Blynk")

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
st.info(f"Jumlah peralatan aktif: {sum([suis_1, suis_2, suis_3])}")