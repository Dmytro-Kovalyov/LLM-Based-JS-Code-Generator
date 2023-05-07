from .models import Script
from node_vm2 import NodeVM
from langchain.agents import Tool, load_tools, initialize_agent, AgentType
from langchain.chains import LLMChain
from langchain.tools import tool
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from stackapi import StackAPI
import os

class AgentService:
    """
    A class used to create a LangChain agent that generates Node.js
    code.
    """
    
    def __init__(self):
        self.llm = OpenAI(temperature=0.0)
        self.agent = self.__create_agent()

    def __create_llm_tool(self):
        """
        Function that defines a Language Model tool, which will be used
        to generate Node.js code
        """
        template = """
        You need to write a function for Node.js, output only executable code 
        make sure that it is silent, and only returns a value. 
        It is very important to use only built in functions, 
        format code as a module, that is include an "exports" before the function 
        Here is the description of the task: 
        {query}
        """
        llm_prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )
        llm_chain = LLMChain(llm=self.llm, prompt=llm_prompt)
        llm_tool = Tool(
            name="Language Model",
            func=llm_chain.run,
            description="Use this tool first of all to write code"
        )

        return llm_tool
    
    def __create_stackoverflow_tool(self):
        """
        Function that defines a StackOverflow Search tool, which uses
        the website's API to search it for an answer and then passes it
        to an llm to parse
        """
        # Get API key from environment
        STACKOVERFLOW_API_KEY = os.getenv("STACKOVERFLOW_API_KEY")
        # Create description for the tool
        class SearchInput(BaseModel):
            query: str = Field(description="should be a programming related search query")
        # Definining the tool using @tool wrapper
        @tool("StackOverflow Search", return_direct=True, args_schema=SearchInput)
        def search_stackoverflow(query: str) -> str:
                """Searches StackOverflow for the query"""
                # Init StackAPI with out API key
                SITE = StackAPI("stackoverflow", key=STACKOVERFLOW_API_KEY)
                # Search the site, sorting the output in descending order by relevance
                search = SITE.fetch("search/advanced", tagged="javascript", q=query, sort="relevance", order="desc")
                # Initialise final answer with 'error' in case we can't find anything
                final_answer = 'error'
                # Go through all the questions that fit our search
                for question in search["items"]:
                    # Find the first answered question
                    if question["is_answered"]:
                        # Get all the answers for that question
                        answers = SITE.fetch("questions/{ids}/answers", ids=[question["question_id"]], filter="withbody")
                        # Go through all the answers to the question
                        for answer in answers["items"]:
                            # Find accepted answer
                            if answer["is_accepted"]:
                                final_answer = answer["body"]
                                break
                # Parse the received answer using llm
                template = """
                You need to read through raw data received from stackoverflow 
                regarding a question asked by the user and you need to answer it 
                Here is the question: 
                {query} 
                Here is the raw data received from stackoverflow: 
                {final_answer}
                """
                stackoverflow_prompt = PromptTemplate(
                    input_variables=["query", "final_answer"],
                    template=template
                )
                return self.llm(stackoverflow_prompt.format(query=query, final_answer=final_answer))
        
        return search_stackoverflow

    def __create_tools(self):
        """
        Function that loads builtin tools and then our custom tools
        """
        tools = load_tools(["serpapi"], llm=self.llm)
        tools += [self. __create_llm_tool(), self.__create_stackoverflow_tool()]
        
        return tools

    def __create_agent(self):
        """
        Function that assembles all the necessary components
        and returns an agent
        """
        tools = self.__create_tools()

        return initialize_agent(
            tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
            max_iterations=5
        )
    
    def run_query(self, query):
        """
        Function that passes a query to the agent
        """
        template = """
        Your task is to generate code in javascript for Node.js based on the user's description. 
        Use the Language Model tool first, and if it doesn't provide a good answer use other tools 
        to search google or stackoverflow for information. Here is the user's description of the function, 
        delimited by triple backticks: 
        ```{query}``` 
        Once you know the answer, output only the code
        """
        prompt = PromptTemplate(
            input_variables=["query"],
            template=template,
        )
        return self.agent.run(prompt.format(query=query))
    
class ScriptService:
    """
    A class used to interact with the AgentService to generate Node.js
    code from user input and run it
    """
    
    agent_service = AgentService()

    def __extract_function_name(self, js_code):
        """
        Function that extracts the name of the function generated by the agent
        """
        # Cut out the name of the fucntion from between "exports." and " "
        target_word = "exports."
        func_name_start_idx = js_code.find(target_word) + len(target_word)
        func_name = js_code[func_name_start_idx:]
        func_name_end_idx = func_name.find(' ')
        func_name = func_name[:func_name_end_idx]

        return func_name

    def generate(self, description):
        """
        Function that generates a Node.js script based on user's description,
        verifies if the script runs, and if does saves it and returns id.
        """
        # Use the agent to generate a function, get its name and create a Script object
        js_code = self.agent_service.run_query(description)
        func_name = self.__extract_function_name(js_code)

        return Script(function_name=func_name, script_content=js_code)
    
    def test(self, script, params):
        """
        Function that accepts script object and parameters,
        runs the script and returns its output
        """
        # Settings for the Node VM, builtin = * means all builtin modules are allowed
        require = {
            "external": False,
            "builtin": ["*"],
            "root": './',
        }
        # Use the VM to load the function and then call it passing it test parameters
        with NodeVM(console="off", require=require) as vm:
            module = vm.run(script.script_content)
            result = module.call_member(script.function_name, *params)

        return result