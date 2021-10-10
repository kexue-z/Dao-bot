import time
from pathlib import Path

from .data import get_logger_time, is_logging, remove_logging, start_logging, stop_logging
from .upload import upload_file


def handle_command(**kargs):
    if kargs["message"] == "on":
        if is_logging(kargs["group_id"]):
            return "正在进行日志记录, 无法再次开始!"
        else:
            start_logging(kargs["group_id"], kargs["time"])
            return "开始日志记录"
    elif kargs["message"] == "off":
        if is_logging(kargs["group_id"]):
            stop_logging(kargs["group_id"])
            return "正在上传文件，请稍等"
        else:
            return "没有已开始的日志记录!"
    else:
        return (
            "TRPGLogger 使用说明：\n" ".log on 开始记录\n" ".log off 停止记录\n" "一个群同一时间段不能存在两个记录！"
        )


def handle_logger(**kargs):
    file_path = (
        Path()
        / "data"
        / "trpglogger"
        / f"group_{kargs['group_id']}_{get_logger_time(kargs['group_id'])}.txt"
    )

    if is_logging(kargs["group_id"]):
        with file_path.open("a+", encoding="utf-8") as f:
            f.write(
                f'{kargs["nickname"]}({kargs["user_id"]}) {time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(kargs["time"]))}\n'
            )
            f.write(f'{kargs["message"]}\n\n')
        if kargs["time"] - get_logger_time(kargs["group_id"]) > 60 * 60 * 24:
            stop_logging(kargs["group_id"])
            return "已持续记录24小时，已自动停止记录并上传"
    else:
        if file_path.exists():
            upload_file(str(file_path), "dicelogger", file_path.name)
            file_path.unlink()
            remove_logging(kargs["group_id"])
            return f"上传已完成，请访问 https://logpainter.kokona.tech/?s3={file_path.name} 以查看记录"
        else:
            remove_logging(kargs["group_id"])
