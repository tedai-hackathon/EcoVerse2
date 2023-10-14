import streamlit as st
# from dashboard import func

def main():
   st.title("Ecoverse")
   st.header("Helping in your solar energy journey")

    # Create a form
   with st.form(key='my_form'):
      address = st.text_input(label='Enter your address', placeholder= '555 California Street, San Francisco')
      description = st.text_area(label='Tell us about your location', placeholder= 'What is the sq ft area, What is the usable area, Near San Marie Square')

        # Create a submit button
      submit_button = st.form_submit_button(label='Submit')

    # Display the data after submission
   if submit_button:
      if address:
         st.write(f"Your address: {address}")
      if description:
         st.write(f"Information: {description}")
   

if __name__ == "__main__":
   main()
