import streamlit as st
import requests

# --- BLYNK CONFIGURATION ---
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"

def dapatkan_status_blynk(pin):
    """BACA status pin semasa dari Blynk Cloud"""
    url = f"https://sgp1.blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 200:
            return int(res.text.strip())
    except Exception:
        pass
    return 0

def kawal_blynk(pin, value):
    """HANTAR arahan ON/OFF ke Blynk Cloud bila ditekan"""
    url = f"https://sgp1.blynk.cloud/external/api/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        res = requests.get(url, timeout=2)
        return res.status_code == 200
    except Exception:
        return False

# --- SETTING PAGE ---
st.set_page_config(page_title="Smart Home Ain", page_icon="🏠", layout="centered")

st.title("🏠 Dashboard Smart Home")
st.write("Selamat Datang, **Ain Nursyafiqah**! Kawal peranti anda di sini.")
st.divider()

# --- FRAGMENT UNTUK AUTO-UPDATE PAPARAN (SETIAP 1 SAAT) ---
@st.fragment(run_every="1s")
def panel_kawalan():
    # 1. Semak status real-time kat server Blynk
    status_lampu = dapatkan_status_blynk("V0")  # 1 (ON) atau 0 (OFF)
    
    col1, col2, col3 = st.columns(3)

    # --- KAWALAN LAMPU UTAMA (V0) ---
    with col1:
        st.subheader("💡 Lampu (V0)")
        
        # Paparkan status terkini litar
        if status_lampu == 1:
            st.success("🟢 STATUS: LAMPU ON")
            if st.button("🔴 TUTUP LAMPU (OFF)", key="btn_off", use_container_width=True):
                kawal_blynk("V0", 0)
                st.rerun()
        else:
            st.error("⚫ STATUS: LAMPU OFF")
            if st.button("🟢 BUKA LAMPU (ON)", key="btn_on", use_container_width=True):
                kawal_blynk("V0", 1)
                st.rerun()

    # --- KAWALAN DAPUR ---
    with col2:
        st.subheader("🍳 Dapur")
        st.info("⚪ Tiada sambungan litar")
        st.button("Tukar Dapur", key="btn_dapur", disabled=True, use_container_width=True)

    # --- KAWALAN KIPAS ---
    with col3:
        st.subheader("🌀 Kipas")
        st.info("⚪ Tiada sambungan litar")
        st.button("Tukar Kipas", key="btn_kipas", disabled=True, use_container_width=True)

    st.divider()
    status_text = "LAMPU TERBUKA (ON)" if status_lampu == 1 else "LAMPU TERTUTUP (OFF)"
    st.info(f"📡 Real-time Sync Status: **{status_text}**")

# Jalankan panel
panel_kawalan()