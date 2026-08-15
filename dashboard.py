import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"

def dapatkan_status_blynk(pin):
    """BACA status pin semasa dari Blynk Cloud secara pantas"""
    url = f"https://sgp1.blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 200:
            return int(res.text.strip())
    except Exception:
        pass
    return 0

def kawal_blynk(pin, value):
    """HANTAR arahan ON/OFF ke Blynk Cloud"""
    url = f"https://sgp1.blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        res = requests.get(url, timeout=2)
        return res.status_code == 200
    except Exception:
        return False

# --- SETTING PAGE ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠", layout="centered")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.caption("⚡ *Live Auto-Sync aktif (status dikemaskini automatik setiap 2 saat).*")
st.divider()

# --- BLOK AUTO-SYNC SETIAP 2 SAAT ---
@st.fragment(run_every="2s")
def live_dashboard():
    # 1. Tarik status sebenar dari Blynk Cloud
    status_v0 = bool(dapatkan_status_blynk("V0"))
    
    col1, col2, col3 = st.columns(3)

    # --- SWITCH 1: LAMPU UTAMA (V0) ---
    with col1:
        st.subheader("💡 Lampu (V0)")
        
        # Switch sentiasa ikut status semasa Blynk
        suis_1 = st.toggle("Lampu 1", value=status_v0, key="suis_v0")
        
        # Jika ditekan oleh user (berbeza dari status server)
        if suis_1 != status_v0:
            status_baru = 1 if suis_1 else 0
            kawal_blynk("V0", status_baru)
            st.rerun()

        if status_v0:
            st.success("Lampu ON! 💡")
        else:
            st.info("Lampu OFF 🌑")

    # --- SWITCH 2: DAPUR ---
    with col2:
        st.subheader("🍳 Dapur")
        suis_2 = st.toggle("Lampu 2", key="s2")
        if suis_2:
            st.success("ON")
        else:
            st.info("OFF")

    # --- SWITCH 3: KIPAS ---
    with col3:
        st.subheader("🌀 Kipas")
        suis_3 = st.toggle("Kipas Siling", key="s3")
        if suis_3:
            st.success("ON")
        else:
            st.info("OFF")

    st.divider()
    st.info(f"📊 Status Lampu: **{'HIDUP (ON)' if status_v0 else 'MATI (OFF)'}**")

# Jalankan fungsi dashboard
live_dashboard()