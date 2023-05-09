from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import torch
import numpy as np

model = BertForQuestionAnswering.from_pretrained('bert-model')

tokenizer_for_bert = BertTokenizer.from_pretrained('bert-tokenizer')



def bert_question_answer(question, passage, max_len=500):
    input_ids = tokenizer_for_bert.encode(question, passage, max_length=max_len, truncation=True)
    sep_index = input_ids.index(102)
    len_question = sep_index+1
    len_passage = len(input_ids) - len_question
    segment_ids = [0]*(len_question) + [1]*(len_passage)
    tokens = tokenizer_for_bert.convert_ids_to_tokens(input_ids)
    start_token_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))[0]
    end_token_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))[1]

    start_token_scores = start_token_scores.detach().numpy().flatten()
    end_token_scores = end_token_scores.detach().numpy().flatten()

    answer_start_index = np.argmax(start_token_scores)
    answer_end_index = np.argmax(end_token_scores)

    start_token_score = np.round(start_token_scores[answer_start_index], 2)
    end_token_score = np.round(end_token_scores[answer_end_index], 2)

    answer = tokens[answer_start_index] 

    for i in range(answer_start_index + 1, answer_end_index + 1):
        if tokens[i][0:2] == '##':  
            answer += tokens[i][2:] 
        else:
            answer += ' ' + tokens[i]  

    # If the answer didn't find in the passage
    if ( answer_start_index == 0) or (start_token_score < 0 ) or  (answer == '[SEP]') or ( answer_end_index <  answer_start_index):
        answer = "Sorry!, I could not find an answer in the passage."
    
    return answer