def process_file():
    try:
        filename = input("Enter the filename to process: ")
        with open(filename) as inputFile:
            content = inputFile.read()

        word_count = len(content.split(' '))
            
        uppercase_content = content.upper()
        with open('output.txt', 'w') as outputFile:
            outputFile.write(uppercase_content + "\n\n")
            outputFile.write(f"Word Count: ${word_count}")

        print("Processing complete. Results written to output.txt")
    except FileNotFoundError:
        print(f"'{filename}' Not Found!")

process_file()