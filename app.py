import streamlit as st
import ollama
import time

def init_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def display_chat_messages():
    """Display chat messages from history"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def get_ollama_streaming_response(messages):
    """Get streaming response from Ollama model"""
    try:
        stream = ollama.chat(
            model='schroneko/gemma-2-2b-jpn-it',
            messages=messages,
            stream=True
        )
        return stream
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

def main():
    st.title("ローカルSLMチャットボット")
    st.caption("Powered by Ollama & Gemma 2b")

    # Initialize session state
    init_session_state()

    # Display chat messages
    display_chat_messages()

    # Chat input
    if prompt := st.chat_input("メッセージを入力してください..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response with streaming
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Prepare messages for the model
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # Get streaming response
            try:
                for chunk in get_ollama_streaming_response(messages):
                    if 'message' in chunk:
                        content = chunk['message'].get('content', '')
                        full_response += content
                        # Display the updated response in real-time
                        message_placeholder.markdown(full_response + "▌")
                        time.sleep(0.01)  # Small delay for smooth streaming effect
                
                # Final update without cursor
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            except Exception as e:
                message_placeholder.markdown(f"エラーが発生しました: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"エラーが発生しました: {str(e)}"})

if __name__ == "__main__":
    main()