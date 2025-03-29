from pymilvus import connections, Collection, utility
from pymilvus.client.types import LoadState

def init_app(app):
    try:
        connections.connect(
            alias="default",
            host=app.config['MILVUS_HOST'],
            port=app.config['MILVUS_PORT']
        )
    except Exception as e:
        print(f"An error occurred while connecting to Milvus: {e}")

class MilvusBaseModel:
    collection_name = None #Collection集合是实际的数据存储实体 即表 提供直接操作的接口
    schema = None #Schema：定义了集合的结构，包括字段名称、数据类型、主键等
    index_params = None #IndexParams：定义了索引的参数，包括索引类型、索引维度等
    index_field_name = None #IndexFieldName：定义了索引的字段名称

    @classmethod
    def init_collection(cls):
        # 初始化集合
        if cls.collection_name is None or cls.schema is None:
            
            raise ValueError("collection_name and schema must be defined in the subclass")
       
        # collections 是一个字符串列表，包含了 Milvus 数据库中所有已创建的集合名称。
        collections = utility.list_collections()
        # 判断当前类的collection_name是否在集合列表中
        if cls.collection_name not in collections:
            # Collection实例对象有两种创建方式：
            # 创建新集合或连接现有集合
            # 创建一个新的集合 这里需要schema
            #添加类属性collection=新集合
            cls.collection = Collection(name=cls.collection_name, schema=cls.schema)
            print(f"Collection '{cls.collection_name}' created.")
        else:
            # 如果集合已存在，直接实例化该集合 
            # 类属性是共享的 此时是一个实例对象
            cls.collection = Collection(name=cls.collection_name)
            print(f"Collection '{cls.collection_name}' already exists.")

    @classmethod
    def load_collection(cls):
        collection = Collection(name=cls.collection_name)
        # 检查集合的加载状态
        if utility.load_state(cls.collection_name) == LoadState.NotLoad:
            collection.load()#将集合数据从磁盘加载到内存中以提高查询性能
        return collection

    @classmethod
    def drop_collection(cls):
        collections = utility.list_collections()
        if cls.collection_name in collections:
            utility.drop_collection(cls.collection_name)
            print(f"Collection '{cls.collection_name}' has been deleted.")
        else:
            print(f"Collection '{cls.collection_name}' does not exist.")

    @classmethod
    def create_index(cls):
        collection = Collection(name=cls.collection_name)
        if cls.index_field_name is None:
            return None
        if not collection.has_index(index_name=cls.index_field_name):
            if cls.index_params is None:
                raise ValueError("index_params must be defined in the subclass")
            print(cls.index_field_name, cls.index_params)
            collection.create_index(field_name=cls.index_field_name, index_params=cls.index_params)
            print(f"Index created for collection '{cls.collection_name}'.")

    @classmethod
    def get_entity_count(cls):
        collection = cls.load_collection()
        # 获取集合中的实体数量
        entity_count = collection.num_entities
        return entity_count

    @classmethod
    def insert(cls, data):
        collection = cls.load_collection()
        collection.insert(data)

    @classmethod
    def query(cls, expr, output_fields=None):
        collection = cls.load_collection()
        if not output_fields:
            schema = collection.schema
            output_fields = [field.name for field in schema.fields]
       
        results = collection.query(expr=expr, output_fields=output_fields)
        return results

    @classmethod
    def delete(cls, expr):
        collection = cls.load_collection()
        collection.delete(expr)

    @classmethod
    def search(cls, query_vectors, top_k, expr=None, output_fields=None):
        collection = cls.load_collection()
        # 搜索数据
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        if not output_fields:
            # 动态获取所有字段
            schema = collection.schema
            output_fields = [field.name for field in schema.fields]
        results = collection.search(query_vectors, cls.index_field_name, search_params, top_k, expr=expr, output_fields=output_fields)
        return results
