prompts = {
    'prompt_1': [
        {
            'role': 'system',
            'content': 'Please reason step by step'
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'image',
                },
                {
                    'type': 'text',
                    'text': 'Analyze the previous image: a grid of images with one cell marked with the symbol ?. Identify any visual or logical patterns within rows and columns to understand what the missing cell should contain.'
                },
                {
                    'type': 'image',
                },
                {
                    'type': 'text',
                    'text': 'Analyze the previous image: This image shows all possible answer choices. Each choice has a unique drawing labeled with a letter above it, which you can select from to complete the missing cell in the first image based on the identified pattern.'
                },
                {
                    'type': 'text',
                    'text': 'Using the two images, determine the pattern in the first image and select the letter above the drawing in the second image that best completes the missing cell. Return your answer in the following JSON format: {"answer": your selected letter, "explanation": your reasoning here}. Do not use "" symbols within the explanation inside the json. It is extremelly important that the answer is given in the requested json format. Make sure and double check the answer given is in the json format requested. If you won\'t give a correct json format answer, you will be penalized.'
                }
            ]
        }
    ],
    'prompt_2': [
        {
            'role': 'system',
            'content': 'Please reason step by step'
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'image',
                },
                {
                    'type': 'text',
                    'text': 'Analyze the previous image: a grid of images with one cell marked with the symbol ?. Identify any visual or logical patterns within rows and columns to understand what the missing cell should contain.'
                },
                {
                    'type': 'image',
                },
                {
                    'type': 'text',
                    'text': 'Analyze the previous image: This image shows all possible answer choices. Each choice has a unique drawing labeled with a letter above it, which you can select from to complete the missing cell in the first image based on the identified pattern.'
                },
                {
                    'type': 'text',
                    'text': 'Using the two images, determine the pattern in the first image and select the letter above the drawing in the second image that best completes the missing cell. Return your answer in the following JSON format: {"answer": your selected letter, "explanation": your reasoning here}. Do not use "" symbols within the explanation inside the json. It is extremelly important that the answer is given in the requested json format. Make sure and double check the answer given is in the json format requested. If you won\'t give a correct json format answer, you will be penalized.'
                }
            ]
        }
    ],
    'prompt_3': [
        {
            'role': 'system',
            'content': 'Please reason step by step'
        },
        {
            'role': 'user',
            'content': [
                {
                    'type': 'image',
                },
                {
                    'type': 'text',
                    'text': 'Analyze carefully the previous image: its made up of a grid of 6 cells. Each cell has a drawing inside of it, except the last one which has a ? symbol. You goal is to analyze each cell and try to find a pattern along the columns, the rows and the diagonals, in order to understand what the missing cell should contain.'
                },
                {
                    'type': 'image',
                },
                {
                    'type': 'text',
                    'text': 'Analyze carefully the previous image: This image shows all possible answer choices. Each choice has a unique drawing and is labeled with a letter above it. Select the correct drawing to complete the previous grid based on the identified pattern.'
                },
                {
                    'type': 'text',
                    'text': 'Using the two images, determine the pattern in the first image and select the letter above the drawing in the second image that best completes the missing cell. Return your answer in the following JSON format: {"answer": your selected letter,"explanation": your reasoning here}. Do not use "" symbols within the explanation inside the json.'
                }
            ]
        }
    ],
    'analyst_prompt': [
        {'role': 'system', 'content': 'You are a methodical and detail-oriented analyst, tasked with meticulously examining complex IQ test patterns. Your responses must be precise, well-reasoned, and logical. Treat each question with the absolute seriousness.'},
        {'role': 'user', 'content': [
            {'type': 'image'},
            {'type': 'text', 'text': 'Inspect the previous image carefully. It is a grid with one cell marked as "?". Detect any consistent patterns across rows, columns an diagonals in order to find the replacement inside the missing cell.'},
            {'type': 'image'},
            {'type': 'text', 'text': 'Examine the image displaying answer choices, each marked with a letter. Deduce the most suitable choice based on the previously identified pattern.'},
            {'type': 'text', 'text': 'Submit your answer using the following JSON format, with thorough reasoning for your selection: {"answer": chosen letter, "explanation": reasoning}. Refrain from using extraneous symbols within the explanation.'}
        ]}

    ],
    'difficulty_prompt': [
        {'role': 'system', 'content': 'You will be given 2 images regarding a visual iq test. The first image is the question, while the second image contain several solutions, but only one is the correct answer. You will be given the difficulty of each question. The difficulty can be of value 1 (easy), 2 (medium), 3 (hard). The harder the question, the more careful you will have to be at analyzing the question image.'},
        {'role': 'user', 'content': [
            {'type':'text', 'text': 'Difficulty of the question: {}'},
            {'type': 'image'},
            {
                    'type': 'text',
                    'text': 'Analyze the previous image: a grid of images with one cell marked with the symbol ?. Identify any visual or logical patterns within rows,columns and diagonals to understand what the missing cell should contain.'
            },
            {'type': 'image'},
            {
                    'type': 'text',
                    'text': 'Analyze the previous image: This image shows all possible answer choices. Each choice has a unique drawing labeled with a letter above it, which you can select from to complete the missing cell in the first image based on the identified pattern.'
            },
            {
                    'type': 'text',
                    'text': 'Using the two images, determine the pattern in the first image and select the letter above the drawing in the second image that best completes the missing cell. Return your answer in the following JSON format: {"answer": your selected letter, "explanation": your reasoning here}. Do not use "" symbols within the explanation inside the json. It is extremelly important that the answer is given in the requested json format. Make sure and double check the answer given is in the json format requested. If you won\'t give a correct json format answer, you will be penalized.'
            }
        ]}
    ],
    'in_context_prompt':[
        {'role': 'system', 'content': 'You will be given 2 images regarding a visual iq test. The first image is the question, while the second image contain several solutions, but only one is the correct answer. You will also be given a question and a solution of a similar problem. Using the given explanation, you will have to find a similar approach to solve the problem.'},
        {'role': 'user', 'content': [
            {'type': 'image'},
            {
                    'type': 'text',
                    'text': 'Analyze the previous image: a grid of images with one cell marked with the symbol ?. Identify any visual or logical patterns within rows,columns and diagonals to understand what the missing cell should contain.'
            },
            {'type': 'image'},
            {
                    'type': 'text',
                    'text': 'Analyze the previous image: This image shows all possible answer choices. Each choice has a unique drawing labeled with a letter above it, which you can select from to complete the missing cell in the first image based on the identified pattern.'
            },
            {'type':'image'},
            {
                    'type': 'text',
                    'text': 'This is a similar question to the one you were given. The category of the problem is: /category{}'
            },
            {'type': 'image'},
            {
                    'type': 'text',
                    'text': 'These are the possible answers to the previous question.'
            },
            {
                'type': 'text',
                'text':'The correct answer to the previous question is: /solution{}. The explanation for why the answer given is correct is: /explanation{}.'
            },
            {
                    'type': 'text',
                    'text': 'Using the two images, and the example problem given, determine the pattern in the first image. Select the letter above the drawing in the second image that best completes the missing cell. Return your answer in the following JSON format: {"answer": your selected letter, "explanation": your reasoning here}. Ensure the answer is formatted correctly in JSON without "" symbols within the explanation. If the JSON format is incorrect, it will result in a penalty.'
            }

        ]
      }
    ]
}