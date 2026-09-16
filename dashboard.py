import streamlit as st
import requests

# ==========================================
# KONFIGURASI BLYNK API
# ==========================================
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x" # Letak token penuh di sini
BLYNK_SERVER = "https://sgp1.blynk.cloud/external/api"

st.set_page_config(
    page_title="Dashboard Smart Home",
    page_icon="🏠",
    layout="centered"
)

# ==========================================
# FUNGSI KOMUNIKASI BLYNK REST API
# ==========================================
def get_blynk_status(pin):
    """Membaca nilai semasa dari virtual pin Blynk (0 atau 1)"""
    url = f"{BLYNK_SERVER}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            raw_val = response.text.replace('[', '').replace(']', '').replace('"', '').strip()
            return 1 if raw_val == "1" else 0
    except Exception:
        pass
    return 0

def set_blynk_status(pin, value):
    """Menghantar nilai baru ke virtual pin Blynk (0 atau 1)"""
    url = f"{BLYNK_SERVER}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

# ==========================================
# ANTARAMUKA PENGGUNA (UI)
# ==========================================
st.title("🏠 Dashboard Smart Home")
st.caption("Kawalan Jarak Jauh Bersepadu ESP32 & Blynk Cloud")
st.divider()

# Susunan pin yang diselaraskan dengan Blynk Console
appliances = [
    {"name": "Lampu Ruang Tamu", "pin": "V0", "icon": "💡"},
    {"name": "Lampu Dapur", "pin": "V1", "icon": "💡"},
    {"name": "Kipas Dapur (Exhaust Fan)", "pin": "V2", "icon": "🌀"},
]

for item in appliances:
    pin = item["pin"]
    name = item["name"]
    icon = item["icon"]

    st.subheader(f"{icon} {name}")
    
    current_state = get_blynk_status(pin)
    is_on = (current_state == 1)

    if is_on:
        st.success(f"🟢 STATUS: {name.upper()} SEDANG BERFUNGSI (ON)")
        if st.button(f"🔴 TUTUP {name.upper()} (OFF)", key=f"off_{pin}"):
            if set_blynk_status(pin, 0):
                st.rerun()
    else:
        st.error(f"⚫ STATUS: {name.upper()} TIDAK AKTIF (OFF)")
        if st.button(f"🟢 BUKA {name.upper()} (ON)", key=f"on_{pin}"):
            if set_blynk_status(pin, 1):
                st.rerun()

    st.write("")

st.divider()

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()