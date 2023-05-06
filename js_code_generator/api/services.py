from .models import Script
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from node_vm2 import NodeVM
import os

# Make sure to set OPENAI_API_KEY environment variable

class ScriptService:

    @staticmethod
    def generate(description):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)
        template = """
        You need to write a function for Node.js, output only executable code\
        make sure that it is silent, and only returns a value. \
        It is very important to use only built in functions, \
        format code as a module, that is include an "exports" before the function \
        Here is the description of the task:
        {description} \
        """
        prompt = PromptTemplate(
            input_variables=["description"],
            template=template,
        )
        js_code = llm(prompt.format(description=description))
        func_name = ScriptService.extract_function_name(js_code)
        return Script(function_name=func_name, script_content=js_code)

    @staticmethod
    def extract_function_name(js_code):
        target_word = "exports."
        func_name_start_idx = js_code.find(target_word) + len(target_word)
        func_name = js_code[func_name_start_idx:]
        func_name_end_idx = func_name.find(' ')
        func_name = func_name[:func_name_end_idx]
        return func_name

    @staticmethod
    def test(script, params):
        require = {
            "external": False,
            "builtin": ["*"],
            "root": './',
        }
        with NodeVM(console="off", require=require) as vm:
            module = vm.run(script.script_content)
            result = module.call_member(script.function_name, *params)
        return result