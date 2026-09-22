import streamlit as st
import requests

# ==========================================
# KONFIGURASI BLYNK API
# ==========================================
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"
BLYNK_SERVER = "https://sgp1.blynk.cloud/external/api"

st.set_page_config(
    page_title="Dashboard Smart Home",
    page_icon="🏠",
    layout="wide"
)

# ==========================================
# FUNGSI KOMUNIKASI BLYNK REST API
# ==========================================
def get_blynk_status(pin):
    """Membaca status virtual pin dari Blynk"""
    url = f"{BLYNK_SERVER}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        response = requests.get(url, timeout=1.2)
        if response.status_code == 200:
            raw_val = response.text.replace('[', '').replace(']', '').replace('"', '').strip()
            return int(raw_val) if raw_val in ["0", "1"] else None
    except Exception:
        pass
    return None

def set_blynk_status(pin, value):
    """Mengirim status baru ke Blynk"""
    url = f"{BLYNK_SERVER}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        response = requests.get(url, timeout=1.2)
        return response.status_code == 200
    except Exception:
        return False

# ==========================================
# HEADER & UCAPAN (Kekal Statik)
# ==========================================
st.markdown("# 🏠 Dashboard Smart Home")
st.markdown("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")
st.write("---")

devices = [
    {"header": "💡 Lampu", "label": "Lampu 1", "pin": "V0"},
    {"header": "🍳 Dapur", "label": "Lampu 2", "pin": "V1"},
    {"header": "🌀 Kipas", "label": "Kipas Siling", "pin": "V2"},
]

# ==========================================
# FRAGMENT KAWALAN (AUTO-SYNC DARI HP & BLYNK)
# ==========================================
@st.fragment(run_every=2)
def render_dashboard():
    cols = st.columns(3)
    active_count = 0

    for i, dev in enumerate(devices):
        with cols[i]:
            st.subheader(dev["header"])
            pin = dev["pin"]

            # 1. Ambil nilai sebenar terkini dari Blynk server
            current_server_val = get_blynk_status(pin)
            is_active = (current_server_val == 1)

            if is_active:
                active_count += 1

            # 2. Toggle guna key unik berpandukan nilai server supaya automatik ikut fon
            toggle_state = st.toggle(
                dev["label"],
                value=is_active,
                key=f"tg_{pin}_{current_server_val}",
                disabled=(current_server_val is None)
            )

            # 3. Kalau Ain klik toggle kat skrin laptop ni sendiri
            if toggle_state != is_active and current_server_val is not None:
                new_val = 1 if toggle_state else 0
                set_blynk_status(pin, new_val)
                st.rerun(scope="fragment")

            # 4. Kotak Status Warna
            if current_server_val is None:
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

    st.write("---")
    st.markdown(
        f"""
        <div style="background-color: #102840; padding: 14px 20px; border-radius: 8px; color: #4fc3f7; font-size: 16px; border: 1px solid #194569;">
            📊 Jumlah peralatan aktif: <b>{active_count}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

render_dashboard()