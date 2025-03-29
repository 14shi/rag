import json
from config import *
from openai import OpenAI
from config import *


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def segment_text(text, segment_length=500, overlap=100):
    """
    根据指定的段落长度和重叠长度，将文本分段
    """
    segments = []
    start = 0
    while start < len(text):
        end = start + segment_length
        segments.append(text[start:end])
        start += segment_length - overlap
    return segments


def get_embedding_model():
    return EMBEDDING_MODELS[EMBEDDING_MODEL_NAME]

def get_llm_embedding(input):
    model = get_embedding_model()
    client = OpenAI(
        base_url = model['base_url'],
        api_key = model['api_key']
    )
    response = client.embeddings.create(
        model = model['model_name'],
        input = input,
        encoding_format = "float"
    )
    return response


def get_llm_chat(messages, model_name, stream=False):
    model = LLM_MODELS[model_name]
    client = OpenAI(
        base_url = model['base_url'],
        api_key = model['api_key']
    )
    response = client.chat.completions.create(
        model = model['model_name'],
        messages = messages,
        temperature = 0.7,
        stream = stream
    )
    return response


def json_response(status, message, data=None, errors=None):
    response = {
        'status': status,
        'message': message
    }
    if data is not None:
        response['data'] = data
    if errors is not None:
        response['errors'] = errors
    return json.dumps(response)


if __name__ == '__main__':
    # resp = get_llm_embedding('陈华编程 LLM-RAG 课程')
    # print(resp)
    # print(len(resp.data[0].embedding))

    resp = get_llm_chat([
        {'role': 'user', 'content': '给我讲个笑话.'}
    ], 'gpt-4o-mini')
    print(resp)