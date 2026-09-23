import streamlit as st
import requests

# ==========================================
# KONFIGURASI BLYNK API
# ==========================================
BLYNK_AUTH_TOKEN = "zW9oV9_a-PD7IXvfZ2b-8uhT8OgiEz8x"
BLYNK_SERVER = "https://sgp1.blynk.cloud/external/api"

# Kekalkan sambungan HTTP terbuka untuk elak delay
if "http_session" not in st.session_state:
    st.session_state.http_session = requests.Session()

http = st.session_state.http_session

st.set_page_config(
    page_title="Dashboard Smart Home",
    page_icon="🏠",
    layout="wide"
)

# ==========================================
# FUNGSI KOMUNIKASI BLYNK REST API (PANTAS)
# ==========================================
def get_blynk_status(pin):
    """Membaca status virtual pin dari Blynk"""
    url = f"{BLYNK_SERVER}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        response = http.get(url, timeout=0.6)
        if response.status_code == 200:
            raw_val = response.text.replace('[', '').replace(']', '').replace('"', '').strip()
            return int(raw_val) if raw_val in ["0", "1"] else 0
    except Exception:
        pass
    return 0

def set_blynk_status(pin, value):
    """Menghantar arahan terus ke Blynk"""
    url = f"{BLYNK_SERVER}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        http.get(url, timeout=0.6)
    except Exception:
        pass

# ==========================================
# HEADER & UCAPAN (KEKAL STATIK)
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
# FRAGMENT AUTO-SYNC (KEMASKINI DALAM KOTAK SAHAJA)
# ==========================================
@st.fragment(run_every=1)
def render_dashboard():
    cols = st.columns(3)
    active_count = 0

    for i, dev in enumerate(devices):
        with cols[i]:
            st.subheader(dev["header"])
            pin = dev["pin"]

            # Tarik status sebenar terkini dari server Blynk
            server_val = get_blynk_status(pin)
            is_active = (server_val == 1)

            if is_active:
                active_count += 1

            # KUNCI PENYELESAIAN:
            # key diletakkan server_val di belakang (contoh: tg_V2_1 atau tg_V2_0)
            # Bila tekan push button fizikal, key automatik berubah -> Streamlit terpaksa lukis balik suis ke posisi ON/OFF sebenar!
            widget_key = f"tg_{pin}_{server_val}"
            
            toggle_state = st.toggle(
                dev["label"],
                value=is_active,
                key=widget_key
            )

            # Jika user petik suis di skrin ini secara manual
            if toggle_state != is_active:
                new_val = 1 if toggle_state else 0
                set_blynk_status(pin, new_val)
                st.rerun(scope="fragment")

            # Kotak Paparan Status Warna
            if is_active:
                st.markdown(
                    """
                    <div style="background-color: #1b3820; padding: 16px; border-radius: 8px; color: #81c784; font-weight: bold; text-align: center;">
                        ON
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style="background-color: #2b1b1f; padding: 16px; border-radius: 8px; color: #e57373; font-weight: bold; text-align: center;">
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