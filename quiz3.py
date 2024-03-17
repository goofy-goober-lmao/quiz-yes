import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from selenium import webdriver
from ttkbootstrap import Style

# Define the related answers for each question
related_answers = {
    "What is the capital of France?": ["Paris", "Marseille", "Lyon", "Nice", "Toulouse", "Bordeaux", "Lille", "Strasbourg"],
    "What is the largest planet in our solar system?": ["Jupiter", "Saturn", "Neptune", "Uranus", "Earth", "Venus", "Mars", "Mercury"],
    "Who wrote 'A Christmas Carol'?": ["Charles Dickens", "Jane Austen", "William Shakespeare", "Mark Twain", "Ernest Hemingway", "George Orwell", "J.K. Rowling", "F. Scott Fitzgerald"],
    "What year did the Titanic sink?": ["1912", "1913", "1911", "1910", "1914", "1915", "1916", "1917"],
    "What is the chemical symbol for water?": ["H2O", "CO2", "O2", "NH3", "CH4", "NO2", "SO2", "NaCl"],
    "Who painted the Mona Lisa?": ["Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso", "Michelangelo", "Rembrandt", "Claude Monet", "Salvador Dalí", "Edvard Munch"],
    "What is the powerhouse of the cell?": ["Mitochondria", "Ribosome", "Endoplasmic reticulum", "Nucleus", "Golgi apparatus", "Lysosome", "Cell membrane", "Cytoplasm"],
    "How many continents are there?": ["7", "5", "6", "8", "4", "3", "9", "10"]
}

# Define the questions, answers, and explanations
questions = {
    "What is the capital of France?": ("Paris", "Paris is the capital city of France."),
    "What is the largest planet in our solar system?": ("Jupiter", "Jupiter is the largest planet in our solar system."),
    "Who wrote 'A Christmas Carol'?": ("Charles Dickens", "A Christmas Carol was written by Charles Dickens."),
    "What year did the Titanic sink?": ("1912", "The Titanic sank in the year 1912."),
    "What is the chemical symbol for water?": ("H2O", "The chemical symbol for water is H2O."),
    "Who painted the Mona Lisa?": ("Leonardo da Vinci", "The Mona Lisa was painted by Leonardo da Vinci."),
    "What is the powerhouse of the cell?": ("Mitochondria", "Mitochondria are often referred to as the powerhouse of the cell."),
    "How many continents are there?": ("7", "There are 7 continents on Earth.")
}

# global variable to store selected mode
selected_mode = "Easy"

# Global variables for quiz
correct_answers = 0
total_questions = 4 if selected_mode == "Easy" else len(questions)
report = ""
incorrect_questions = []
start_time = 0


def start_quiz_with_difficulty(difficulty):
    # Initialize variables
    global correct_answers, report, start_time, incorrect_questions, selected_questions, quiz_ended
    correct_answers = 0
    incorrect_questions = []
    report = ""
    start_time = time.time()
    quiz_ended = False

    # Filter questions based on difficulty
    if difficulty == "Easy":
        if len(questions) <= 4:
            selected_questions = list(questions.items())
        else:
            selected_questions = random.sample(list(questions.items()), 4)
    else:
        selected_questions = list(questions.items())

    # Start asking questions
    ask_question(selected_questions)

def ask_question(questions_list):
    if questions_list and not quiz_ended:
        question, (answer, explanation) = questions_list.pop(0)
        choices = [(answer, explanation)]  # Choices should be a list of tuples
        create_question_window(question, choices, questions_list)
    else:
        # No more questions, show quiz report
        show_quiz_report()

def create_question_window(question, choices, questions_list):
    root = tk.Toplevel()
    root.title("Quiz")
    root.geometry("600x400")
    style = Style(theme="flatly")

    label = ttk.Label(root, text=question, font=("Helvetica", 16))
    label.pack(pady=20)

    # Display the number of questions answered and left
    question_number = total_questions - len(questions_list) + 1
    question_info = f"Question {question_number}/{total_questions}"
    question_label = ttk.Label(root, text=question_info)
    question_label.pack()

    # Shuffle the related answers for the current question
    random.shuffle(related_answers[question])

    # Select a subset of related answers as choices for the current question
    other_choices = random.sample(related_answers[question], min(len(related_answers[question]), 3))

    # Add the correct answer back to the choices list
    other_choices.append(choices[0][0])

    # Shuffle the choices to ensure the correct answer isn't always in the same position
    random.shuffle(other_choices)

    # Create buttons for choices
    for choice in other_choices:
        # Create a button for each choice
        choice_button = ttk.Button(root, text=choice, command=lambda btn_text=choice: check_answer(btn_text, choices, questions_list, root))
        choice_button.pack(fill="x", padx=20, pady=5)  # Reduced pady for better spacing




def check_answer(choice, choices, questions_list, root):
    user_answer = choice
    correct_choice, explanation = choices[0]  # Get the correct answer from the first item in the choices list

    if user_answer == correct_choice:
        global correct_answers
        correct_answers += 1
    else:
        incorrect_questions.append(questions_list[0][0])  # Append the question with incorrect answer

    root.destroy()  # Close the question window
    ask_question(questions_list[1:])  # Ask the next question, excluding the current one


def show_quiz_report():
    global correct_answers, incorrect_questions, quiz_ended
    end_time = time.time()
    total_time = end_time - start_time
    total_questions_asked = correct_answers + len(incorrect_questions)  # Calculate total questions asked
    if total_questions_asked == 0:
        score = 0  # Handle the case where no questions were asked
    else:
        score = (correct_answers / total_questions_asked) * 100  # Calculate score
    report_text = f"Correct Answers: {correct_answers}\n"
    report_text += f"Incorrect Answers: {len(incorrect_questions)}\n"
    report_text += f"\nTotal Time taken: {round(total_time, 2)} seconds\nScore: {score:.2f}%"  # Format score to two decimal places

    messagebox.showinfo("Quiz Report", report_text)

    # Log results to quiz_results.txt
    with open("quiz_results.txt", "a") as file:
        file.write(report_text)
        file.write("\n\n")

    open_youtube_video(incorrect_questions)
    quiz_ended = True


def open_youtube_video(incorrect_questions):
    urls = {
        "What is the capital of France?": "https://worldpopulationreview.com/countries/france/capital",
        "Who wrote 'A Christmas Carol'?": "https://en.wikipedia.org/wiki/A_Christmas_Carol",
        "Who painted the Mona Lisa?": "https://www.pariscityvision.com/en/paris/museums/louvre-museum/the-mona-lisa-history-and-mystery",
        "What do cells use to generate their energy?": "https://www.genome.gov/genetics-glossary/Mitochondria",
        "How many continents are there?": "https://education.nationalgeographic.org/resource/Continent/",
        "What year did the Titanic sink?": "https://www.history.com/topics/early-20th-century/titanic",
        "What is the chemical symbol for water?": "https://www.thoughtco.com/water-chemistry-4133657",
        "What is the powerhouse of the cell?": "https://www.britannica.com/science/cell-biology",
        "What is the largest planet in our solar system?": "https://science.nasa.gov/jupiter/"
    }

    driver = webdriver.Chrome()  # Initialize webdriver
    try:
        for question in incorrect_questions:
            if question in urls:
                url = urls[question]
                driver.execute_script("window.open('" + url + "');")  # Open URL in new window
                # Switch to the new window
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the WebDriver instance
        driver.quit()


# Create main window
window = tk.Tk()
window.title("Quiz Application")

# Set up style for the GUI
style = Style(theme='flatly')

# Flag to track if the quiz has ended
quiz_ended = False

# Function to start the quiz
def play_quiz():
    difficulty_menu()

# Function to select difficulty
def difficulty_menu():
    difficulty_window = tk.Toplevel(window)
    difficulty_window.title("Select Difficulty")
    difficulty_window.geometry("300x200")

    easy_button = ttk.Button(difficulty_window, text="Easy", command=lambda: start_quiz_with_difficulty("Easy"))
    hard_button = ttk.Button(difficulty_window, text="Hard", command=lambda: start_quiz_with_difficulty("Hard"))

    easy_button.pack(pady=20)
    hard_button.pack(pady=20)

# Create play button
play_button = ttk.Button(window, text="Play Quiz", command=play_quiz)
play_button.pack(pady=50)

# Start the application
window.mainloop()
