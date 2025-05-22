import streamlit as st
import pandas as pd

# 頁面設定
st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")
st.title("🎶 歌曲情緒與情境搜尋器")

# 上傳 Excel 檔案
uploaded_file = st.file_uploader(
    "📁 請上傳 Excel 檔案（需包含：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）",
    type="xlsx"
)

if uploaded_file:
    try:
        # 讀取 Excel
        df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取 Excel！")
        st.dataframe(df.head())

        # 顯示封面圖（來自第一首歌）
        if '圖片連結' in df.columns and pd.notna(df.iloc[0]['圖片連結']):
            cover_img = df.iloc[0]['圖片連結']
            st.image(cover_img, use_container_width=True)

        # 拆分情緒與情境欄位
        df_exp = df.copy()
        df_exp['情緒'] = df_exp['情緒'].str.split('、')
        df_exp['情境'] = df_exp['情境'].str.split('、')
        df_exp = df_exp.explode('情緒').explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()

        # 側邊欄選擇條件
        st.sidebar.header("🔍 請選擇條件")
        emotion = st.sidebar.selectbox("🎭 選擇情緒", sorted(df_exp['情緒'].unique()))
        scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].unique()
        scene = st.sidebar.selectbox("🎬 選擇情境", sorted(scene_options))

        # 檢查欄位存在，準備要顯示的欄位
        cols = ['歌名', '歌手', '情緒', '情境', '點閱率', 'YouTube 連結']
        if '圖片連結' in df_exp.columns:
            cols.append('圖片連結')
        if '歌詞' in df_exp.columns:
            cols.append('歌詞')

        # 篩選符合條件的資料
        result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)][cols].drop_duplicates()

        # 顯示結果
        st.subheader("🎧 符合的歌曲")
        if result.empty:
            st.warning("❌ 找不到符合條件的歌曲")
        else:
            for _, row in result.iterrows():
                st.markdown("---")

                # 圖片（若有）
                if '圖片連結' in row and pd.notna(row['圖片連結']):
                    st.markdown(f"<img src='{row['圖片連結']}' width='300' style='border-radius: 15px;'>", unsafe_allow_html=True)

                # 歌曲資訊
                st.markdown(
                    f"<h3 style='margin-bottom: 0.2em;'>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h3>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"🎭 <b>情緒：</b><code>{row['情緒']}</code> ｜ "
                    f"🎬 <b>情境：</b><code>{row['情境']}</code> ｜ "
                    f"🔥 <b>點閱率：</b>{row['點閱率']}",
                    unsafe_allow_html=True
                )
                st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})")

                # 歌詞（可展開）
                if '歌詞' in row and pd.notna(row['歌詞']):
                    with st.expander("📝 點我看歌詞"):
                        st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
