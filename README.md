# 📌 LangChain Code & Unit Test Generation Guide

This guide explains how the LangChain script generates code and unit tests, along with instructions for creating the necessary files and running the tests.

---

## **🚀 How the LangChain Script Works**
### **1️⃣ User Provides Arguments**
When you run the script:
```sh
python main.py --language python --task "return a list of numbers"
```
- `--language` specifies the programming language (e.g., Python, JavaScript).
- `--task` specifies the code to generate (e.g., "return a list of numbers").

---

### **2️⃣ Generate Code Using a Prompt Template**
The script takes the arguments and passes them to the `code_prompt`:
```python
code_prompt = PromptTemplate(
    input_variables=["task", "language"],
    template="Write a standalone {language} function that will {task}. "
             "Only provide the function implementation with a proper function signature and return statement. "
             "Do not include any test cases, assertions, or example usages."
)
```
Example Prompt Sent to OpenAI:
```
Write a standalone Python function that will return a list of numbers.
Only provide the function implementation with a proper function signature and return statement.
Do not include any test cases, assertions, or example usages.
```
Generated Code Example:
```python
def generate_numbers():
    return [1, 2, 3, 4, 5]
```

---

### **3️⃣ Generate a Unit Test Based on the Code**
Once the function is generated, it is passed into `test_prompt`:
```python
test_prompt = PromptTemplate(
    input_variables=["code", "language"],
    template="Write a full unit test in {language} using unittest for the following function. "
             "Include an import statement assuming the function is defined in a separate module named `your_module.py`. "
             "Only provide the test class and methods, do not include the function implementation itself:\n\n{code}"
)
```
Example Prompt Sent to OpenAI:
```
Write a full unit test in Python using unittest for the following function.
Include an import statement assuming the function is defined in a separate module named `your_module.py`.
Only provide the test class and methods, do not include the function implementation itself:

def generate_numbers():
    return [1, 2, 3, 4, 5]
```
Generated Test Example:
```python
import unittest
from your_module import generate_numbers

class TestGenerateNumbers(unittest.TestCase):
    def test_generate_numbers(self):
        self.assertEqual(generate_numbers(), [1, 2, 3, 4, 5])

if __name__ == '__main__':
    unittest.main()
```

---

## **🔗 LangChain Script (`main.py`)**

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import argparse
import os

# Load environment variables
load_dotenv()

# Ensure API key is loaded
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Missing OpenAI API Key! Ensure it's set in .env or manually in os.environ.")

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("--task", default="return a list of numbers")
parser.add_argument("--language", default="python")
args = parser.parse_args()

# Initialize OpenAI model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# ✅ Enforce function-only output
code_prompt = PromptTemplate(
    input_variables=["task", "language"],
    template="Write a standalone {language} function that will {task}. "
             "Only provide the function implementation with a proper function signature and return statement. "
             "Do not include any test cases, assertions, or example usages."
)

# ✅ Enforce test-only output
test_prompt = PromptTemplate(
    input_variables=["code", "language"],
    template="Write a full unit test in {language} using unittest for the following function. "
             "Only provide the test class and methods, do not include the function implementation itself:\n\n{code}"
)

# Chain A: Generate function code
code_chain = code_prompt | llm | StrOutputParser()

# Chain B: Generate the unit test based on the generated function
test_chain = test_prompt | llm | StrOutputParser()

# ✅ Correct `RunnableLambda` to return a dictionary with both `code` and `test`
full_chain = (
    RunnableLambda(lambda x: {"task": x["task"], "language": x["language"]})  # Prepare input
    | code_chain  # Generate function code
    | RunnableLambda(lambda code: {"code": code, "language": args.language})  # Pass both `code` and `language`
    | RunnableLambda(lambda x: {"code": x["code"], "test": test_chain.invoke(x)})  # Generate test and return both
)

# Execute chain and correctly extract outputs
result = full_chain.invoke({
    "task": args.task,
    "language": args.language
})

# ✅ Ensure correct access to dictionary output
print(">>>>>>>> GENERATED CODE:")
print(result["code"])  # Print only the function

print(">>>>>>>> GENERATED TEST:")
print(result["test"])  # Print only the test
```

---

## **📌 Example: Running LangChain for Fibonacci Function**
### **Run the LangChain Script**
```sh
python main.py --language python --task "generate Fibonacci sequence"
```

### **Generated Fibonacci Function (`fibonacci.py`)**
```python
def generate_fibonacci_sequence(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fibonacci_sequence = [0, 1]
    for i in range(2, n):
        next_num = fibonacci_sequence[i-1] + fibonacci_sequence[i-2]
        fibonacci_sequence.append(next_num)

    return fibonacci_sequence
```

### **Generated Unit Test for Fibonacci (`test_fibonacci.py`)**
```python
import unittest
from fibonacci import generate_fibonacci_sequence

class TestGenerateFibonacciSequence(unittest.TestCase):

    def test_generate_fibonacci_sequence_with_n_0(self):
        self.assertEqual(generate_fibonacci_sequence(0), [])

    def test_generate_fibonacci_sequence_with_n_1(self):
        self.assertEqual(generate_fibonacci_sequence(1), [0])

    def test_generate_fibonacci_sequence_with_n_2(self):
        self.assertEqual(generate_fibonacci_sequence(2), [0, 1])

    def test_generate_fibonacci_sequence_with_n_5(self):
        self.assertEqual(generate_fibonacci_sequence(5), [0, 1, 1, 2, 3])

    def test_generate_fibonacci_sequence_with_n_10(self):
        self.assertEqual(generate_fibonacci_sequence(10), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])

if __name__ == '__main__':
    unittest.main()
```
---

## **📌 Example: Running and Testing Fibonacci Function**
### **Run the Fibonacci Function**
```sh
python fibonacci.py
```

### **Run the Fibonacci Unit Test**
#### ✅ **Method 1: Run Directly**
```sh
python test_fibonacci.py
```
#### ✅ **Method 2: Using `unittest`**
```sh
python -m unittest test_fibonacci.py
```
#### ✅ **Method 3: Run All Tests in the Directory**
```sh
python -m unittest discover
```

---

## **🎯 Next Steps**
- **Try different `--task` values** to generate various functions and tests.
- **Modify the LangChain script to save the outputs directly into files.**
- **Experiment with different programming languages by changing `--language`.**

🚀 Now you're ready to generate, save, and test your code efficiently! Let me know if you have any questions. 😊

