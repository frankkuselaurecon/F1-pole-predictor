import streamlit as st
# Set the background color of the entire app

def main():
    
    st.title("F1 Pole Predictor")

    st.markdown("Welcome to the F1 Prediction Game! Predict the 10th place driver and earn points.")

    # Get user's guess
    user_guess = st.text_input("Enter your guess for the 10th place driver:", "")

    # Display the actual result (for demo purposes)
    actual_result = "Fernando Alonso"
    st.info(f"Actual 10th place driver: {actual_result}")

    # Calculate points based on user's guess and display the result
    points = 10
    st.success(f"You scored {points} points for your guess!")

# Run the app
if __name__ == "__main__":
    main()