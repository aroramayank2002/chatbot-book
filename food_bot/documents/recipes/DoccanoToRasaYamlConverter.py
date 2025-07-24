import json
import yaml


def doccano_to_rasa_yaml(input_file: str, output_file: str):
    """
    Converts a Doccano JSON file into a Rasa-compatible YAML file.

    Args:
        input_file (str): Path to the input Doccano JSON file.
        output_file (str): Path to the output Rasa YAML file.
    """
    # Load Doccano JSON file
    with open(input_file, "r") as f:
        doccano_data = json.load(f)

    # Create Rasa YAML structure
    rasa_data = {"version": "3.0", "nlu": []}

    for entry in doccano_data:
        text = entry["text"]
        labels = entry["label"]

        # Replace text with entities in Rasa YAML format
        annotated_text = text
        for start, end, entity in sorted(labels, reverse=True):  # Reverse to avoid index shifting
            annotated_text = (
                    annotated_text[:start]
                    + f"[{annotated_text[start:end]}]({entity})"
                    + annotated_text[end:]
            )

        # Append example to Rasa YAML data
        rasa_data["nlu"].append({
            "intent": "inform",  # Default intent, change as needed
            "examples": f"- {annotated_text}"
        })

    # Save the Rasa YAML data to a file
    with open(output_file, "w") as f:
        yaml.dump(rasa_data, f, allow_unicode=True)

    print(f"Rasa-compatible YAML saved as '{output_file}'")


def main():
    """
    Main function to convert Doccano JSON to Rasa YAML.
    """
    # File paths (customize as needed)
    input_file = "aalu-gobi-ingredients"  # Replace with your Doccano JSON file path
    output_file = "nlu.yml"  # Replace with your desired output YAML file path

    # Convert and save
    print(f"Converting '{input_file}' to '{output_file}'...")
    doccano_to_rasa_yaml(input_file, output_file)


if __name__ == "__main__":
    main()