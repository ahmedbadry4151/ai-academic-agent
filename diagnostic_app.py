"""
Quick diagnostic to see what's in the Streamlit app output
"""
import streamlit as st

st.write("If you see this, Streamlit is running!")

# Test imports
try:
    from utils.watsonx_client import WatsonxClient
    st.success("✓ Watsonx client imported")
    
    client = WatsonxClient()
    st.success(f"✓ Client initialized with model: {client.model_id}")
    
    # Simple test
    with st.spinner("Testing API call..."):
        response = client.generate_text("Say hello in JSON: {\"message\": \"hello\"}")
        
    if response:
        st.write(f"Response length: {len(response)}")
        st.code(response)
    else:
        st.error("Empty response!")
        
except Exception as e:
    st.error(f"Error: {e}")
    import traceback
    st.code(traceback.format_exc())
