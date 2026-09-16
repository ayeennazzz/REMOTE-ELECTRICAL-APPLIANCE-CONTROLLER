import streamlit as st
import requests

# ==========================================
# KONFIGURASI BLYNK API
# ==========================================
# Gantikan dengan Auth Token penuh dari Blynk Console anda
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"

# Server Blynk (ikut domain tab Blynk anda, cth: sgp1.blynk.cloud atau blynk.cloud)
BLYNK_SERVER = "https://sgp1.blynk.cloud/external/api"

# Tetapan paparan Streamlit
st.set_page_config(page_title="Dashboard Smart Home", page_icon="🏠", layout="centered")

# ==========================================
# FUNGSI KOMUNIKASI BLYNK REST API
# ==========================================
def get_blynk_status(pin):
    """Membaca nilai semasa dari virtual pin Blynk (0 atau 1)"""
    url = f"{BLYNK_SERVER}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return int(response.text.strip())
    except Exception as e:
        st.error(f"Ralat menyambung ke Blynk ({pin}): {e}")
    return 0

def set_blynk_status(pin, value):
    """Menghantar nilai baru ke virtual pin Blynk (0 atau 1)"""
    url = f"{BLYNK_SERVER}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Gagal menghantar arahan ke {pin}: {e}")
        return False

# ==========================================
# ANTARAMUKA DASHBOARD (UI)
# ==========================================
st.title("🏠 Dashboard Smart Home")
st.write("Sistem Kawalan Jarak Jauh Bersepadu ESP32 & Blynk")
st.divider()

# Senarai peralatan dan pin Blynk yang dipadankan
appliances = [
    {"name": "Lampu Utama (Bilik 1)", "pin": "V1", "icon": "💡"},
    {"name": "Lampu Bilik 2", "pin": "V2", "icon": "💡"},
    {"name": "Exhaust Fan 5V", "pin": "V3", "icon": "🌀"},
    {"name": "Peralatan Tambahan (Spare)", "pin": "V4", "icon": "🔌"},
]

for app in appliances:
    pin = app["pin"]
    name = app["name"]
    icon = app["icon"]
    
    st.subheader(f"{icon} {name}")
    
    # Ambil status terkini dari Blynk
    current_state = get_blynk_status(pin)
    is_on = (current_state == 1)

    # Paparan status kotak
    if is_on:
        st.success(f"🟢 STATUS: {name.upper()} SEDANG BERFUNGSI (ON)")
        btn_label = f"🔴 TUTUP {name.upper()} (OFF)"
        if st.button(btn_label, key=f"btn_off_{pin}"):
            if set_blynk_status(pin, 0):
                st.rerun()
    else:
        st.error(f"⚫ STATUS: {name.upper()} TIDAK AKTIF (OFF)")
        btn_label = f"🟢 BUKA {name.upper()} (ON)"
        if st.button(btn_label, key=f"btn_on_{pin}"):
            if set_blynk_status(pin, 1):
                st.rerun()
                
    st.write("") # Ruang pemisah

st.divider()
if st.button("🔄 Segarkan Status Dashboard"):
    st.rerun()