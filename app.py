import streamlit as st
import os
import tempfile
import zipfile

from rag_engine import process_code_files, answer_query

# -- Streamlit page configuration
st.set_page_config(page_title="CodeDoc RAG", page_icon="📝", layout="centered")

# -- Custom CSS for vibrant visuals
st.markdown("""
<style>
    .main { background: linear-gradient(110deg, #fbeee6 0%, #e4efff 100%); font-family: 'Nunito', sans-serif;}
    .stButton>button {
        background: linear-gradient(90deg, #53bffa 50%, #b171f8 100%);
        color:white; border-radius:8px; font-size:1.05em;
        padding:0.7em 2.3em; border:0; transition:0.2s;
    }
    .stButton>button:hover { box-shadow: 0 0 0 3px #b171f8; }
    .stTextInput>div>input { border-radius:8px; border:2px solid #e0e6ff; }
    .stMarkdown h1, .stMarkdown h2 { color: #6d28d9;}
    .stExpanderHeader { color: #3a2e56; font-size:1.11em;}
</style>
""", unsafe_allow_html=True)

# -- Big 'About' heading
st.markdown("""
<h1 style='
    font-size:3.5em;
    font-weight:900;
    background: linear-gradient(45deg,#ff6ec4,#7873f5,#4ade80,#facc15);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom:0.2em;
'>CodeDoc RAG</h1>
<p style='
    font-size:1.18em;
    color:#5a5a5a;
    font-family:"Segoe UI",Tahoma,Geneva,Verdana,sans-serif;
'>
Meet <b>CodeDoc RAG</b>: Your friendly, interactive assistant for understanding <u>your own codebases</u>! Upload a zipped project and start exploring—no AI jargon, no fuss.
</p>
""", unsafe_allow_html=True)

# -- Conversational onboarding (one-time per session)
if "visited" not in st.session_state:
    st.session_state.visited = True
    st.markdown(
      "<div style='background:#fffbe6;padding:16px 24px;border-radius:8px;margin-bottom:12px'><b>👋 Welcome!</b> Upload your zipped project and start asking questions—see code insights appear instantly.<br><i>Begin by dropping a zip file below...</i></div>",
      unsafe_allow_html=True
    )

# -- Session state for docs and Q&A history
if "docs" not in st.session_state: st.session_state.docs = None
if "qa_history" not in st.session_state: st.session_state.qa_history = []

# -- Project ZIP uploader
st.header("1️⃣ Upload your code.zip project:")
uploaded_file = st.file_uploader("Choose a .zip file from your computer", type="zip")

# Helper: Inline instructions if user wants help
with st.expander("💡 How to prepare your ZIP?"):
    st.markdown("- Only include **source files** you want to analyze.\n- File and folder names should avoid special characters.\n- Max size: 100MB.")

# -- Upload/Process zip: progress, feedback, code chunk previews
if uploaded_file and st.session_state.docs is None:
    st.toast("Unpacking your code...hold on 👀", icon="📦")
    with st.spinner("Extracting ZIP..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "repo.zip")
            with open(zip_path, "wb") as f: f.write(uploaded_file.read())
            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref: zip_ref.extractall(tmpdir)
                st.progress(40, "Scanning your files...")
                docs = process_code_files(tmpdir)
                st.progress(100, "Almost done!")
                st.session_state.docs = docs
                st.success(f"🎉 Ready! {len(docs)} code pieces found. Preview below.")
                st.balloons()
                # -- Preview up to 5 code chunk filenames
                code_preview = '\n'.join([f'• `{doc.get("filename","<untitled>")}`' for doc in docs[:5]])
                remain_count = max(0, len(docs)-5)
                st.markdown(f"**Sample files parsed:**\n{code_preview}\n{'_(and '+str(remain_count)+' more...)_' if remain_count else ''}")
            except zipfile.BadZipFile:
                st.error("Not a valid zip file. Please try again.", icon="❗")
            except Exception as e:
                st.error(f"Error: {e}", icon="❗")

# -- Q&A Interaction section, retains history, lets user provide feedback
if st.session_state.docs:
    st.write("-----")
    st.header("2️⃣ Ask your questions ✏️")
    query = st.text_input("Ask a question about your code...", key="ask",
                          placeholder="E.g. What does main.py do?")
    if query:
        with st.spinner("Let me dig for answers! 💡"):
            try:
                answer = answer_query(query, st.session_state.docs)
                st.session_state.qa_history.append((query, answer))
                st.snow()
            except Exception as e:
                st.error(f"Failed: {e}", icon="🙁")

    if st.session_state.qa_history:
        st.write("---")
        st.markdown("### Your Q&A so far")
        for idx, (q, a) in reversed(list(enumerate(st.session_state.qa_history))):
            with st.expander(f"Q: {q}", expanded=(idx==len(st.session_state.qa_history)-1)):
                st.markdown(a.strip())
                st.button("👍 Helpful!", key=f"up_{idx}", help="Was this answer helpful?")
                st.button("👎 Not Helpful", key=f"dn_{idx}", help="Let us know if this needs improvement.")

else:
    st.info("⬆️ Upload a project ZIP to get started.", icon="💡")

# -- Animated, friendly footer
st.markdown("---")
st.markdown(
    "<center style='color:#bbb'><small>Hand-crafted for code explorers. <span style='color:#d295fa'>✨</span></small></center>",
    unsafe_allow_html=True
)
