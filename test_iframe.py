import streamlit as st
import streamlit.components.v1 as components

st.sidebar.page_link("pages/02_Data_Upload.py", label="Target Link")

st.markdown('<button id="html-btn">Click Me (HTML)</button>', unsafe_allow_html=True)

components.html("""
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const parentDoc = window.parent.document;
        const btn = parentDoc.getElementById("html-btn");
        if(btn) {
            btn.addEventListener("click", function(e) {
                e.preventDefault();
                const links = parentDoc.querySelectorAll('a');
                for(let link of links) {
                    if(link.href && link.href.includes("Data_Upload")) {
                        link.click();
                        break;
                    }
                }
            });
        }
    });
</script>
""")
