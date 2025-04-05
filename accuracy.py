import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton

# Target message the user needs to type
#Just an example should be calling from main 
target_message = "The quick brown fox jumps over the lazy dog."

# Variable to store the typed text and the number of mistakes
typed_text = ""
mistakes = 0

# Function to calculate final accuracy
def calculate_accuracy(mistakes, target):
    # Calculate accuracy as a percentage based on mistakes
    accuracy = (1 - mistakes / len(target)) * 100
    accuracy = max(accuracy, 0)  # Ensure accuracy doesn't go below 0%
    return accuracy

# Function to capture the typed characters and count mistakes
def capture_typing():
    global typed_text, mistakes

    # Get the current text in the input field
    typed_text = input_field.text()

    # Reset mistakes count
    mistakes = 0

    # Count the mistakes (comparing each character)
    for i in range(min(len(typed_text), len(target_message))):
        if typed_text[i] != target_message[i]:
            mistakes += 1

    # Display the mistakes in the label
    mistakes_label.setText(f"Mistakes so far: {mistakes}")

# Function to handle the final calculation when the user presses Enter
def on_submit():
    global typed_text, mistakes

    # Calculate final accuracy
    accuracy = calculate_accuracy(mistakes, target_message)

    # Update the final accuracy label
    accuracy_label.setText(f"Final Accuracy: {accuracy:.2f}%")

    # Print the final accuracy to the terminal
    print(f"Final Accuracy: {accuracy:.2f}%")

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle("Typewriter Test with Final Accuracy")

# Create a layout
layout = QVBoxLayout()

# Create the target message label
target_label = QLabel("Type the message below:")
target_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
layout.addWidget(target_label)

# Create the target message display
target_message_label = QLabel(target_message)
target_message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
layout.addWidget(target_message_label)

# Create the input field
input_field = QLineEdit()
input_field.setFont(input_field.font().setPointSize(14))
input_field.setFixedWidth(400)
layout.addWidget(input_field)

# Create the mistakes display label
mistakes_label = QLabel("Mistakes so far: 0")
mistakes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
layout.addWidget(mistakes_label)

# Create the accuracy display label
accuracy_label = QLabel("Final Accuracy: 100.00%")
accuracy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
layout.addWidget(accuracy_label)

# Create a button for submitting the text
submit_button = QPushButton("Submit")
layout.addWidget(submit_button)

# Connect the text input field to the typing capture function
input_field.textChanged.connect(capture_typing)

# Connect the button to finalize the accuracy calculation
submit_button.clicked.connect(on_submit)

# Set the layout for the window
window.setLayout(layout)

# Show the window
window.show()

# Start the application loop
sys.exit(app.exec())

