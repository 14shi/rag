import os

CURRENT_VERSION = '1.0.0'
DEBUG = True

TIMEZONE = 'Asia/Shanghai'

# You can generate a strong key using `openssl rand -base64 42`.
SECRET_KEY = 'CAUoej9GdRX55DeVJGGOb6hTt47MWCs+AuNclM9lDeZP5v5gQZ3IAGsK'

# PostgreSQL database config
DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_USERNAME = 'postgres'
DB_PASSWORD = 'vl8jhGRflh6fIeJu'
DB_DATABASE = 'llm_rag'

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Milvus database config
MILVUS_HOST = '127.0.0.1'
MILVUS_PORT = '19530'

# Upload info config
BASE_DIR = os.path.dirname(__file__)

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'storage', 'files')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'docx', 'xlxs'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

TOP_K = 3
SEGMENT_LENGTH = 500
OVERLAP = 100

OPENAI_BASE_URL = 'https://api.openai-proxy.com/v1'
OPENAI_API_KEY = 'sk-proj-xxxx'

QWEN_BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
QWEN_API_KEY = 'sk-xxxx'

LOCAL_QWEN_BASE_URL = 'http://22.50.21.17:23342/v1'
LOCAL_QWEN_API_KEY = 'xx'

EMBEDDING_MODEL_NAME = 'text-embedding-3-small'

EMBEDDING_MODELS = {
    'text-embedding-3-small': {
        'base_url': OPENAI_BASE_URL,
        'api_key': OPENAI_API_KEY,
        'model_name': 'text-embedding-3-small',
        'vertor_dim': 1536
    },
}

LLM_MODELS = {
    'gpt-4o-mini': {
        'base_url': OPENAI_BASE_URL,
        'api_key': OPENAI_API_KEY,
        'model_name': 'gpt-4o-mini'
    },
    'qwen-max': {
        'base_url': QWEN_BASE_URL,
        'api_key': QWEN_API_KEY,
        'model_name': 'qwen-max'
    },
    'qwen2-7b': {
        'base_url': LOCAL_QWEN_BASE_URL,
        'api_key': LOCAL_QWEN_API_KEY,
        'model_name': 'qwen'
    }
}