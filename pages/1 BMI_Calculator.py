## Create a body mass index calculator app. It should take in height in feet or meters and weight in lbs or kilograms and return the associated body mass index. Post both the python code for your dash app and a gif screen capture of it running.

import streamlit as st
import numpy as np

st.title('Body Mass Index Calculator')
st.write("This app calculates your Body Mass Index (BMI) based on your height in feet and weight in pounds.")
## Wait for user to input height and weight

with st.form(key='my_form'):
    height = st.number_input('Enter your height in feet', value=5.0)
    weight = st.number_input('Enter your weight in pounds', value=150.0)
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    height = height * 12
    bmi = (weight / (height * height)) * 703
    bmi = np.round(bmi, 2)
    st.metric(label="Your BMI is:", value=bmi)
    if bmi < 18.5 :
        st.write("You are underweight")
    elif (bmi >= 18.5) & (bmi < 24.9) :
        st.write("You are normal weight")
    elif (bmi >= 25) & (bmi < 29.9) :
        st.write("You are overweight")
    else :
        st.write("You are obese")

st.markdown("""
    #### Guide to BMI Categories:
    - Underweight = <18.5
    - Normal weight = 18.5–24.9
    - Overweight = 25–29.9
    - Obesity = BMI of 30 or greater
""")
