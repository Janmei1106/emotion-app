import streamlit as st
import pandas as pd

st.set_page_config(page_title="歌曲情緒搜尋器", page_icon="🎵", layout="wide")
st.title("🎶 歌曲情緒與情境搜尋器")

menu = st.sidebar.radio("選單", ["首頁", "情緒探索"])

@st.cache_data
def load_excel(file):
    df = pd.read_excel(file)
    df = df.copy()
    df = df.assign(情緒=df['情緒'].str.split('、')).explode('情緒')
    df = df.assign(情境=df['情境'].str.split('、')).explode('情境')
    df['情緒'] = df['情緒'].str.strip()
    df['情境'] = df['情境'].str.strip()
    return df

# 首頁：語言與情緒按鈕
if menu == "首頁":
    st.subheader("🌐 請選擇語言")
    langs = ["華語", "英語", "日語", "韓語"]
    lang_cols = st.columns(len(langs))
    for i, lang in enumerate(langs):
        lang_cols[i].button(lang)

    st.subheader("🎭 入門情緒")
    moods = ["開心", "難過", "戀愛", "思念", "遺憾", "心痛"]
    mood_cols = st.columns(len(moods))
    for i, mood in enumerate(moods):
        mood_cols[i].button(mood)

# 情緒探索：顯示資料
elif menu == "情緒探索":
    uploaded_file = st.file_uploader("📁 請上傳 Excel 檔案（需包含：歌名、歌手、情緒、情境、點閱率、YouTube 連結）", type="xlsx")

    if uploaded_file:
        df_exp = load_excel(uploaded_file)
        st.success("✅ 成功載入！")

        all_emotions = sorted(df_exp['情緒'].unique())
        if 'chosen_emotion' not in st.session_state:
            st.session_state.chosen_emotion = all_emotions[0]

        st.sidebar.header("🎭 請選擇情緒")
        for i in range(0, len(all_emotions), 2):
            cols = st.sidebar.columns(2)
            for j in range(2):
                if i + j < len(all_emotions):
                    emo = all_emotions[i + j]
                    if cols[j].button(emo, key=f"emo_{emo}"):
                        st.session_state.chosen_emotion = emo

        emotion = st.session_state.chosen_emotion
        scene_options = df_exp[df_exp['情緒'] == emotion]['情境'].unique()
        scene = st.sidebar.selectbox("🎬 選擇情境", sorted(scene_options))

        result = df_exp[(df_exp['情緒'] == emotion) & (df_exp['情境'] == scene)][['歌名', '歌手', '情緒', '情境', '點閱率', 'YouTube 連結']].drop_duplicates()

        st.subheader("🎧 符合的歌曲")
        if result.empty:
            st.warning("❌ 找不到符合條件的歌曲")
        else:
            for _, row in result.iterrows():
                st.markdown(f"**🎵 {row['歌名']} - {row['歌手']}**")
                st.markdown(f"🎭 情緒：`{row['情緒']}` ｜ 🎬 情境：`{row['情境']}` ｜ 🔥 點閱率：{row['點閱率']}")
                st.markdown(f"[▶️ 點我聽歌]({row['YouTube 連結']})")
                st.markdown("---")
