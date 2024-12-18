import random
import wandb
def extract_answer(text):
    # Extract the answer field
    answer_start = text.find('"answer": "') + len('"answer": "')
    answer_end = text.find('"', answer_start)
    answer_content = text[answer_start:answer_end]

    # Clean the answer content (if needed)
    cleaned_answer = answer_content.strip()

    # Extract and clean the explanation content
    cleaned_explanation = extract_and_clean_explanation(text)

    # Return a dictionary with the extracted and cleaned fields
    return {
        "answer": cleaned_answer,
        "explanation": cleaned_explanation
    }

def extract_and_clean_explanation(text):
    # Locate the start of the explanation content
    start = text.find('explanation": "') + len('explanation": "')

    # Find the end quote of the explanation text
    end = text.find('"', start)

    # Extract the content between the quotes
    explanation_content = text[start:end]

    # Remove all double quotes from the explanation content
    cleaned_explanation = explanation_content.replace('"', '')

    return cleaned_explanation

def get_similar_question(question_category):
  similar_questions = dataset['train'].filter(lambda x: question_category in x['categories'])
  return random.choice(similar_questions)

def get_in_context_prompt(prompt, categories, answer, explanations):
    formatted_prompt = prompt.copy()
    formatted_prompt[1]['content'][5]['text'] = formatted_prompt[1]['content'][5]['text'].replace('/category{}', str(categories))
    formatted_prompt[1]['content'][8]['text'] = formatted_prompt[1]['content'][8]['text'].replace('/solution{}', answer)
    formatted_prompt[1]['content'][8]['text'] = formatted_prompt[1]['content'][8]['text'].replace('/explanation{}', str(explanations))
    return formatted_prompt

def test_split(dataset, model=None, prompt=None, processor=None, **params):
    # Extract arguments from kwargs
    subset = params.get('subset', 'MENSA Norway')
    start = params.get('start', 0)
    end = params.get('end', None)
    decoding_strategy = params.get('decoding_strategy', 'greedy')
    top_p = params.get('top_p', 0.9)
    num_beams = params.get('num_beams', 2)
    max_new_tokens = params.get('max_new_tokens', 512)
    device = params.get('device', 'GPU')

    # Select the dataset split
    if subset is None:
        dataset_subset = dataset['train']
    else:
        print(f"Subset: {subset}")
        dataset_subset = dataset['train'].filter(lambda x: x['subset'] == subset)

    # Determine the range of indices
    dataset_length = len(dataset_subset)
    if end is None or end > dataset_length:
        end = dataset_length

    # Slice the filtered subset based on start and end
    dataset_subset = dataset_subset.select(range(start, end))

    print(f"Strategy: {decoding_strategy}")
    print(f"Using device: {device}")
    answers = []

    for i in range(len(dataset_subset)):
        question_img = dataset_subset[i]['question_img']
        answer_img = dataset_subset[i]['multiple_answer_img']

        if prompt == prompts['difficulty_prompt']:
          prompt = get_difficulty_prompt(prompt,dataset_subset[i]['difficulty'])
        elif prompt == prompts['in_context_prompt']:
          similar_question = get_similar_question(random.choice(dataset_subset[i]['categories']))
          prompt = get_in_context_prompt(
              prompt, similar_question['categories'],
              similar_question['correct_answer'],
              similar_question['explanations']
          )


        # Apply the provided prompt template if available, otherwise use a default
        text_prompt = processor.apply_chat_template(prompt, add_generation_prompt=True)
        #print(text_prompt)

        if prompt == prompts['in_context_prompt']:
          inputs = processor(
                text=text_prompt,
                images=[question_img, answer_img, similar_question['question_img'], similar_question['multiple_answer_img']],
                return_tensors="pt"
          )
        else:
          # Prepare inputs with text and images
          inputs = processor(
                text=text_prompt,
                images=[question_img, answer_img],
                return_tensors="pt"
          )

        # Ensure inputs are moved to the correct device

        if device == 'GPU':
            inputs = inputs.to("cuda")
        elif device == 'CPU':
            inputs = inputs.to("cpu")
        else:
            print(f"Invalid compute device '{device}'. Defaulting to CPU.")
            inputs = inputs.to("cpu")

       # inputs = inputs.to('cpu')
        # Move the model to the correct device

        # Generate output from the model
        if decoding_strategy == 'greedy':
            output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)
        elif decoding_strategy == 'top_p':
            output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, top_p=top_p)
        elif decoding_strategy == 'beam_search':
            output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, num_beams=num_beams)
        else:
            print(f"Invalid decoding strategy '{decoding_strategy}'. Using default greedy strategy.")
            output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)

        # Process generated text
        output_text = processor.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        #print(f"\nOutput: {output_text}")
        # Convert output to answer dicts
        answer = extract_answer(output_text[0])
        if answer:
            answer['difficulty'] = dataset_subset[i]["difficulty"]
            answer['question_id'] = dataset_subset[i]["question_id"]
            answer['is_correct'] = answer['answer'] == dataset_subset[i]['correct_answer']
            answers.append(answer)
        else:
            print(f"No valid JSON found in the generated text from question {dataset_subset[i]['question_id']}.")

    return answers

def get_score(answers, dataset):
  num_correct_answers = sum(answer['answer'] == dataset['train'][answer['question_id']]['correct_answer'] for answer in answers)
  percentage_correct_answers = (num_correct_answers/len(answers)) * 100
  subset = dataset['train'][answers[0]['question_id']]['subset']
  if subset == 'MENSA Norway' or subset == 'MENSA Denmark':
    iq_score = num_correct_answers * (145/len(answers))
  elif subset == 'MENSA Sweden':
    iq_score = num_correct_answers * (126/len(answers))
  else:
    print(f"Invalid subset '{subset}'. Using default IQ score of 0.")
    iq_score = 0
  return (num_correct_answers, percentage_correct_answers, iq_score)

def get_difficulty_prompt(prompt, difficulty):
    updated_prompt = prompt.copy()  # Create a copy to avoid mutation
    updated_prompt[1]['content'][0]['text'] = updated_prompt[1]['content'][0]['text'].format(difficulty)
    return updated_prompt

def log_answers_to_wandb(answers, mensa_score):
    # Create a W&B Table to store answers
    table = wandb.Table(columns=["question_id", "answer", "is_correct", "difficulty", "explanation"])

    for answer in answers:
        table.add_data(
            answer.get("question_id"),
            answer.get("answer"),
            answer.get("is_correct"),
            answer.get("difficulty"),
            answer.get("explanation"),
        )

    # Log the table to W&B
    wandb.log({"answers_table": table})

    # Log score and metrics
    wandb.log({
        "correct_answers": mensa_score[0],
        "correct_percentage": mensa_score[1],
        "IQ_score": mensa_score[2],
    })