import os
import json

def generate_minecraft_item_jsons():
    """
    Generates JSON files for Minecraft items based on user input.

    The user provides a directory and a list of item names.
    For each item name, a JSON file is created in the specified directory
    with a specific Minecraft model structure.
    """
    print("Welcome to the Minecraft Item JSON Generator!")

    # 1. Ask for the directory to save files
    while True:
        output_directory = input("Please enter the directory where you want to save the JSON files: ").strip()
        if not output_directory:
            print("Directory cannot be empty. Please try again.")
            continue
        try:
            os.makedirs(output_directory, exist_ok=True)
            print(f"Using directory: {os.path.abspath(output_directory)}")
            break
        except OSError as e:
            print(f"Error creating directory '{output_directory}': {e}. Please enter a valid path.")

    item_names = []
    print("\nPlease enter item names, one per line.")
    print("Type 'done' (case-insensitive) on a new line when you are finished.")

    # 2. Take a list of items, one per line, until 'done'
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == 'done':
            break
        if user_input:  # Only add non-empty inputs
            item_names.append(user_input)

    if not item_names:
        print("\nNo items were entered. No JSON files will be generated.")
        return

    print(f"\nGenerating JSON files for {len(item_names)} item(s)...")

    # 3. Write a JSON file for each entry
    for item in item_names:
        # Construct the JSON content
        json_content = {
            "model": {
                "type": "minecraft:model",
                "model": f"leg:item/{item}"
            }
        }

        # Define the output file path
        file_name = f"{item}.json"
        file_path = os.path.join(output_directory, file_name)

        try:
            # Write the JSON content to the file
            with open(file_path, 'w') as f:
                json.dump(json_content, f, indent=2)
            print(f"Successfully created: {file_name}")
        except IOError as e:
            print(f"Error writing file {file_name}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred for {file_name}: {e}")

    print("\nJSON generation complete!")
    print(f"All files are saved in: {os.path.abspath(output_directory)}")

# Entry point for the script
if __name__ == "__main__":
    generate_minecraft_item_jsons()
