import streamlit as st
import pandas as pd

st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")

# ⬇ 自訂全站 CSS 樣式
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #F0F4FF, #FDEBFF);
}
section.main > div {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}
h3 {
    color: #303F9F;
    font-weight: bold;
}
button[kind="secondary"] {
    background: linear-gradient(to right, #d1c4e9, #bbdefb) !important;
    color: #333 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    margin: 4px 0px !important;
    transition: all 0.3s ease-in-out;
}
button[kind="secondary"]:hover {
    background: linear-gradient(to right, #b39ddb, #90caf9) !important;
    transform: scale(1.04);
}
img.song-cover {
    width: 100%;
    max-width: 400px;
    border-radius: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# 📁 上傳 Excel 檔案
uploaded_file = st.file_uploader("📁 請上傳 Excel（需含：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取 Excel！")

        # 🔄 拆分欄位多值
        df_exp = df.copy()
        df_exp['情緒'] = df_exp['情緒'].str.split('、')
        df_exp['情境'] = df_exp['情境'].str.split('、')
        df_exp = df_exp.explode('情緒').explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()

        # 🎭 sidebar：情緒選單
        st.sidebar.header("🎭 請選擇情緒")
        all_emotions = sorted(df_exp['情緒'].dropna().unique())
        chosen_emotion = st.sidebar.selectbox("情緒", all_emotions)

        # 🎬 sidebar：情境選單（根據情緒過濾）
        st.sidebar.header("🎬 請選擇情境")
        scene_options = sorted(df_exp[df_exp['情緒'] == chosen_emotion]['情境'].dropna().unique())
        chosen_scene = st.sidebar.selectbox("情境", scene_options)

        # 📊 過濾資料
        result = df_exp[
            (df_exp['情緒'] == chosen_emotion) &
            (df_exp['情境'] == chosen_scene)
        ].drop_duplicates()

        st.subheader("🎧 符合的歌曲")

        if result.empty:
            st.warning("❌ 找不到符合的歌曲")
        else:
            for _, row in result.iterrows():
                st.markdown("---")

                # 🖼️ 封面圖
                if '圖片連結' in row and pd.notna(row['圖片連結']):
                    st.markdown(f"<img src='{row['圖片連結']}' class='song-cover'>", unsafe_allow_html=True)

                # 🎵 基本資訊
                st.markdown(f"<h3>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h3>", unsafe_allow_html=True)
                st.markdown(
                    f"🎭 <b>情緒：</b><code>{row['情緒']}</code> ｜ "
                    f"🎬 <b>情境：</b><code>{row['情境']}</code> ｜ "
                    f"🔥 <b>點閱率：</b>{row['點閱率']}",
                    unsafe_allow_html=True
                )
                st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})")

                # 📝 歌詞展開
                if '歌詞' in row and pd.notna(row['歌詞']):
                    with st.expander("📝 點我看歌詞"):
                        st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
else:
    st.info("📥 請先上傳 Excel 檔案以開始操作")
