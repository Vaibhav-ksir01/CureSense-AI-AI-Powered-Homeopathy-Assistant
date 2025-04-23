from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from config import AZURE_API_KEY, AZURE_MODEL_NAME, AZURE_API_VERSION, AZURE_ENDPOINT

# Initialize Azure OpenAI Client
client = AzureOpenAIChatCompletionClient(
    azure_deployment=AZURE_MODEL_NAME,
    model=AZURE_MODEL_NAME,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)

# Define Agents
planning_agent = AssistantAgent(
    "PlanningAgent",
    model_client=client,
    system_message="""
    You are the lead agent and the very first agent to receive the user's task. Your role is to:
        - Determine which agents need to be involved.
        - Assign the appropriate sub-tasks to your team.
        - Ensure that each agent works on their assigned sub-task and returns their output to you.
        - Collect and consolidate all the outputs from the team.
        - Once all the sub-tasks are completed, you will send the final compiled data to the next appropriate agent(s) for further processing.

    Your team includes:
        - Analyzer: Analyzes the question to understand the user's intent and provides interpretation.
        - Editor: Edits the content to make it understandable for a 6th-grade student and modifies accordingly.
        - Formule: Formats mathematical or chemical equations using standard notation and returns the result to the Editor.
        - Approval: Reviews and approves the final content if it meets all requirements, responding with 'APPROVED'.

    Assign task as:
        - Agent : sub-task

    When a task arrives:
        - You will first determine which agents should handle the sub-tasks.
        - Once an agent completes its sub-tasks, you will collect and consolidate the result.
        - After gathering all the necessary data, send it to another agent for further processing or approval, depending on the task's nature.
    
    You should ensure that tasks are efficiently assigned to the appropriate agents, taking into account:
        - For question generation: Adjust difficulty based on the assigned marks.
        - For topic explanations: Provide a simple, effective explanation with key points, fun facts, and jokes to keep it interesting.
        
    Ensure that you manage the process efficiently, track the status of tasks, and ensure that the outputs from all agents are integrated before finalizing the task. 
    You should also ensure that the task is aligned with the user's request, whether it involves generating questions, explaining a topic, or any other task.
    """
)

Analyzer = AssistantAgent(
    "Analyzer", 
    model_client=client, 
    system_message="""
    Your job is to analyze the user's question and accurately determine their intent. 
    You need to extract important information and categorize the request to help the team decide the next steps.
    - If the user is asking for an explanation, determine the complexity level.
    - If the user is asking for a question generation, assess the difficulty based on the marks.
    Provide a precise interpretation to help guide the delegation of tasks to the appropriate agents.
    """
)

Editor = AssistantAgent(
    "Editor", 
    model_client=client, 
    system_message="""
    Your responsibility is to edit and simplify the content to ensure that it is clear and easy to understand for a 6th-grade student.
    If the content needs to be revised or simplified, you should adjust the language accordingly.
    Focus on clarity, simplicity, and appropriateness for a younger audience, avoiding jargon and complex terminology.
    """
)

Formule = AssistantAgent(
    "Formule", 
    model_client=client, 
    system_message="""
    Your role is to format mathematical or chemical equations using standard, universally accepted notation.
    Remove unnecessary symbols or formatting and ensure the equations are simple, clear, and accurate.
    Focus on clarity and correctness in the representation of all expressions.
    """
)

Approval = AssistantAgent(
    "Approval",
    model_client=client, 
    system_message="""
    You are responsible for reviewing the final content and approving it if it meets all requirements.
    Ensure that the content is clear, correct, and appropriate for a 6th-grade audience.
    The content is only text dont ask for Visual Elements
    If the content needs improvements, return it to the editor with suggestions for changes.
    Once you are satisfied that the task is complete, respond with 'APPROVED'.
    """
)

Retrival_Analyzer = AssistantAgent(
    "Analyzer", 
    model_client=client, 
    system_message="Analyze the question to determine the user's intent."
    )

Retrival_agent = AssistantAgent(
    "Retrival",
    model_client=client,
    system_message="Extract what words or phrases to be searched in the database from the question and return a list of words to be searched."
    )

# Define Team
termination = TextMentionTermination("APPROVED") | MaxMessageTermination(20)
team = SelectorGroupChat(
    [planning_agent, Analyzer,Editor,Formule,Approval], 
    model_client=client, 
    termination_condition=termination
    )

retrival_termination = MaxMessageTermination(5)
retrival_team = SelectorGroupChat(
    [Retrival_agent,Retrival_Analyzer],
    model_client=client,
    termination_condition=retrival_termination
)