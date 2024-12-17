import streamlit as st
import nbformat as nbf
import io

st.title("Convert Notebook to Slideshow")

# File Uploader for the Jupyter Notebook
uploaded_file = st.file_uploader("Choose a Jupyter Notebook file", type=["ipynb"])

if uploaded_file is not None:
    # Read the notebook from bytes
    ntbk = nbf.read(io.BytesIO(uploaded_file.getvalue()), nbf.NO_CONVERT)
    
    # Update metadata for each cell to be a slide
    for cell in ntbk.cells:
        metadata = cell.get("metadata", {})
        slideshow = metadata.get("slideshow", {})
        slideshow["slide_type"] = "slide"  # Set slide type to 'slide'
        metadata["slideshow"] = slideshow
        cell["metadata"] = metadata
    
    # Write the updated notebook to a BytesIO object
    output = io.BytesIO()
    nbf.write(ntbk, output)
    
    # Provide download option for the updated notebook
    output.seek(0)
    btn = st.download_button(
        label="Download Updated Notebook",
        data=output,
        file_name="slideshow_" + uploaded_file.name,
        mime="application/octet-stream"
    )
    
    # Instructions for user after download
    st.write("After downloading, you can convert this notebook to slides using:")
    st.code("jupyter nbconvert " + "slideshow_" + uploaded_file.name + " --to slides --post serve")

else:
    st.info("Please upload a Jupyter Notebook file to convert it to a slideshow.")