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
