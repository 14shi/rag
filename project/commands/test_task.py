import click
from tasks.demo_task import task as demo_task
from tasks.dateset_segment_embed_task import task as dateset_segment_embed_task


@click.command("test_task")
def run():
    # # 调用立即执行
    # demo_task.delay('exec now')

    # # 调用后延迟10秒再执行
    # demo_task.apply_async(
    #     kwargs = {'msg': 'exec async'},
    #     countdown = 10
    # )

    # dateset_segment_embed_task.delay(5)
    dateset_segment_embed_task.delay(None, 23)
    
    click.echo("success.")