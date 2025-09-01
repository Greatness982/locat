import streamlit as st
import datetime
import time
import random

# Set page configuration
st.set_page_config(
    page_title="Real-Time Chat App",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f0f2f5;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #2d333b;
        color: white;
    }
    
    /* Chat containers */
    .chat-container {
        background-color: white;
        height: calc(100vh - 200px);
        overflow-y: auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Message bubbles */
    .user-message {
        background-color: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 18px;
        margin-bottom: 10px;
        max-width: 70%;
        margin-left: auto;
        border-bottom-right-radius: 5px;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .other-user-message {
        background-color: #e9ecef;
        color: #333;
        padding: 10px 15px;
        border-radius: 18px;
        margin-bottom: 10px;
        max-width: 70%;
        margin-right: auto;
        border-bottom-left-radius: 5px;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Timestamps */
    .message-time {
        font-size: 0.7em;
        color: #6c757d;
        margin-top: 3px;
    }
    
    .user-time {
        text-align: right;
        margin-right: 10px;
    }
    
    .other-time {
        text-align: left;
        margin-left: 10px;
    }
    
    /* Contact list */
    .contact {
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .contact:hover {
        background-color: #404956;
    }
    
    .contact.active {
        background-color: #404956;
        border-left: 3px solid #007bff;
    }
    
    .contact-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .contact-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #495057;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-weight: bold;
    }
    
    .contact-details {
        display: flex;
        flex-direction: column;
    }
    
    .contact-name {
        color: #e9ecef;
        font-weight: 500;
    }
    
    .contact-status {
        font-size: 0.8em;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .online-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #28a745;
    }
    
    .offline-text {
        color: #868e96;
    }
    
    /* Input area */
    .input-area {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* Login form */
    .login-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        margin: 100px auto;
        max-width: 400px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "users" not in st.session_state:
        st.session_state.users = {}
    
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    
    if "chats" not in st.session_state:
        st.session_state.chats = {}
    
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = None
    
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    
    if "online_users" not in st.session_state:
        st.session_state.online_users = {}
    
    if "message_count" not in st.session_state:
        st.session_state.message_count = 0

# Display login form
def display_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #333;">Real-Time Chat App</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6c757d;">Sign in to start chatting</p>', unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Login", use_container_width=True):
            if username.strip():
                # Allow any username/password combination
                st.session_state.current_user = username
                
                # Add user to users list if not already there
                if username not in st.session_state.users:
                    st.session_state.users[username] = {
                        "password": password, 
                        "name": username, 
                        "online": True,
                        "last_seen": datetime.datetime.now()
                    }
                
                # Mark user as online
                st.session_state.online_users[username] = datetime.datetime.now()
                st.session_state.users[username]["online"] = True
                st.session_state.users[username]["last_seen"] = datetime.datetime.now()
                
                st.rerun()
            else:
                st.error("Please enter a username")
    
    # Demo info
    st.markdown(
        '''
        <div style="color: #6c757d; margin-top: 20px;">
            <p><strong>How to use:</strong></p>
            <p>1. Enter any username and password</p>
            <p>2. Open another browser window/tab</p>
            <p>3. Login with a different username</p>
            <p>4. Start chatting between users</p>
        </div>
        ''', 
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Display a message in the chat
def display_message(sender, message, timestamp):
    if sender == st.session_state.current_user:
        st.markdown(f'<div class="user-message">{message}<div class="message-time user-time">{timestamp}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="other-user-message">{message}<div class="message-time other-time">{timestamp}</div></div>', unsafe_allow_html=True)

# Display the chat interface
def display_chat():
    if st.session_state.current_chat:
        # Extract the other user from the chat ID
        users_in_chat = st.session_state.current_chat.split("_")
        other_user = users_in_chat[0] if users_in_chat[1] == st.session_state.current_user else users_in_chat[1]
        
        # Display chat header with online status
        is_online = other_user in st.session_state.online_users
        status_color = "#28a745" if is_online else "#6c757d"
        status_text = "Online" if is_online else "Offline"
        
        st.markdown(
            f'<div style="display: flex; align-items: center; padding: 10px; background-color: white; border-radius: 5px; margin-bottom: 10px;">'
            f'<h3 style="margin: 0; flex-grow: 1;">{other_user}</h3>'
            f'<div style="display: flex; align-items: center; gap: 5px;">'
            f'<div style="width: 10px; height: 10px; border-radius: 50%; background-color: {status_color};"></div>'
            f'<span style="color: {status_color};">{status_text}</span>'
            f'</div></div>', 
            unsafe_allow_html=True
        )
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display all messages in the current chat
        if st.session_state.current_chat in st.session_state.chats:
            for msg in st.session_state.chats[st.session_state.current_chat]:
                display_message(msg["sender"], msg["message"], msg["time"])
        else:
            st.info("No messages yet. Start the conversation!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        col1, col2 = st.columns([6, 1])
        
        with col1:
            user_input = st.text_input("Type a message...", value=st.session_state.user_input, key="user_input", label_visibility="collapsed")
        
        with col2:
            if st.button("Send", use_container_width=True):
                if user_input.strip():
                    # Ensure chat exists
                    if st.session_state.current_chat not in st.session_state.chats:
                        st.session_state.chats[st.session_state.current_chat] = []
                    
                    # Add user message to chat
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    st.session_state.chats[st.session_state.current_chat].append({
                        "sender": st.session_state.current_user, 
                        "message": user_input, 
                        "time": current_time
                    })
                    
                    # Increment message count for auto-refresh
                    st.session_state.message_count += 1
                    
                    # Clear input
                    st.session_state.user_input = ""
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Select a user from the sidebar to start messaging")

# Display the sidebar with contacts and online status
def display_sidebar():
    with st.sidebar:
        st.markdown(f'<div style="color: white; padding: 10px; background-color: #343a40; border-radius: 5px;">Logged in as: <strong>{st.session_state.current_user}</strong></div>', unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            # Mark user as offline
            if st.session_state.current_user in st.session_state.online_users:
                del st.session_state.online_users[st.session_state.current_user]
            if st.session_state.current_user in st.session_state.users:
                st.session_state.users[st.session_state.current_user]["online"] = False
                st.session_state.users[st.session_state.current_user]["last_seen"] = datetime.datetime.now()
            
            st.session_state.current_user = None
            st.rerun()
        
        st.markdown('<h3 style="color: white; margin-top: 20px;">Online Users</h3>', unsafe_allow_html=True)
        
        # Display online users count
        online_count = len(st.session_state.online_users)
        st.markdown(f'<p style="color: #868e96; margin-top: -10px;">{online_count} user(s) online</p>', unsafe_allow_html=True)
        
        # Search box
        search_term = st.text_input("Search users...", label_visibility="collapsed", placeholder="Search users")
        
        # Display other users
        other_users = [user for user in st.session_state.users.keys() if user != st.session_state.current_user]
        
        if not other_users:
            st.info("No other users online. Open another browser window/tab and log in with a different username.")
        
        for user in other_users:
            if not search_term or search_term.lower() in user.lower():
                # Determine chat ID (always alphabetical to ensure consistency)
                user1, user2 = sorted([st.session_state.current_user, user])
                chat_id = f"{user1}_{user2}"
                
                # Check if user is online
                is_online = user in st.session_state.online_users
                last_seen = "now" if is_online else st.session_state.users[user]["last_seen"].strftime("%I:%M %p") if user in st.session_state.users else "recently"
                
                if st.button(f"chat_{user}", key=user, use_container_width=True):
                    st.session_state.current_chat = chat_id
                    st.rerun()
                
                # Display contact with online status
                if st.session_state.current_chat == chat_id:
                    st.markdown(
                        f'''
                        <div class="contact active">
                            <div class="contact-info">
                                <div class="contact-avatar">{user[0] if user else "U"}</div>
                                <div class="contact-details">
                                    <div class="contact-name">{user}</div>
                                    <div class="contact-status">
                                        {"<div class='online-dot'></div> Online" if is_online else f"<span class='offline-text'>Last seen {last_seen}</span>"}
                                    </div>
                                </div>
                            </div>
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'''
                        <div class="contact">
                            <div class="contact-info">
                                <div class="contact-avatar">{user[0] if user else "U"}</div>
                                <div class="contact-details">
                                    <div class="contact-name">{user}</div>
                                    <div class="contact-status">
                                        {"<div class='online-dot'></div> Online" if is_online else f"<span class='offline-text'>Last seen {last_seen}</span>"}
                                    </div>
                                </div>
                            </div>
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )

# Main app
def main():
    local_css()
    init_session_state()
    
    # Auto-refresh every 5 seconds to check for new messages
    if st.session_state.current_user:
        if time.time() % 5 < 0.1:
            st.rerun()
    
    if st.session_state.current_user is None:
        display_login()
    else:
        # Update user's last seen time
        st.session_state.online_users[st.session_state.current_user] = datetime.datetime.now()
        st.session_state.users[st.session_state.current_user]["last_seen"] = datetime.datetime.now()
        
        # Set up layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            display_sidebar()
        
        with col2:
            display_chat()

if __name__ == "__main__":
    main()