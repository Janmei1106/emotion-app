import streamlit as st
import pandas as pd

# ✅ 頁面設定
st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵")

# ✅ 加入背景與按鈕樣式
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #e0f7fa, #fbeaff);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #4A90E2;
}
.stButton>button {
    background-color: #E1EFFF;
    color: #4A90E2;
    border: none;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    box-shadow: 4px 4px 10px #d0d0d0, -4px -4px 10px #ffffff;
    transition: 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #cde3ff;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# ✅ 標題
st.title("🎶 歌曲情緒與情境搜尋器")

# ✅ 上傳 Excel
uploaded_file = st.file_uploader("📁 請上傳 Excel（含：歌名、歌手、情緒、情境、點閱率、YouTube 連結、圖片連結、歌詞）", type="xlsx")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # 🔧 清除欄位空白
        st.success("✅ 成功讀取 Excel！")

        # 拆分欄位
        df_exp = df.copy()
        df_exp = df_exp.assign(情緒=df_exp['情緒'].str.split('、')).explode('情緒')
        df_exp = df_exp.assign(情境=df_exp['情境'].str.split('、')).explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()

        # 側邊欄選擇器
        st.sidebar.header("🔍 請選擇條件")
        emotion = st.sidebar.selectbox("🎭 選擇情緒", sorted(df_exp['情緒'].unique()))
        scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].unique()
        scene = st.sidebar.selectbox("🎬 選擇情境", sorted(scene_options))

        # 欄位過濾
        cols = ['歌名', '歌手', '情緒', '情境', '點閱率', 'YouTube 連結']
        if '圖片連結' in df_exp.columns:
            cols.append('圖片連結')
        if '歌詞' in df_exp.columns:
            cols.append('歌詞')

        result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)][cols].drop_duplicates()

        # 顯示結果
        st.subheader("🎧 符合的歌曲")
        if result.empty:
            st.warning("❌ 找不到符合條件的歌曲")
        else:
            for _, row in result.iterrows():
                st.markdown("---")

                # ✅ 漂亮圖片
                if '圖片連結' in row and pd.notna(row['圖片連結']):
                    st.markdown(
                        f"<img src='{row['圖片連結']}' width='300' "
                        f"style='border-radius: 20px; box-shadow: 8px 8px 20px rgba(0,0,0,0.15); margin-bottom: 10px;'>",
                        unsafe_allow_html=True
                    )

                # ✅ 歌名 + 歌手
                st.markdown(f"<h3>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h3>", unsafe_allow_html=True)

                # ✅ 情緒＋情境＋點閱率
                st.markdown(
                    f"🎭 <b>情緒：</b><code>{row['情緒']}</code> ｜ "
                    f"🎬 <b>情境：</b><code>{row['情境']}</code> ｜ "
                    f"🔥 <b>點閱率：</b>{row['點閱率']}",
                    unsafe_allow_html=True
                )

                # ✅ YouTube 連結
                st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})")

                # ✅ 歌詞
                if '歌詞' in row and pd.notna(row['歌詞']):
                    with st.expander("📝 點我看歌詞"):
                        st.markdown(str(row['歌詞']).replace('\n', '<br>'), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
