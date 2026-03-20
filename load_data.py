import pandas as pd
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'statements.csv')

def load_and_preprocess_data():
    if not os.path.exists(DATA_PATH):
        print("Data file not found. Creating an advanced dummy dataset...")
        
        # A more comprehensive synthetic dataset to train an advanced model
        statements = [
            # True statements
            ("The Earth revolves around the Sun in an elliptical orbit.", "True"),
            ("Water is composed of two hydrogen atoms and one oxygen atom.", "True"),
            ("Python is a high-level, interpreted programming language.", "True"),
            ("Photosynthesis is the process used by plants to convert light energy into chemical energy.", "True"),
            ("The human body typically has 206 bones in adulthood.", "True"),
            ("Isaac Newton formulated the laws of motion and universal gravitation.", "True"),
            ("Mount Everest is the highest mountain above sea level.", "True"),
            ("The speed of light in a vacuum is approximately 299,792 kilometers per second.", "True"),
            ("DNA carries the genetic instructions for the development and functioning of living organisms.", "True"),
            ("The Eiffel Tower is located in Paris, France.", "True"),
            ("A year has 365 days, with a leap year having 366.", "True"),
            ("Oxygen is essential for human respiration.", "True"),
            ("Gravity is the force that attracts a body toward the center of the earth.", "True"),
            ("The Pacific Ocean is the largest and deepest of Earth's oceanic divisions.", "True"),
            ("William Shakespeare wrote the play Romeo and Juliet.", "True"),
            
            # Fake/Lie statements
            ("The Earth is completely flat and has an ice wall at the edge.", "Fake"),
            ("Humans only use 10 percent of their brain capacity.", "Fake"),
            ("Vaccines inject microchips into the human body to track people.", "Fake"),
            ("Drinking bleach can cure serious viral infections.", "Fake"),
            ("The moon landing in 1969 was staged in a Hollywood studio.", "Fake"),
            ("Bulls become enraged specifically by the color red.", "Fake"),
            ("Cracking your knuckles leads to arthritis later in life.", "Fake"),
            ("Eating carrots gives you flawless night vision.", "Fake"),
            ("Goldfish have a memory span of only three seconds.", "Fake"),
            ("Shaving hair makes it grow back thicker and significantly darker.", "Fake"),
            ("Bats are completely blind and rely solely on magic to fly.", "Fake"),
            ("The Great Wall of China is the only human-made object visible from space.", "Fake"),
            ("Lightning never strikes the same place twice.", "Fake"),
            ("Swallowed chewing gum takes seven years to digest.", "Fake"),
            ("Touching a toad will give you warts on your hands.", "Fake")
        ]
        
        df = pd.DataFrame(statements, columns=['statement', 'label'])
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
    
    return pd.read_csv(DATA_PATH)

if __name__ == '__main__':
    data = load_and_preprocess_data()
    print(f"Data loaded successfully. Total records: {len(data)}")
