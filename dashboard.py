import streamlit as st
import requests

# Masukkan URL Realtime Database anda (pastikan ada .json di hujung)
FIREBASE_URL = "https://smart-home-ain-default-rtdb.asia-southeast1.firebasedatabase.app/lampu1.json"

def dapatkan_status():
    try:
        res = requests.get(FIREBASE_URL, timeout=2)
        if res.status_code == 200 and res.text != "null":
            return int(res.text)
    except Exception:
        pass
    return 0

def hantar_status(val):
    try:
        requests.put(FIREBASE_URL, json=val, timeout=2)
    except Exception:
        pass

st.set_page_config(page_title="Smart Home Ain", page_icon="🏠", layout="centered")
st.title("🏠 Dashboard Smart Home")
st.divider()

@st.fragment(run_every="1s")
def panel():
    status = dapatkan_status()
    st.subheader("💡 Lampu Utama")
    
    if status == 1:
        st.success("🟢 STATUS: LAMPU ON")
        if st.button("🔴 TUTUP LAMPU (OFF)", use_container_width=True):
            hantar_status(0)
            st.rerun()
    else:
        st.error("⚫ STATUS: LAMPU OFF")
        if st.button("🟢 BUKA LAMPU (ON)", use_container_width=True):
            hantar_status(1)
            st.rerun()

panel()