import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with new API syntax
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="FitGenie AI", layout="centered")
st.title("🏋️ FitGenie AI - Personalized Workout & Diet Planner")

with st.form("user_input_form"):
    name = st.text_input("Your Name", "")
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (in cm)", min_value=100, max_value=250)
    weight = st.number_input("Weight (in kg)", min_value=30, max_value=200)
    diet = st.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    weekly_time = st.slider("Workout Time Per Week (in hours)", 1, 20)
    goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintain"])
    submit = st.form_submit_button("Generate My Plan")

if submit:
    if not name or height == 0 or weight == 0 or age == 0:
        st.warning("Please fill in all fields properly.")
        st.stop()

    with st.spinner("Generating your plan..."):
        prompt = f"""
        You are a certified fitness and nutrition expert. Based on this profile:

        Name: {name}
        Age: {age}, Gender: {gender}, Height: {height} cm, Weight: {weight} kg
        Diet: {diet}, Weekly Workout Time: {weekly_time} hrs, Goal: {goal}

        Return:
        1. A weekly workout schedule (day-by-day)
        2. Daily focus (cardio/strength/rest)
        3. A daily meal plan (3 meals + 2 snacks) with calories & macros
        4. Ensure diet aligns with preference and fitness goal
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            plan = response.choices[0].message.content
            st.markdown("## 🧠 Your Personalized Fitness Plan")
            st.markdown(plan)
        except Exception as e:
            st.error(f"Failed to generate plan: {e}")
