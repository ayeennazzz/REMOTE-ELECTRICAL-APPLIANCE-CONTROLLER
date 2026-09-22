import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# ==========================================
# KONFIGURASI BLYNK API
# ==========================================
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"  # Auth Token anda
BLYNK_SERVER = "https://sgp1.blynk.cloud/external/api"

st.set_page_config(
    page_title="Dashboard Smart Home",
    page_icon="🏠",
    layout="wide"
)

# ==========================================
# AUTO-REFRESH DI LATAR BELAKANG
# ==========================================
# Semak status setiap 2000 ms (2 saat) secara senyap tanpa kelip skrin
st_autorefresh(interval=2000, key="blynk_sync_counter")

# ==========================================
# FUNGSI KOMUNIKASI BLYNK REST API
# ==========================================
def get_blynk_status(pin):
    """Membaca nilai semasa dari virtual pin Blynk (0 atau 1)"""
    url = f"{BLYNK_SERVER}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        response = requests.get(url, timeout=1.5)
        if response.status_code == 200:
            raw_val = response.text.replace('[', '').replace(']', '').replace('"', '').strip()
            return int(raw_val) if raw_val in ["0", "1"] else None
    except Exception:
        pass
    return None

def set_blynk_status(pin, value):
    """Menghantar nilai baru ke virtual pin Blynk (0 atau 1)"""
    url = f"{BLYNK_SERVER}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        response = requests.get(url, timeout=1.5)
        return response.status_code == 200
    except Exception:
        return False

# ==========================================
# HEADER & UCAPAN
# ==========================================
st.markdown("# 🏠 Dashboard Smart Home")
st.markdown("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.write("---")

# ==========================================
# SENARAI PERALATAN (3 LAJUR)
# ==========================================
devices = [
    {"header": "💡 Lampu", "label": "Lampu 1", "pin": "V0"},
    {"header": "🍳 Dapur", "label": "Lampu 2", "pin": "V1"},
    {"header": "🌀 Kipas", "label": "Kipas Siling", "pin": "V2"},
]

cols = st.columns(3)
active_count = 0

for i, dev in enumerate(devices):
    with cols[i]:
        st.subheader(dev["header"])
        pin = dev["pin"]
        key_name = f"toggle_{pin}"

        # Ambil nilai sebenar dari Blynk
        server_val = get_blynk_status(pin)
        is_active = (server_val == 1)

        if is_active:
            active_count += 1

        # Toggle Switch
        toggle_state = st.toggle(
            dev["label"],
            value=is_active,
            key=key_name,
            disabled=(server_val is None)
        )

        # Jika toggle di dashboard disentuh oleh user
        if toggle_state != is_active and server_val is not None:
            new_val = 1 if toggle_state else 0
            if set_blynk_status(pin, new_val):
                st.rerun()

        # Kotak Paparan Status Warna
        if server_val is None:
            st.markdown(
                """
                <div style="background-color: #3b3a1a; padding: 16px; border-radius: 8px; color: #d4e157; font-weight: bold;">
                    Gagal sambung
                </div>
                """,
                unsafe_allow_html=True
            )
        elif is_active:
            st.markdown(
                """
                <div style="background-color: #1b3820; padding: 16px; border-radius: 8px; color: #81c784; font-weight: bold;">
                    ON
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background-color: #2b1b1f; padding: 16px; border-radius: 8px; color: #e57373; font-weight: bold;">
                    OFF
                </div>
                """,
                unsafe_allow_html=True
            )

# ==========================================
# FOOTER: JUMLAH PERALATAN AKTIF
# ==========================================
st.write("---")
st.markdown(
    f"""
    <div style="background-color: #102840; padding: 14px 20px; border-radius: 8px; color: #4fc3f7; font-size: 16px; border: 1px solid #194569;">
        📊 Jumlah peralatan aktif: <b>{active_count}</b>
    </div>
    """,
    unsafe_allow_html=True
)