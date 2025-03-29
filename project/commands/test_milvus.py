import click
from random import random
from pymilvus import connections
from apps.dataset.milvus_models import DatasetMilvusModel

@click.command("test_milvus")
def run():
    # 检查连接状态
    if connections.has_connection("default"):
        print("Successfully connected to Milvus")
    else:
        print("Failed to connect to Milvus")

    # 初始化集合并创建索引
    # DatasetMilvusModel.init_collection()
    # DatasetMilvusModel.create_index()

    # 插入数据
    # data = [
    #     {"dataset_id": 1, "document_id": 1, "segment_id": 1, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 1, "document_id": 1, "segment_id": 2, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 2, "document_id": 2, "segment_id": 1, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 2, "document_id": 2, "segment_id": 2, "text_vector": [random() for i in range(1536)]},
    #     {"dataset_id": 2, "document_id": 2, "segment_id": 3, "text_vector": [random() for i in range(1536)]},
    # ]
    # DatasetMilvusModel.insert(data)

    # # 查询数据
    records = DatasetMilvusModel.query('document_id==3')
    print(records)
    print(len(records))

    # # 查看数据数量
    # print(DatasetMilvusModel.get_entity_count())

    # 删除数据
    # delete_expr = 'segment_id==3'
    # DatasetMilvusModel.delete(delete_expr)

    # 删除集合
    # DatasetMilvusModel.drop_collection()

    # 向量检索
    # query_vec = [random() for i in range(1536)]
    # records = DatasetMilvusModel.search([query_vec], 3)
    # for record in records[0]:
    #     print(record)
