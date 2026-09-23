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
# FUNGSI KOMUNIKASI BLYNK REST API (LAJU)
# ==========================================
def get_blynk_status(pin):
    """Membaca status virtual pin dengan timeout singkat"""
    url = f"{BLYNK_SERVER}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        response = requests.get(url, timeout=0.8)
        if response.status_code == 200:
            raw_val = response.text.replace('[', '').replace(']', '').replace('"', '').strip()
            return int(raw_val) if raw_val in ["0", "1"] else 0
    except Exception:
        pass
    return 0

def set_blynk_status(pin, value):
    """Menghantar status terus ke Blynk serta-merta"""
    url = f"{BLYNK_SERVER}/update?token={BLYNK_AUTH_TOKEN}&{pin}={value}"
    try:
        requests.get(url, timeout=0.8)
    except Exception:
        pass

# ==========================================
# SIMPAN STATUS DALAM SESSION STATE
# ==========================================
devices = [
    {"header": "💡 Lampu", "label": "Lampu 1", "pin": "V0"},
    {"header": "🍳 Dapur", "label": "Lampu 2", "pin": "V1"},
    {"header": "🌀 Kipas", "label": "Kipas Siling", "pin": "V2"},
]

# Tarik data permulaan sekali sahaja semasa mula buka
if "initialized" not in st.session_state:
    for dev in devices:
        p = dev["pin"]
        st.session_state[f"state_{p}"] = (get_blynk_status(p) == 1)
    st.session_state["initialized"] = True

# ==========================================
# HEADER, BUTANG REFRESH & UCAPAN
# ==========================================
col_title, col_btn = st.columns([4, 1])

with col_title:
    st.markdown("# 🏠 Dashboard Smart Home")
    st.markdown("Selamat Datang, **Ain Nursyafiqah**! Kawal litar anda di sini.")

with col_btn:
    st.write("##")
    # Butang manual untuk semak status jika ada tekan push button fizikal
    if st.button("🔄 Segerak Status (Sync)", use_container_width=True):
        for dev in devices:
            p = dev["pin"]
            st.session_state[f"state_{p}"] = (get_blynk_status(p) == 1)
        st.rerun()

st.write("---")

# ==========================================
# PAPARAN SUIS TOGGLE & STATUS (STATIK)
# ==========================================
cols = st.columns(3)
active_count = 0

for i, dev in enumerate(devices):
    pin = dev["pin"]
    current_val = st.session_state[f"state_{pin}"]
    if current_val:
        active_count += 1

    with cols[i]:
        st.subheader(dev["header"])

        # Fungsi tindakan serta-merta apabila pengguna petik suis
        def on_toggle_change(p=pin):
            new_val = 1 if st.session_state[f"ui_{p}"] else 0
            st.session_state[f"state_{p}"] = (new_val == 1)
            set_blynk_status(p, new_val)

        st.toggle(
            dev["label"],
            value=current_val,
            key=f"ui_{pin}",
            on_change=on_toggle_change
        )

        # Kotak Status Warna (Kekal Statik, Tiada Kelip)
        if current_val:
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