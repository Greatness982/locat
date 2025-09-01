import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="💬 WhatsApp-Style App", layout="wide")

# ---------------- Session Setup ----------------
if "users" not in st.session_state:
    st.session_state["users"] = set()
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ---------------- User Login ----------------
st.sidebar.title("👤 User Login")
username = st.sidebar.text_input("Enter your name:", key="username_input")

if username:
    st.session_state["users"].add(username)

# ---------------- Online Users ----------------
st.sidebar.subheader("🟢 Online Users")
if st.session_state["users"]:
    for user in st.session_state["users"]:
        st.sidebar.write(f"✅ {user}")
else:
    st.sidebar.write("No users online")

# ---------------- Chat Layout ----------------
st.title("💬 WhatsApp-Style Chat")

chat_box = st.container()

# Show messages
with chat_box:
    for user, msg in st.session_state["messages"]:
        if user == username:
            st.markdown(f"<div style='text-align:right; background:#dcf8c6; padding:8px; border-radius:8px; margin:5px; display:inline-block;'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; background:#fff; padding:8px; border-radius:8px; margin:5px; display:inline-block;'><b>{user}:</b> {msg}</div>", unsafe_allow_html=True)

# ---------------- Message Input ----------------
msg = st.text_input("Type a message:", key=f"msg_{time.time()}")

if st.button("Send"):
    if username and msg.strip():
        st.session_state["messages"].append((username, msg.strip()))
        st.experimental_rerun()
