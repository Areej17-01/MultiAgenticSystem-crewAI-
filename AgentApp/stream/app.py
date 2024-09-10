
import streamlit as st
from module import Crew, researcher, writer, research, write, image_agent, image_task  ,Router_Agent,router_task
import os
import shutil 
# Define the two Crew instances
crew_yt = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    verbose=True,
    planning=False,  # Disable planning
)

crew_img = Crew(
    agents=[image_agent],
    tasks=[image_task, image_task],
    verbose=True,
    planning=False,  # Disable planning
)

rag_crew = Crew(
    agents=[Router_Agent],
    tasks=[router_task],
    verbose=True,
    full_output=True,

)

st.title("Research and Content Creation App")

# Input from the user for the topic to research
topic = st.text_input("Enter a topic for research:")

# File uploader to allow uploading of images and PDFs
uploaded_file = st.file_uploader("Upload an image or PDF", type=["png", "jpg", "jpeg", "pdf"])

# Button to trigger the research and content creation process
if st.button("Run Research Task"):
    if topic or (uploaded_file and uploaded_file.type.startswith("image/")):
        # Dictionary to store the inputs
        query_data = {}

        # If a topic is provided and no file is uploaded, execute crew_yt
        if topic and not uploaded_file:
            st.write(f"Starting research on: {topic}")
            query_data["topic"] = topic
            
            # Execute the research process using crew_yt
            crew_yt.kickoff(inputs={"topic": str(topic)})  

            file_path = r'blog-posts\\new_post.md'

            # Open and read the file
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    st.write('result')
                    # Display the blog post content on Streamlit
                    st.write(content)
                    print("chain finished.")
                    # Create a downloadable button for the blog post
                    st.download_button(
                        label="Download Blog Post",
                        data=content,
                        file_name="new_post.md",
                        mime="text/markdown"
                    )
            

            except FileNotFoundError:
                st.write(f"The file at {file_path} was not found.")
            except Exception as e:
                st.write(f"An error occurred: {e}")
                st.write("Research completed for the topic.")

        # If a file is uploaded, show the details
        if uploaded_file:
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }
            query_data["file"] = file_details
            st.write("Uploaded file details:", file_details)

            if file_details['filetype'].startswith("image/"):
                # Save the uploaded image
                save_dir='image'
                os.makedirs(save_dir, exist_ok=True)
                file_extension = os.path.splitext(uploaded_file.name)[1]
                image_path = os.path.join(save_dir, f"newimg{file_extension}")
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Display the image
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                st.write("Running image agent...")

                #image crew
                
                
                response=crew_img.kickoff(inputs={"topic": str(topic)})  
                st.write(response.raw)
              
                if os.path.exists(save_dir):
                    shutil.rmtree(save_dir)
                    st.write("Temporary directory deleted successfully after processing the image.")
                st.write('process finished')






            elif file_details['filetype'] == "application/pdf":
                # Path to save the uploaded PDF
                save_path = os.path.join("RAG", "newpdf.pdf")
                
                # Ensure the folder exists, create if not
                os.makedirs("RAG", exist_ok=True)
                
                # Save the uploaded file to the specified path
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                print("PDF file saved successfully to RAG/newpdf.pdf")
                
                response=rag_crew.kickoff(inputs={"topic": topic}) 
                st.write('RESULTS:')
                st.write(response.raw)
               
                if os.path.exists('RAG'):
                    shutil.rmtree('RAG')
                    st.write("Temporary directory deleted successfully after processing the pdf.")

