import asyncio
from agents import team, retrival_team
from symbol import clean_latex_output

fp = open("file.log", "w")

async def main():
    while True:
        user_question = input("\nEnter your question (or type 'exit' to quit): ")
        knowledge = []
        fp = open("./file.log", "w")
        if user_question.lower() == 'exit':
            print("\nExiting...\n")
            break

        retrival_task = f"question:{user_question}"
        async for result in retrival_team.run_stream(task=retrival_task):
            retrival_response = []
            if hasattr(result, 'messages') and hasattr(result.messages[-2], 'content'):
                response = str(result.messages[-2].content).replace("Retrival:", "").replace("'","").replace("\n","").replace("[","").replace("]","").replace("Retrieval:","").replace('"','').replace(",","").replace(r':\\','')
                retrival_response.extend(response.strip(",").split())
                fp.write(f"list with Duplicate Elements: \n{retrival_response}\n")
                for i in range(len(retrival_response)):
                    x=''
                    for w in retrival_response[i]:
                        if (str(w).isalpha() or str(w).isnumeric()) and w!='.':
                            x+=w
                        else:
                            x+=" "
                    if not x.isspace():
                        retrival_response[i]=x
                retrival_response = list(set(retrival_response))
                cleaned_list = [s.strip() for s in retrival_response]
                fp.write(f"\nWords retrived:\n{cleaned_list}\n")

        from retrieval import retrieve_knowledge
        knowledge = retrieve_knowledge(retrival_response)

        if not knowledge:
            fp.write("No relevant knowledge found in Neo4j.\n")
            continue

        fp.write(f"\nRetrieved knowledge:\n {knowledge}\n")

        task = f"""question: {user_question}
        context: {knowledge}
"""

        async for result in team.run_stream(task=task):
            fp.write(f"\nAgent Output\n{result}\n")
            if hasattr(result, 'messages'):
                for i in range(-2,-(len(result.messages)+1),-1):
                    if 'user' not in result.messages[i].content.lower().split():
                        response = result.messages[i].content
                        response = clean_latex_output(response)
                        print(f"\nChatbot:\n{response}\n")
                        break
                    else:
                        continue
                    
if __name__ == "__main__":
    asyncio.run(main())