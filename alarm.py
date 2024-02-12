import streamlit as st
import datetime
import time
import pygame
import os
import random

# Function to generate algebraic puzzles
def generate_puzzles(num_puzzles):
    puzzles = []
    for _ in range(num_puzzles):
        a = random.randint(1, 10)
        b = random.randint(0, 10)
        c = random.randint(0, 99)
        puzzle = f"{a}x + {b} = {c}"
        answer = (c - b) // a if a != 0 else "Undefined"
        puzzles.append((puzzle, answer))
    return puzzles

# Function to validate user input as integer
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to set alarm
def set_alarm(alarm_datetime, snooze_used):
    pygame.init()
    audio_path = os.path.join(os.path.dirname(__file__), "audio.wav")
    alarm_sound = pygame.mixer.Sound(audio_path)
    
    timer_text = st.empty()
    alarm_text = st.empty()
    stop_button = st.empty()
    snooze_button = st.empty()
    
    # Load puzzles
    puzzles = generate_puzzles(100)
    
    while True:
        current_time = datetime.datetime.now()
        
        if alarm_datetime <= current_time:
            alarm_text.text("Alarm!")
            alarm_sound.play(-1)  # Play on loop
            
            # Select a random puzzle
            puzzle, answer = random.choice(puzzles)
            alarm_text.text(f"Solve the equation to stop the alarm: {puzzle}")
            
            stop_button_text = st.text_input("Write your answer here:")
            if stop_button_text and is_integer(stop_button_text) and 0 <= int(stop_button_text) <= 99:
                if int(stop_button_text) == answer:
                    alarm_text.text("Correct! Alarm stopped.")
                    alarm_sound.stop()
                    break
                else:
                    alarm_text.text("Incorrect answer. Try again.")
        
        time_diff = alarm_datetime - current_time
        if time_diff.total_seconds() <= 0:
            break
        
        hours, remainder = divmod(time_diff.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        timer_text.text(f"Time left until alarm: {int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds")
        
        # Snooze button logic
        if not snooze_used:
            snooze_button_key = f"snooze_button_{id(alarm_datetime)}_{random.randint(1, 1000)}"  # Unique key
            if snooze_button.button("Snooze", key=snooze_button_key):
                alarm_datetime += datetime.timedelta(minutes=5)
                snooze_used = True
        
        time.sleep(1)  # Check every second

# Main function
def main():
    st.title("Simple Alarm Clock")
    st.markdown(
        """
        <style>
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }

            .stTextInput>div>div>div>input {
                border-radius: 10px;
                padding: 10px 15px;
            }

            .stTextInput>div>div>div {
                margin: 20px 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.write("Set the date and time for your alarm:")
    
    current_time = datetime.datetime.now()
    default_date = datetime.date(current_time.year, current_time.month, current_time.day)
    default_hour = current_time.hour
    default_minute = current_time.minute

    alarm_date = st.date_input("Date", default_date)
    alarm_hour = st.slider("Hour", 0, 23, default_hour)
    alarm_minute = st.slider("Minute", 0, 59, default_minute)

    alarm_datetime = datetime.datetime(alarm_date.year, alarm_date.month, alarm_date.day, alarm_hour, alarm_minute)
    snooze_used = False  # Initialize snooze status
    
    if st.button("Set Alarm"):
        set_alarm(alarm_datetime, snooze_used)

if __name__ == "__main__":
    main()
