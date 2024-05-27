import csv
import yaml

csv_file = 'data.csv'
intents = []
responses = []

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        example = row[1].split()
        example = example[: -1]
        example = ' '.join(example)
        data_split = row[1].split()
        data_intent = data_split[-1]
        intent = f"inquire_{data_intent}"
        response = row[2]
        intents.append((intent, example))
        responses.append((intent, response))

nlu_data = {'version': '2.0', 'nlu': []}
intent_examples = {}

for intent, example in intents:
    formatted_intent = f'{intent}'
    if formatted_intent not in intent_examples:
        intent_examples[formatted_intent] = []
    intent_examples[formatted_intent].append(f"- {example}")

for intent, examples in intent_examples.items():
    nlu_data['nlu'].append({
        'intent': intent,
        'examples': examples
    })

# Write to nlu.yml
with open('nlu.yml', 'w', encoding='utf-8') as file:
    file.write("version': '3.1'\n")
    file.write("nlu:\n")
    for item in nlu_data['nlu']:
        file.write(f"- intent: {item['intent']}\n")
        file.write(f"  examples: |\n")
        for example in item['examples']:
            file.write(f"    {example}\n")

print("nlu.yml file generated successfully.")

# Create domain.yml content
domain_data = {
    'version': '3.1',
    'intents': list(intent for intent, _ in intents),
    'responses': {},
    'session_config': {'session_expiration_time': 60, 'carry_over_slots_to_new_session': True}
}
for intent, response in responses:
    domain_data['responses'][f'utter_{intent}'] = [{'text': response}]

# Create stories.yml content
stories_data = {'version': '3.1', 'stories': []}
for intent, _ in intents:
    story = {
        'story': intent,
        'steps': [
            {'intent': intent},
            {'action': f'utter_{intent}'}
        ]
    }
    stories_data['stories'].append(story)


# Write to domain.yml
with open('domain.yml', 'w', encoding='utf-8') as file:
    yaml.dump(domain_data, file, sort_keys=False, allow_unicode=True)

# Write to stories.yml
with open('stories.yml', 'w', encoding='utf-8') as file:
    yaml.dump(stories_data, file, sort_keys=False, allow_unicode=True)

print("YML files generated successfully.")
