import streamlit as st
import pandas as pd

# 🔧 設定最上層
st.set_page_config(page_title="歌曲情緒搜尋器", layout="wide")

# 💡 自定義 CSS：極簡圓角風格 + 漸層背景 + 卡片樣式
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        background-color: #111;
        color: white;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #333;
        transform: scale(1.03);
    }
    .card {
        background-color: white;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 0 15px rgba(0,0,0,0.05);
    }
    .card img {
        border-radius: 20px;
        margin-bottom: 15px;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# ⬆️ 頁面標題區
st.title("🎶 歌曲情緒與情境搜尋器")

# 📁 檔案上傳
uploaded_file = st.file_uploader("📁 請上傳 Excel 檔案（包含欄位：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df_exp = df.copy()
        df_exp = df_exp.assign(情緒=df_exp['情緒'].str.split('、')).explode('情緒')
        df_exp = df_exp.assign(情境=df_exp['情境'].str.split('、')).explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()

        st.sidebar.header("🎯 選擇條件")
        emotion = st.sidebar.selectbox("🎭 情緒", sorted(df_exp['情緒'].unique()))
        scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].unique()
        scene = st.sidebar.selectbox("🎬 情境", sorted(scene_options))

        # 欄位檢查
        cols = ['歌名', '歌手', '情緒', '情境', '點閱率', 'YouTube 連結']
        if '圖片連結' in df_exp.columns:
            cols.append('圖片連結')
        if '歌詞' in df_exp.columns:
            cols.append('歌詞')

        result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)][cols].drop_duplicates()

        st.subheader("🎧 符合的歌曲")
        if result.empty:
            st.warning("❌ 沒有符合條件的歌曲")
        else:
            for _, row in result.iterrows():
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    # 封面圖片
                    if '圖片連結' in row and pd.notna(row['圖片連結']):
                        st.markdown(f"<img src='{row['圖片連結']}' width='100%'>", unsafe_allow_html=True)
                    
                    # 歌曲標題與資訊
                    st.markdown(f"<h3>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h3>", unsafe_allow_html=True)
                    st.markdown(
                        f"🎭 <b>情緒：</b><code>{row['情緒']}</code>　"
                        f"🎬 <b>情境：</b><code>{row['情境']}</code>　"
                        f"🔥 <b>點閱率：</b>{row['點閱率']}",
                        unsafe_allow_html=True
                    )

                    st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})", unsafe_allow_html=True)

                    # 歌詞展開區塊
                    if '歌詞' in row and pd.notna(row['歌詞']):
                        with st.expander("📝 點我看歌詞"):
                            st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
