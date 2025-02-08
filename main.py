import argparse
from src.retrieval.retrieval import retrieve_best_sentence, generate_fallback_response

def main():
    parser = argparse.ArgumentParser(description="Retrieve answers from FAISS and Elasticsearch.")
    parser.add_argument("query", nargs="?", type=str, help="Enter your question to retrieve answers.")
    args = parser.parse_args()

    while True:
        # If no query was passed via CLI, ask the user interactively
        if not args.query:
            args.query = input("\n❓ Enter your question (or type 'exit' to quit): ")
        
        if args.query.lower() == "exit":
            print("👋 Exiting the program.")
            break

        answers = retrieve_best_sentence(args.query)

        if "❌ No relevant answer found!" in answers:
            print("⚠️ No relevant answer found! Generating a fallback response...")
            fallback_answer = generate_fallback_response(args.query)
            print(f"💡 Fallback Answer: {fallback_answer}")
        else:
            print("\n✅ **Top Answers:**")
            for i, ans in enumerate(answers, 1):
                print(f"{i}. {ans}\n")

        # Reset query for the next loop iteration (only matters for interactive mode)
        args.query = None

if __name__ == "__main__":
    main()
