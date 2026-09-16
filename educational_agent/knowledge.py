knowledge_base = {
    "operating system": 
        "An Operating System is system software that manages computer hardware and software resources.",

    "agent": 
        "An AI agent is a system that can perceive a task, make decisions, use tools, and perform actions to achieve a goal.",

    "memory": 
        "Memory allows an agent to keep relevant information from previous interactions and use it later."
}


def search_knowledge(query):
    query = query.lower()

    for topic, information in knowledge_base.items():
        if topic in query:
            return information

    return "لم أجد معلومات مناسبة في قاعدة المعرفة."