from documentchat import ChatCompletion
import streamlit as st



def LaunchDocumentChatbot():
    
    
    st.markdown(
        """
        <style>
        .title-text {
            font-size: 24px;
            color: #0066cc;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Use the custom CSS class for styling the title
    st.markdown("<p class='title-text'>Knowledge Management Document Chatbot</p>", unsafe_allow_html=True)

    # st.write("Knowledge Management  Document Chatbot")
        
    if "st_messages" not in st.session_state:
        st.session_state.st_messages = []
                

            #  # Display chat messages from history on app rerun
    for message in st.session_state.st_messages:
        with st.chat_message(message["role"]):
            # st.markdown function to display the content of the message.
            st.markdown(message["content"])
            
            
    if user_message := st.chat_input("Enter your query?"):
        
        # Display user message in chat message container
        
        
        print(user_message)
                
                # Display user message in chat message container
        st.chat_message("user").markdown(user_message)
        
        st.session_state.st_messages.append({"role":"user","content":user_message})
                
        # TO use Gpt-3 Model Response
                
        response = ChatCompletion(user_message)   
        
            
                    
        with st.chat_message("assistant"):
            st.markdown(response)
            
        ### Appending the Model genrated message to chathistory
        st.session_state.st_messages.append({"role":"assistant","content":response})
        
        
        
if __name__ == "__main__":
    LaunchDocumentChatbot()