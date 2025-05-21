import streamlit as st
import pandas as pd

# ✅ 必須是第一個指令
st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")

st.title("🎶 歌曲情緒與情境搜尋器")

# 📌 初始化封面圖片變數
cover_img = None

# 上傳 Excel 檔案
uploaded_file = st.file_uploader("📁 請上傳 Excel 檔案（需包含：圖片連結欄位）", type="xlsx")

if uploaded_file:
    try:
        # 讀取 Excel
        df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取 Excel！")

        # 若有「圖片連結」欄位，且第一首歌有圖片 → 當封面圖
        if '圖片連結' in df.columns and pd.notna(df.iloc[0]['圖片連結']):
            cover_img = df.iloc[0]['圖片連結']

        # ✅ 正式顯示封面圖（用 Excel 的第一首圖）
        if cover_img:
            st.image(cover_img, use_column_width=True)

        # 👉 繼續原本你的邏輯（拆欄位、顯示選單等等）
        # （這段請保留你原本後面程式碼）

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
