import streamlit as st
import pandas as pd


st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")
st.title("🎶 歌曲情緒與情境搜尋器")


# 自訂按鈕樣式（圓角卡片風格）
st.markdown("""
<style>
button[kind="secondary"] {
    background-color: #F0F4FF !important;
    color: #333 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    height: 42px !important;
    margin: 2px 0px !important;
}
button[kind="secondary"]:hover {
    background-color: #BBD7FF !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader("📁 請上傳 Excel 檔案（需包含：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）", type="xlsx")
cover_img = None  # 預設封面圖為空


if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取 Excel！")


        # 設定封面
        if '圖片連結' in df.columns and pd.notna(df.iloc[0]['圖片連結']):
            cover_img = df.iloc[0]['圖片連結']
            st.image(cover_img, use_container_width=True)


        # 拆分多重欄位
        df_exp = df.copy()
        df_exp = df_exp.assign(情緒=df_exp['情緒'].str.split('、')).explode('情緒')
        df_exp = df_exp.assign(情境=df_exp['情境'].str.split('、')).explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()


        # ====== 左側條件選單 ======
        st.sidebar.header("🔍 請選擇情緒")
        all_emotions = sorted(df_exp['情緒'].unique())


        if 'chosen_emotion' not in st.session_state:
            st.session_state.chosen_emotion = all_emotions[0]


        for i in range(0, len(all_emotions), 2):
            cols = st.sidebar.columns(2)
            for j in range(2):
                if i + j < len(all_emotions):
                    emo = all_emotions[i + j]
                    if cols[j].button(f"🎭 {emo}", key=f"emo_{emo}"):
                        st.session_state.chosen_emotion = emo


        emotion = st.session_state.chosen_emotion
        scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].unique()
        scene = st.sidebar.selectbox("🎬 選擇情境", sorted(scene_options))


        # 顯示符合條件的歌曲
        cols = ['歌名', '歌手', '情緒', '情境', '點閱率', 'YouTube 連結']
        if '圖片連結' in df_exp.columns:
            cols.append('圖片連結')
        if '歌詞' in df_exp.columns:
            cols.append('歌詞')


        result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)][cols].drop_duplicates()


        st.subheader("🎧 符合的歌曲")
        if result.empty:
            st.warning("❌ 找不到符合條件的歌曲")
        else:
            for _, row in result.iterrows():
                st.markdown("---")
                if '圖片連結' in row and pd.notna(row['圖片連結']):
                    st.markdown(f"<img src='{row['圖片連結']}' style='width:100%; max-width:400px; border-radius:16px;'>", unsafe_allow_html=True)


                st.markdown(f"<h3 style='margin-bottom: 0.2em;'>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h3>", unsafe_allow_html=True)
                st.markdown(
                    f"🎭 <b>情緒：</b><code>{row['情緒']}</code> ｜ "
                    f"🎬 <b>情境：</b><code>{row['情境']}</code> ｜ "
                    f"🔥 <b>點閱率：</b>{row['點閱率']}",
                    unsafe_allow_html=True
                )
                st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})")


                if '歌詞' in row and pd.notna(row['歌詞']):
                    with st.expander("📝 點我看歌詞"):
                        st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)


    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")