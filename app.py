if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ 成功讀取 Excel！")

        # 拆分欄位
        df_exp = df.copy()
        df_exp['情緒'] = df_exp['情緒'].str.split('、')
        df_exp['情境'] = df_exp['情境'].str.split('、')
        df_exp = df_exp.explode('情緒').explode('情境')
        df_exp['情緒'] = df_exp['情緒'].str.strip()
        df_exp['情境'] = df_exp['情境'].str.strip()

        # 🎛️ sidebar 選擇情緒與情境
        st.sidebar.header("🎭 請選擇情緒")
        all_emotions = sorted(df_exp['情緒'].dropna().unique())
        chosen_emotion = st.sidebar.selectbox("情緒", all_emotions)

        st.sidebar.header("🎬 請選擇情境")
        scene_options = sorted(df_exp[df_exp['情緒'] == chosen_emotion]['情境'].dropna().unique())
        chosen_scene = st.sidebar.selectbox("情境", scene_options)

        # 📊 結果過濾與呈現
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
                if '圖片連結' in row and pd.notna(row['圖片連結']):
                    st.markdown(f"<img src='{row['圖片連結']}' class='song-cover'>", unsafe_allow_html=True)
                st.markdown(f"<h3>🎵 <b>{row['歌名']}</b> - <i>{row['歌手']}</i></h3>", unsafe_allow_html=True)
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
