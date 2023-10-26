import streamlit as st
from documentchatbotui import *
from PIL import Image
import base64


# Initialize session state
if 'present_page' not in st.session_state:
    st.session_state['present_page'] = 0
    st.session_state['present_sub_page'] = 0

# Define functions for each page
def page_1a():
    st.session_state['present_page'] = 0
    st.session_state['present_sub_page'] = 0
    LaunchDocumentChatbot()

def page_1b():
    st.session_state['present_page'] = 0
    st.session_state['present_sub_page'] = 1
    st.write("This is Page 1b")

def page_1c():
    st.session_state['present_page'] = 0
    st.session_state['present_sub_page'] = 2
    st.write("This is Page 1c")

def page_2a():
    st.session_state['present_page'] = 1
    st.session_state['present_sub_page'] = 0
    st.write("This is Page 2a")

def page_2b():
    st.session_state['present_page'] = 1
    st.session_state['present_sub_page'] = 1
    st.header("Text Generation App")

    choice = st.selectbox(
        "Select the type of file you want to upload?", ("txt", "py")
    )

    st.write("You have selected:", choice)

    if choice == "txt":
        uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    else:
        uploaded_file = st.file_uploader("Upload a python file", type=["py"])

    if uploaded_file is not None:
        txt_input = uploaded_file.read()

    ip = st.radio(
        "Do you want to do in-context learning? 👉",
        key="incontext_learning",
        options=["yes", "no"],
    )

    result = []
    with st.form('summarize_form', clear_on_submit=True):
        submitted = st.form_submit_button('Submit')
        with st.spinner('Calculating...'):
            if submitted:
                if ip == 'yes':
                    response = generate_response(txt_input, choice, incontext_learning=True)
                    result.append(response)
                else:
                    response = generate_response(txt_input, choice, incontext_learning=False)
                    result.append(response)
    
    if len(result):
        st.info(response)

    if len(result) > 0:
        download_filename = "generated_output.txt"
        st.download_button(
            label="Download Output",
            data=response.encode('utf-8'),
            key="download_output",
            file_name=download_filename,
            mime="text/plain",
        )

def page_3a():
    st.session_state['present_page'] = 2
    st.session_state['present_sub_page'] = 0
    st.write("This is Page 3a")

def page_3b():
    st.session_state['present_page'] = 2
    st.session_state['present_sub_page'] = 1
    st.write("This is Page 3b")

def page_4a():
    st.session_state['present_page'] = 3
    st.session_state['present_sub_page'] = 0
    st.write("This is Page 4a")

def page_4b():
    st.session_state['present_page'] = 3
    st.session_state['present_sub_page'] = 1
    st.write("This is Page 4b")

if __name__ == "__main__":
    # Load the CG logo
    logo_path = 'Capgeminilogo.png'
    
    logo = Image.open(logo_path)

    # Add custom CSS for styling
    custom_css = f"""
        <style>
        .title-text {{
            font-size: 20px;
            color: #327da8;
        }}
        .logo-text-container {{
            display: flex;
            align-items: center;
        }}
        .sidebar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 200px;
            padding: 20px;
            background-color: #f0f0f0;
            border-right: 1px solid #ddd;
        }}
        .sidebar-item {{
            padding: 8px;
            border-radius: 5px;
            margin: 2px;
            cursor: pointer;
        }}
        .active {{
            background-color: #327da8;
            color: white !important;
            font-weight: bold;
        }}
        .content {{
            margin-left: 220px;
            padding: 20px;
        }}
        .logo {{
            width: 150px;
        }}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Create a container for the logo and text side by side
    st.markdown(
        f'<div class="logo-text-container"><img class="logo" src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}"><span class="title-text">GENERATIVE AI POWERED SOFTWARE PRODUCT ENGINEERING</span></div>',
        unsafe_allow_html=True
    )

    # Create a sidebar
    st.sidebar.title("Categories")

    page_hierarchy = {
        "Knowledge Management": {
            "Sub-Pages": ["Document Chatbot", "Database Chatbot", "Code Chatbot"],
        },
        "Solutioning": {
            "Sub-Pages": ["Document to User-Story", "Code to User Story"],
        },
        "Coding": {
            "Sub-Pages": ["Code Generation", "Code Transformation"],
        },
        "Testing": {
            "Sub-Pages": ["Unit Test Creation", "Test Cases Generation"],
        }
    }

    # Initialize selected_section and selected_page with defaults
    selected_section = list(page_hierarchy.keys())[st.session_state['present_page']]
    selected_page = page_hierarchy[selected_section]["Sub-Pages"][st.session_state['present_sub_page']]
    print(selected_section)
    print(selected_page)

    #JavaScript function to handle the click events on sub-categories
    
    

    # Create a Streamlit sidebar with buttons for the sub-pages under the selected section
    for section, sub_pages in page_hierarchy.items():
        st.sidebar.subheader(section)
        for sub_page in sub_pages["Sub-Pages"]:
            css_class = "active" if sub_page == selected_page else ""
            button = f'<div class="sidebar-item {css_class}" onclick="setActive(\'{section}\', \'{sub_page}\')">{sub_page}</div>'
            st.sidebar.markdown(button, unsafe_allow_html=True)

    # Display the selected section name
    st.sidebar.markdown(f"**Selected Section:** {selected_section}")

    # Display the selected sub-page name
    st.sidebar.markdown(f"**Selected Sub-Page:** {selected_page}")

    # Update the page hierarchy with the corresponding functions
    page_hierarchy["Knowledge Management"]["Document Chatbot"] = page_1a
    page_hierarchy["Knowledge Management"]["Database Chatbot"] = page_1b
    page_hierarchy["Knowledge Management"]["Code Chatbot"] = page_1c
    page_hierarchy["Solutioning"]["Document to User-Story"] = page_2a
    page_hierarchy["Solutioning"]["Code to User Story"] = page_2b
    page_hierarchy["Coding"]["Code Generation"] = page_3a
    page_hierarchy["Coding"]["Code Transformation"] = page_3b
    page_hierarchy["Testing"]["Unit Test Creation"] = page_4a
    page_hierarchy["Testing"]["Test Cases Generation"] = page_4b

    # Display the content based on the selected sub-page
    if page_hierarchy[selected_section][selected_page]:
        page_hierarchy[selected_section][selected_page]()
    else:
        st.write("This page is currently under construction.")
