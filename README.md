# Scientific-Calculator

🧮 Scientific Calculator Using Python
📌 About the Project

The Scientific Calculator is a desktop-based application developed using Python and Tkinter. It provides a modern, dark-themed graphical user interface (GUI) to perform basic arithmetic operations and advanced scientific calculations.

The calculator is designed to be user-friendly, efficient, and safe, with support for keyboard input, memory operations, and degree/radian modes.

✨ Features
🔢 Basic Arithmetic Operations
Addition (+)
Subtraction (−)
Multiplication (×)
Division (÷)
Modulus (%)
Decimal calculations
Power calculations (xʸ)
Square (x²)
🔬 Scientific Functions
Sine (sin)
Cosine (cos)
Tangent (tan)
Inverse Sine (asin)
Inverse Cosine (acos)
Inverse Tangent (atan)
Logarithm (log)
Natural Logarithm (ln)
Square Root (√)
Absolute Value (|x|)
Factorial (n!)
📐 Additional Features
Degree (DEG) and Radian (RAD) modes
Mathematical constants (π and e)
Memory functions:
MC – Memory Clear
MR – Memory Recall
M+ – Memory Add
M− – Memory Subtract
Clear All (AC) button
Delete (DEL) button
Calculation history display
Keyboard support
Error handling for invalid expressions
Safe expression evaluation using Python AST
Modern dark-themed graphical interface
🛠️ Technologies Used
Programming Language: Python
GUI Library: Tkinter
Mathematical Library: Math
Expression Parsing: AST
Operator Handling: Operator
Font Management: Tkinter Font
📂 Project Structure
text
Scientific-Calculator/
│
├── scientific_calculator.py
└── README.md

⚙️ Requirements
Python 3.x
Tkinter (usually included with standard Python installations)

Note: No external Python packages are required because the project uses only Python's standard library.

🚀 How to Run the Project
Step 1: Install Python

Download and install Python from:

https://www.python.org/downloads/

Step 2: Download the Project

Clone the repository using:

bash
git clone https://github.com/yourusername/Scientific-Calculator.git


Or download the ZIP file from GitHub and extract it.

Step 3: Open the Project Folder

Open the project folder in VS Code or any Python IDE.

Step 4: Run the Application

Open the terminal and execute:

bash
python scientific_calculator.py


The Scientific Calculator GUI will open on your desktop.

⌨️ Keyboard Shortcuts
Key	Function
0–9	Enter numbers
+	Addition
-	Subtraction
*	Multiplication
/	Division
%	Modulus
.	Decimal point
Enter	Calculate result
Backspace	Delete last character
Esc	Clear all
🖥️ User Interface

The application features a modern dark-themed interface with:

Easy-to-use calculator buttons
Scientific function buttons
Large calculation display
DEG/RAD mode indicator
Memory status display
Color-coded operation buttons
🔒 Safety and Error Handling

The calculator uses Python's AST (Abstract Syntax Tree) module to evaluate mathematical expressions safely instead of using Python's eval() function.

It also handles common calculation errors, including:

Division by zero
Invalid mathematical expressions
Invalid factorial inputs
Out-of-range mathematical operations
Non-finite calculation results
🎯 Project Objective

The main objective of this project is to develop a scientific calculator with a graphical user interface using Python. It demonstrates practical knowledge of Python programming, object-oriented programming, GUI development, mathematical operations, event handling, and safe expression evaluation.

🔮 Future Enhancements
Add calculation history panel.
Add scientific notation support.
Add more advanced mathematical functions.
Add customizable themes.
Add calculation history export functionality.
👨‍💻 Author

Your Name

📜 License

This project is created for educational and learning purposes.

⭐ If you find this project useful, please consider giving this repository a star!
