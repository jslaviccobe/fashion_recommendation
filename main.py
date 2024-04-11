import os
import sys
from dotenv import load_dotenv
from preprocessor import CSVPreprocessor
from chatbot_builder import ChatbotBuilder


def main():
    load_dotenv(override=True)

    data_folder = os.path.join(os.getcwd(), "data")
    input_filepath = os.path.join(data_folder, "example_products.csv")
    output_filepath = os.path.join(data_folder, "preprocessed-data.csv")

    if not os.path.exists(data_folder):
        print(f'Data folder "{data_folder}" not found.')
        sys.exit(1)

    preprocessor = CSVPreprocessor(input_filepath)
    preprocessor.save_preprocessed_file(output_filepath)

    # If Chatbot is built without memory, "chat_history" has to be passed to the chatbot's invoke method as {}
    chatbot = ChatbotBuilder().with_memory().build(output_filepath)

    while True:
        query = input('Prompt (or type "exit" to quit): ')
        if query.lower() == "exit":
            print("Exiting...")
            break

        response = chatbot.invoke({"question": query})
        print("Answer: " + response["answer"])


if __name__ == "__main__":
    main()
