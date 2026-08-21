import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import math

# ── Hằng số ────────────────────────────────────────────────────────
TC_MOI_MON = 3
DIEM = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0}
MAU  = {"A": "#2E7D32", "B": "#F9A825", "C": "#E65100", "D": "#C62828"}

# ── Cấu hình trang ─────────────────────────────────────────────────
st.set_page_config(page_title="Máy tính GPA", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.8rem; max-width: 1000px; }
h1 { color: #1A237E !important; font-weight: 800 !important; }
.card {
    border-radius: 12px; padding: 12px 16px; margin: 6px 0;
    font-family: Inter, sans-serif;
}
.metric-box {
    background: #F0F4F8; border-radius: 12px;
    padding: 14px 18px; text-align: center; margin-bottom: 8px;
}
.metric-box .val { font-size: 2rem; font-weight: 800; }
.metric-box .lbl { font-size: 0.82rem; color: #666; margin-top: 2px; }
.stSlider > div { padding-top: 2px; }
hr { border-color: #ddd; margin: 14px 0; }
</style>
""", unsafe_allow_html=True)

# ── Tiêu đề ────────────────────────────────────────────────────────
st.title("🎓 Máy tính GPA Tốt nghiệp")
st.caption("Tính điểm tối thiểu cho các môn còn lại để đạt GPA mục tiêu khi ra trường.")
st.divider()

# ── Layout: 2 cột ──────────────────────────────────────────────────
col_in, col_out = st.columns([1, 1], gap="large")

with col_in:
    st.markdown("### 📋 Thông tin học tập")
    tc_tong  = st.number_input("📚 Tổng tín chỉ cần học đến tốt nghiệp",
                               min_value=10, max_value=300, value=130, step=1)
    tc_da    = st.number_input("✅ Số tín chỉ đã hoàn thành",
                               min_value=0, max_value=300, value=90, step=1)
    gpa_hien = st.slider("📊 GPA hiện tại", 1.0, 4.0, 2.8, step=0.01,
                         format="%.2f")
    gpa_mong = st.slider("🎯 GPA mong muốn khi tốt nghiệp", 1.0, 4.0, 3.2,
                         step=0.01, format="%.2f")

    st.markdown("### 🎛️ Ước tính phân bổ điểm")
    st.caption("Kéo thử để xem GPA dự kiến thay đổi theo phân bổ điểm.")
    so_b = st.slider("🟡 Số môn điểm B", 0, 60, 5, step=1)
    so_c = st.slider("🟠 Số môn điểm C", 0, 60, 2, step=1)
    so_d = st.slider("🔴 Số môn điểm D", 0, 60, 0, step=1)

# ── Tính toán ──────────────────────────────────────────────────────
tc_con     = tc_tong - tc_da
so_mon_con = tc_con / TC_MOI_MON if tc_con > 0 else 0
n          = int(so_mon_con)

tong_hien    = gpa_hien * tc_da
tong_can     = gpa_mong * tc_tong
tong_con_can = tong_can - tong_hien
tong_toan_A  = DIEM["A"] * tc_con

with col_out:
    st.markdown("### 📈 Kết quả")

    # ── Kiểm tra lỗi ───────────────────────────────────────────────
    if tc_da >= tc_tong:
        st.error("⚠️ Số tín chỉ đã học phải nhỏ hơn tổng số tín chỉ.")
        st.stop()
    elif tong_con_can > tong_toan_A + 0.001:
        st.error("⚠️ GPA mong muốn quá cao, không thể đạt được dù toàn điểm A.")
        st.stop()
    elif tong_con_can <= 0:
        st.info("ℹ️ GPA hiện tại đã vượt mức mong muốn. Bạn chỉ cần duy trì!")
        st.stop()

    # ── Metric tổng quan ───────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.markdown(f"""<div class='metric-box'>
        <div class='val' style='color:#1A237E'>{n}</div>
        <div class='lbl'>Môn còn lại</div></div>""", unsafe_allow_html=True)
    m2.markdown(f"""<div class='metric-box'>
        <div class='val' style='color:#1A237E'>{tc_con}</div>
        <div class='lbl'>Tín chỉ còn lại</div></div>""", unsafe_allow_html=True)
    m3.markdown(f"""<div class='metric-box'>
        <div class='val' style='color:#1A237E'>{gpa_mong:.2f}</div>
        <div class='lbl'>GPA mục tiêu</div></div>""", unsafe_allow_html=True)

    # ── Tính max B / C / D ─────────────────────────────────────────
    du_diem = round(tong_toan_A - tong_con_can, 4)
    max_B = min(n, math.floor(du_diem / ((DIEM["A"]-DIEM["B"]) * TC_MOI_MON)))
    max_C = min(n, math.floor(du_diem / ((DIEM["A"]-DIEM["C"]) * TC_MOI_MON)))
    max_D = min(n, math.floor(du_diem / ((DIEM["A"]-DIEM["D"]) * TC_MOI_MON)))

    def the_ket_qua(nhan, mau, so_A, so_x):
        st.markdown(f"""
        <div class='card' style='background:{mau}18;border-left:5px solid {mau}'>
            <b style='color:{mau};font-size:1.05rem'>Tối đa {so_x} môn {nhan}</b>
            <span style='color:#555;font-size:0.9rem'>
              &nbsp;→ {so_A} môn A + {so_x} môn {nhan}
            </span>
        </div>""", unsafe_allow_html=True)

    the_ket_qua("B", MAU["B"], n - max_B, max_B)
    the_ket_qua("C", MAU["C"], n - max_C, max_C)
    the_ket_qua("D", MAU["D"], n - max_D, max_D)

    st.caption("\\* Các môn còn lại đều lấy điểm A để tối đa hoá số môn được hạ.")

# ── Biểu đồ tròn (toàn chiều rộng bên dưới) ───────────────────────
st.divider()
st.markdown("### 🥧 Biểu đồ phân bổ điểm theo ước tính")

sb = min(so_b, n)
sc = min(so_c, n - sb)
sd = min(so_d, n - sb - sc)
sa = n - sb - sc - sd

tong_slider  = (sa*DIEM["A"] + sb*DIEM["B"] + sc*DIEM["C"] + sd*DIEM["D"]) * TC_MOI_MON
gpa_du_kien  = round((tong_hien + tong_slider) / tc_tong, 2) if tc_tong > 0 else 0
dat_muc_tieu = gpa_du_kien >= gpa_mong

# Metric GPA dự kiến
gpa_color = "#2E7D32" if dat_muc_tieu else "#C62828"
icon = "✅" if dat_muc_tieu else "❌"
trang_thai = "Đạt mục tiêu" if dat_muc_tieu else "Chưa đạt mục tiêu"

c1, c2 = st.columns([1, 2])

with c1:
    st.markdown(f"""
    <div class='metric-box' style='margin-top:18px'>
        <div class='val' style='color:{gpa_color}'>{icon} {gpa_du_kien:.2f}</div>
        <div class='lbl'>GPA dự kiến</div>
        <div style='font-size:0.8rem;color:{gpa_color};font-weight:600;margin-top:4px'>
            {trang_thai}
        </div>
    </div>
    <div style='margin-top:10px;font-size:0.88rem;color:#555;line-height:1.6'>
        <b>Phân bổ ước tính:</b><br>
        🟢 Điểm A: <b>{sa}</b> môn<br>
        🟡 Điểm B: <b>{sb}</b> môn<br>
        🟠 Điểm C: <b>{sc}</b> môn<br>
        🔴 Điểm D: <b>{sd}</b> môn
    </div>
    """, unsafe_allow_html=True)

with c2:
    labels, values, colors = [], [], []
    for ten, so, mau in [("A", sa, MAU["A"]), ("B", sb, MAU["B"]),
                          ("C", sc, MAU["C"]), ("D", sd, MAU["D"])]:
        if so > 0:
            labels.append(f"Điểm {ten}\n{so} môn")
            values.append(so)
            colors.append(mau)

    if not values:
        values, labels, colors = [1], ["(chưa có môn)"], ["#ccc"]

    fig, ax = plt.subplots(figsize=(4.8, 3.8))
    fig.patch.set_facecolor("#F8FAFC")
    ax.set_facecolor("#F8FAFC")

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
        startangle=90,
        textprops={"fontsize": 9, "color": "#333"},
        pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 2.2}
    )
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.set_title(f"GPA dự kiến: {gpa_du_kien:.2f}",
                 fontsize=11, fontweight="bold", color=gpa_color, pad=10)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=False)

# ── Miễn trừ trách nhiệm ───────────────────────────────────────────
st.divider()
st.caption(
    "⚠️ **Lưu ý:** Công cụ này chỉ mang tính tham khảo dựa trên thang điểm 4.0 chuẩn "
    "(A=4, B=3, C=2, D=1) và giả định mỗi môn là 3 tín chỉ. "
    "Quy chế tính GPA thực tế có thể khác nhau tùy trường. "
    "Vui lòng kiểm tra quy định của cơ sở đào tạo của bạn."
)
