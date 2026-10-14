import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ==========================================
# 1. DỮ LIỆU BAN ĐẦU
# ==========================================
data = {
    "Ho_ten": [
        "Nguyễn Ngọc Hải An",
        "Trần Thị Bính",
        "Lê Hồng Mai Thy",
        "Phạm Hoàng Kim Ngọc",
        "Đỗ Thị Thuỳ Trang",
        "Hoàng Thị Ngọc Lan",
        "Vũ Gia Bảo",
        "Đặng Trần Hoài Nam",
        "Phạm Hoàng Như Phúc",
        "Nguyễn Ngọc Như Ý",
    ],
    "Chuyen_can": [9.0, 8.5, 7.0, 9.5, 8.0, 6.0, 9.0, 7.5, 8.0, 9.5],
    "Giua_ky": [8.0, 8.5, 6.0, 9.0, 7.0, 5.0, 8.5, 7.0, 7.5, 9.0],
    "Cuoi_ky": [7.0, 8.0, 6.5, 9.0, 7.0, 5.0, 8.5, 6.5, 7.0, 9.2],
}

df = pd.DataFrame(data)

# ==========================================
# 2. TÍNH ĐIỂM TỔNG KẾT (20% CC + 30% GK + 50% CK)
# ==========================================
df["Tong_ket"] = (
    0.20 * df["Chuyen_can"]
    + 0.30 * df["Giua_ky"]
    + 0.50 * df["Cuoi_ky"]
)
df["Tong_ket"] = df["Tong_ket"].round(2)


# ==========================================
# 3. HÀM XẾP LOẠI
# ==========================================
def xep_loai(diem):
  if diem >= 8.5:
    return "Giỏi"
  elif diem >= 7.0:
    return "Khá"
  elif diem >= 5.0:
    return "Trung bình"
  else:
    return "Yếu"


df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# ==========================================
# GIAO DIỆN WEB APP STREAMLIT
# ==========================================
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

# Hiển thị bảng điểm của 10 sinh viên
st.subheader("1. Bảng điểm chi tiết của 10 sinh viên")
st.dataframe(df, use_container_width=True)

# Thống kê
dtb_lop = df["Tong_ket"].mean()
sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
so_sv_dat = (df["Tong_ket"] >= 5.0).sum()

st.subheader("2. Thống kê kết quả học tập")
st.metric(label="Điểm tổng kết trung bình của lớp", value=f"{dtb_lop:.2f}")

col1, col2 = st.columns(2)
with col1:
  st.success(
      f"**Sinh viên cao điểm nhất:** {sv_cao_nhat['Ho_ten']}"
      f" ({sv_cao_nhat['Tong_ket']} điểm)"
  )
with col2:
  st.error(
      f"**Sinh viên thấp điểm nhất:** {sv_thap_nhat['Ho_ten']}"
      f" ({sv_thap_nhat['Tong_ket']} điểm)"
  )

st.info(f"Số sinh viên đạt (điểm tổng kết >= 5.0): {so_sv_dat}/{len(df)}")

# Danh sách chọn sinh viên (Selectbox)
st.subheader("3. Tra cứu điểm cá nhân sinh viên")
ten_sv_chon = st.selectbox("Chọn một sinh viên:", df["Ho_ten"].tolist())
sv_info = df[df["Ho_ten"] == ten_sv_chon].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", sv_info["Chuyen_can"])
c2.metric("Giữa kỳ", sv_info["Giua_ky"])
c3.metric("Cuối kỳ", sv_info["Cuoi_ky"])
c4.metric("Tổng kết", sv_info["Tong_ket"])
c5.metric("Xếp loại", sv_info["Xep_loai"])

# Biểu đồ cột tổng kết
st.subheader("4. Biểu đồ điểm tổng kết của 10 sinh viên")
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(df["Ho_ten"], df["Tong_ket"], color="#5b9bd5")
ax.invert_yaxis()
ax.set_xlabel("Điểm tổng kết")
ax.set_ylabel("Họ và tên sinh viên")
ax.set_xlim(0, 10)
ax.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig)

# Hiển thị họ tên và MSSV ở cuối trang với kích thước chữ nhỏ
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: small; color: gray;'>Họ tên:"
    " [Trần Hoàng Long] - MSSV: [29]</p>",
    unsafe_allow_html=True,
)