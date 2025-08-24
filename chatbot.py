from search_engine import smart_answer

def chatbot():
    print("🤖 Indian GK Chatbot (Google-powered)")
    print("Ask me about Indian Polity, History, or Geography.")
    print("Type 'quit' to exit.\n")
    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() == "quit":
            print("Bot: Goodbye 👋")
            break
        answer, url = smart_answer(query)
        print("Bot:", answer)
        if url:
            print("Source:", url)

if __name__ == "__main__":
    chatbot()
