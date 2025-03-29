import os
from flask import request, render_template, redirect, url_for, flash
from extensions.ext_database import db
from sqlalchemy.sql import func
from config import *
from ..models import Dataset, Document, Segment
from .. import bp
from ..form import DatasetForm
from ..milvus_models import DatasetMilvusModel


@bp.route('/', endpoint='dataset_list')
def index():
    # 功能：显示所有知识库列表
    """
    功能：显示所有知识库列表
    执行步骤：
    1. 连接表：使用外连接将Dataset表与Document表连接
    2. 分组：按数据集的ID分组
    3. SELECT和聚合计算
    3. 排序：按数据集的ID降序排列
    4. 获取所有查询结果
    
    当使用 db.session.query() 选择多个列时，SQLAlchemy 默认将每行结果包装为元组。
    元组是不可变的，保证数据安全性
    datasets的外层括号只是为了代码格式化允许跨多行书写 最终是一个包含元组的列表
   """
    datasets =(
        db.session.query(
            Dataset.id,  # 数据集的ID
            Dataset.name,  # 数据集的名称
            Dataset.desc,  # 数据集的描述
            Dataset.created_at,  # 数据集的创建时间
            func.count(Document.id).label("document_count") # 统计每个知识库的文档数量，新属性命名为document_count
        )
        .outerjoin(Document, Dataset.id == Document.dataset_id)# 使用左外连接将Dataset表与Document表合并
        .group_by(Dataset.id)# 按数据集的ID分组，以便计算每个数据集的文档数量 先分组后统计
        .order_by(Dataset.id.desc()) # 按数据集的ID降序排列
        .all()  # 获取所有查询结果 返回列表
    )
    # 渲染dataset_list.html模板，并将查询结果传递给模板
    return render_template('dataset/dataset_list.html', datasets=datasets)


@bp.route('/dataset_create', endpoint='dataset_create', methods=['GET', 'POST'])
def create():
    # 创建一个 DatasetForm 实例，用于处理表单数据
    form = DatasetForm(request.form)
    # 检查请求方法是否为 POST，并且表单数据是否通过验证
    if request.method == 'POST' and form.validate():
        # 从表单中获取名称和描述
        name = request.form.get('name')
        desc = request.form.get('desc')

        # 创建 Dataset 实例并插入数据
        new_dataset = Dataset(name=name, desc=desc)
        db.session.add(new_dataset)
        db.session.commit()

        flash("知识库创建成功!", "success")
        return redirect(url_for("dataset.dataset_list"))
    else:
        if form.errors:
            msg = ' '.join([val for values in form.errors.values() for val in values])
            flash(msg, 'error')

    return render_template('dataset/dataset_create.html', form=form)


@bp.route("/dataset_edit/<int:dataset_id>", methods=["GET", "POST"], endpoint="dataset_edit")
def edit(dataset_id):
    form = DatasetForm(request.form)

    # 查询单条 dataset 数据 创建dataset对象 被 SQLAlchemy 的 Session 跟踪
    dataset = Dataset.query.filter_by(id=dataset_id).first()
    
    if request.method == 'POST' and form.validate():
        name = request.form.get('name')
        desc = request.form.get('desc')

        # commit后  Session检测到对象的变化 生成UPDATE SQL语句
        # 根据对象的 ID 更新数据库记录
        dataset.name = name
        dataset.desc = desc
        db.session.commit()
       
        flash("知识库修改成功!", "success")
        return redirect(url_for("dataset.dataset_list"))
    else:
        if form.errors:
            msg = ' '.join([val for values in form.errors.values() for val in values])
            flash(msg, 'error')
            
    return render_template("dataset/dataset_edit.html", dataset=dataset, form=form)


@bp.route("/dataset_delete/<int:dataset_id>", endpoint="dataset_delete")
def delete(dataset_id):
    try:
        documents = Document.query.filter_by(dataset_id=dataset_id).all()
        # 删除本地文件
        for document in documents:
            file_full_path = os.path.join(UPLOAD_FOLDER, document.file_path)
            if os.path.exists(file_full_path):
                os.remove(file_full_path)
        
        Dataset.query.filter_by(id=dataset_id).delete()
        '''
        如果在数据模型定义时添加了外键关联约束并设置了级联删除（cascade delete）
        就不需要手动写关联数据的删除语句了
        '''
        Document.query.filter_by(dataset_id=dataset_id).delete()
        Segment.query.filter_by(dataset_id=dataset_id).delete()
        
        # 删除 milvus 数据
        delete_expr = f'dataset_id == {dataset_id}'
        DatasetMilvusModel.delete(delete_expr)

        # 提交事务
        db.session.commit()

        flash("知识库删除成功", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"操作失败: {e}", "error")

    return redirect(url_for("dataset.dataset_list"))

