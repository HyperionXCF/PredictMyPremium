# Insurance Premium Category Predictor

A simple machine learning project that predicts the insurance premium category — **Low**, **Medium**, or **High** — based on user input data. This is my first ML project using a **Random Forest Classifier**, served with a **FastAPI** backend and a **Streamlit** frontend.

## Features

- ML model: Random Forest Classifier  
- Backend: FastAPI (for serving the model via API)  
- Frontend: Streamlit (for input and displaying results)  
- Input fields: Age, BMI, Income, Lifestyle risk, Occupation, City type, etc.
## Demo 
![Demo](assets/demo.gif)

## How it Works

1. User enters data through the Streamlit UI.
2. Frontend sends data to FastAPI backend.
3. Backend returns the predicted premium category.
4. Result is shown on the Streamlit page.

## Try it out on 
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://predictmypremium.streamlit.app/)
