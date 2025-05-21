import streamlit as st
import pandas as pd

st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")
st.markdown("""
    <h1 style='text-align: center; color: #4A90E2;'>🎶 歌曲情緒與情境搜尋器</h1>
    <hr>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 請上傳 Excel 檔案（含欄位：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

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

        # 動態決定要取出的欄位（防止欄位缺失報錯）
        cols = ['歌名', '歌手', '情緒', '情境', '點閱率', 'YouTube 連結']
        if '圖片連結' in df_exp.columns:
            cols.append('圖片連結')
        if '歌詞' in df_exp.columns:
            cols.append('歌詞')

        # 取出資料
        result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)][cols].drop_duplicates()

        st.markdown("""
        <h2 style='color: #FF6F61;'>🎧 符合的歌曲清單</h2>
        """, unsafe_allow_html=True)

        if result.empty:
            st.warning("❌ 找不到符合條件的歌曲")
        else:
            for _, row in result.iterrows():
                st.markdown(f"""
    <div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 0 8px rgba(0,0,0,0.05);'>
        <h4 style='margin-bottom: 5px;'>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h4>
        {'<img src=\"' + row['圖片連結'] + '\" style=\"width:100%; max-width:300px; border-radius:10px; margin-bottom:10px;\">' if '圖片連結' in row and pd.notna(row['圖片連結']) else ''}
        <p>🌟 <b>情緒：</b> <code>{row['情緒']}</code> ｜ 🎬 <b>情境：</b> <code>{row['情境']}</code></p>
        <p>🔥 <b>點閱率：</b> {row['點閱率']}</p>
        <p><a href=\"{row['YouTube 連結']}\" target=\"_blank\">▶️ 前往 YouTube</a></p>
    </div>
""", unsafe_allow_html=True)


                if '歌詞' in row and pd.notna(row['歌詞']):
                    with st.expander("📝 點我看歌詞"):
                        st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
