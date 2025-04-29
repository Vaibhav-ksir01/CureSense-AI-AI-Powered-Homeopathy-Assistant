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

# Define Chat Agents
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
    - If the user is asking for an explanation, determine the key points and concepts to cover.
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
    Focus on clarity, simplicity, and appropriateness for a younger audience, avoiding complex terminology.

    You should ensure that the content is engaging and informative, while also being suitable for the target age group, taking into account:
        - For question generation: Adjust difficulty based on the assigned marks.
        - For topic explanations: Provide a simple, effective explanation with key points, fun facts, to keep it interesting.
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

termination = TextMentionTermination("APPROVED") | MaxMessageTermination(20)
team = SelectorGroupChat(
    [planning_agent, Analyzer,Editor,Formule,Approval], 
    model_client=client, 
    termination_condition=termination
    )



# Define Intent Agents
Retrival_Analyzer = AssistantAgent(
    "Analyzer", 
    model_client=client, 
    system_message="""
    Your role is to analyze the user's question to accurately determine their intent.
    Break down the question to identify key components and clarify the user's requirements.
    Provide a concise and clear interpretation to guide the retrieval process effectively.
    """
)

Retrival_agent = AssistantAgent(
    "Retrival",
    model_client=client,
    system_message="""
    Your responsibility is to extract relevant keywords or phrases from the user's question 
    that can be used for database searches. Focus on identifying terms that are most likely 
    to yield accurate and useful results. Return a clear and concise list of these keywords.
    """
)

retrival_termination = MaxMessageTermination(5)
retrival_team = SelectorGroupChat(
    [Retrival_agent,Retrival_Analyzer],
    model_client=client,
    termination_condition=retrival_termination
)
