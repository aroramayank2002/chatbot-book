import json


def convert_to_rasa_data(input_file, output_file):
    """
    Converts the annotated dataset into Rasa old JSON format.
    Args:
    - input_file: Path to the annotated JSON Lines file
    - output_file: Path to save the JSON in old Rasa format
    """
    rasa_data = {"rasa_nlu_data": {"common_examples": []}}

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            annotation = json.loads(line.strip())
            text = annotation["text"]
            labels = annotation["label"]

            entities = []
            for start, end, entity in labels:
                entities.append({
                    "start": start,
                    "end": end,
                    "value": text[start:end],
                    "entity": entity
                })

            rasa_data["rasa_nlu_data"]["common_examples"].append({
                "text": text,
                "intent": "get_recipe",  # Default intent; update as necessary
                "entities": entities
            })

    # Write the output JSON file in the required format
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rasa_data, f, indent=2, ensure_ascii=False)

    print(f"Converted data saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    input_file = "matar-paneer-ingridients.jsonl"  # Replace with your filename
    output_file = "data.json"  # Desired output file
    convert_to_rasa_data(input_file, output_file)

# cd /Users/mayankarora/dib/poc/chatbot-book/food_bot/documents/recipes
# rasa data convert nlu --data data.json --out nlu.yml
