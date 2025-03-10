# LangChain as a Coding Assistant: Fibonacci & Unit Testing

![Fibonacci Sequence](langchain-fibonacci.webp)

## Abstract
LangChain provides a powerful way to generate both **code** and **unit tests** automatically using LLMs. This publication explores how LangChain generates a **Python function for the Fibonacci sequence** and its corresponding **unit tests**, showcasing AI-assisted software development.

## Methodology
### **1️⃣ User Provides Arguments**
When you run the script:
```sh
python main.py --language python --task "generate Fibonacci sequence"
```
- `--language` specifies the programming language (e.g., Python, JavaScript).
- `--task` specifies the code to generate (e.g., "generate Fibonacci sequence").

### **2️⃣ Generating Code Using LangChain**
LangChain takes the arguments and constructs a prompt using a `PromptTemplate`:
```python
code_prompt = PromptTemplate(
    input_variables=["task", "language"],
    template="Write a standalone {language} function that will {task}. "
             "Only provide the function implementation with a proper function signature and return statement. "
             "Do not include any test cases, assertions, or example usages."
)
```
#### **Example Prompt Sent to OpenAI:**
```
Write a standalone Python function that will generate a Fibonacci sequence.
Only provide the function implementation with a proper function signature and return statement.
Do not include any test cases, assertions, or example usages.
```
#### **Generated Code Example:**
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

### **3️⃣ Generating Unit Tests with LangChain**
Once the function is generated, it is passed into `test_prompt`:
```python
test_prompt = PromptTemplate(
    input_variables=["code", "language"],
    template="Write a full unit test in {language} using unittest for the following function. "
             "Include an import statement assuming the function is defined in a separate module named `your_module.py`. "
             "Only provide the test class and methods, do not include the function implementation itself:\n\n{code}"
)
```
#### **Example Prompt Sent to OpenAI:**
```
Write a full unit test in Python using unittest for the following function.
Include an import statement assuming the function is defined in a separate module named `fibonacci.py`.
Only provide the test class and methods, do not include the function implementation itself.
```
#### **Generated Unit Test Example:**
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

## Results
### **Run the Fibonacci Function**
```sh
python fibonacci.py
```

### **Run the Unit Tests**
✅ **Method 1: Run Directly**
```sh
python test_fibonacci.py
```
✅ **Method 2: Using unittest**
```sh
python -m unittest test_fibonacci.py
```
✅ **Method 3: Run All Tests in the Directory**
```sh
python -m unittest discover
```

## Conclusion
LangChain successfully generated both a **function** and **unit tests**, reducing manual effort. However, **human oversight is essential** to refine AI-generated code, especially for edge cases.

### **✅ Key Takeaways:**
- LangChain can accelerate **boilerplate code writing & testing**.
- AI-generated code still requires **verification & debugging**.
- Future improvements in **LLMs may lead to fully autonomous coding agents**.

---

✍️ **Author:** Mary Ann Dizon
🔗 **Connect:** [LinkedIn Profile](https://www.linkedin.com/in/mary-ann-dizon-ba336436/) / [GitHub](https://github.com/mctrinity)
📌 **Publication on Ready Tensor**
