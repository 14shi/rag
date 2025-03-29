from celery import shared_task
import os
from apps.dataset.models import Document, Segment
from config import *
from extensions.ext_database import db
from helper import get_llm_embedding
from apps.dataset.milvus_models import DatasetMilvusModel


@shared_task(queue='dataset') #Celery 异步任务
def task(document_id=None, segment_id=None):
    """
    将文本片段转换为向量并存储到 Milvus 向量数据库中
    """
    try:
        # 处理整个文档的所有片段
        if document_id:
            document = Document.query.filter_by(id=document_id).first()
            segments = Segment.query.filter_by(document_id=document_id).all()
            '''
            segments 的类型是 List[Segment]
            每个元素都是 Segment 类的实例
            这些实例是 SQLAlchemy ORM 对象
            '''
            # 删除document_id对应Milvus数据
            #当文档或片段内容被修改时，需要更新对应的向量表示。
            # Milvus 不像关系型数据库那样支持简单的 UPDATE 操作
            # 因此采用"删除再插入"的方式来实现更新：
            #同时如果在更新过程中出现错误（例如，只有部分片段成功处理），milvus有些没有回滚机制
            # 直接添加可能导致数据不完整。
            # 删除再插入可以确保数据库的一致性。
            #确保向量数据库中不会存在重复或过时的数据。
            delete_expr = f'document_id == {document_id}'
            DatasetMilvusModel.delete(delete_expr)

            # 存储片段
            for i, segment in enumerate(segments):
                # 获取句向量并存储
                response = get_llm_embedding(segment.content)
                text_vector = response.data[0].embedding
                DatasetMilvusModel.insert([{
                    'dataset_id': segment.dataset_id,
                    'document_id': segment.document_id,
                    'segment_id': segment.id,
                    'text_vector': text_vector
                }])
                # 修改片段状态
                segment.status = 'completed'

            # 更新文档状态
            document.status = 'completed'
            db.session.commit()
            print('exec dateset_segment_embed_task success.')

        # 插入或更新片段 处理单个文本片段
        if segment_id:
            segment = Segment.query.filter_by(id=segment_id).first()
            # 删除segment_id对应Milvus数据
            delete_expr = f'segment_id == {segment_id}'
            DatasetMilvusModel.delete(delete_expr)
            # 获取句向量并存储
            response = get_llm_embedding(segment.content)
            text_vector = response.data[0].embedding
            DatasetMilvusModel.insert([{
                'dataset_id': segment.dataset_id,
                'document_id': segment.document_id,
                'segment_id': segment.id,
                'text_vector': text_vector
            }])
            # 修改片段状态
            segment.status = 'completed'
            db.session.commit()
            print('exec dateset_segment_embed_task success.')
            
    except Exception as e:
        # db的回滚事务这里只会回滚segment.status  document.status = 'completed'这些操作
        db.session.rollback()
        print(f'exec dateset_segment_embed_task error. {e}')