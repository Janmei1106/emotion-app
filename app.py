import streamlit as st
import pandas as pd

st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")
st.title("🎶 歌曲情緒與情境搜尋器")

# 上傳 Excel 檔案
uploaded_file = st.file_uploader("📁 請上傳 Excel 檔案（需包含：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）", type="xlsx")

if uploaded_file:
    try:
        # 讀取 Excel
        df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取 Excel！")
        st.dataframe(df.head())

        # 拆分欄位
        df_exp = df.copy()
        df_exp = df_exp.assign(情緒=df_exp['情緒'].str.split('、')).explode('情緒')
        df_exp = df_exp.assign(情境=df_exp['情境'].str.split('、')).explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()

        st.sidebar.header("🔍 請選擇條件")
        emotion = st.sidebar.selectbox("🎭 選擇情緒", sorted(df_exp['情緒'].unique()))
        scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].unique()
        scene = st.sidebar.selectbox("🎬 選擇情境", sorted(scene_options))

        # 檢查欄位存在與否
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
                    st.markdown(f"<img src='{row['圖片連結']}' width='300'>", unsafe_allow_html=True)


                st.markdown(f"**🎵 {row['歌名']}** - {row['歌手']}")
                st.markdown(f"👉 情緒：`{row['情緒']}`｜情境：`{row['情境']}`｜點閱率：{row['點閱率']}")
                st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})")

                if '歌詞' in row and pd.notna(row['歌詞']):
                    with st.expander("📝 點我看歌詞"):
                        st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
