from uuid import uuid4
from typing import List
from datetime import datetime, timedelta

from dateutil import tz
from tortoise import fields
from tortoise.models import Model
from tortoise.expressions import Q


class MCTrustIDs(Model):
    user_id = fields.IntField(pk=True, unique=True)
    """用户ID"""
    enabled = fields.BooleanField(default=False)
    """是否启用"""

    class Meta:
        table = "mc_trust_ids"

    @staticmethod
    async def add_id(user_id: int, enabled=True) -> bool:
        _, status = await MCTrustIDs.get_or_create(user_id=user_id, enabled=enabled)
        if status:
            return True
        return False

    @staticmethod
    async def remove_id(user_id: int) -> bool:
        res = await MCTrustIDs.get(user_id=user_id)
        await res.delete()
        return True

    @staticmethod
    async def get_all_enabled_ids() -> list[int]:
        res = await MCTrustIDs.filter(enabled=True).all()
        ids: list[int] = []
        for i in res:
            ids.append(i.user_id)
        return ids


class MCServers(Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=255, unique=True)
    instance_uuid = fields.CharField(max_length=32)
    remote_uuid = fields.CharField(max_length=32)
    ip = fields.CharField(max_length=512)

    class Meta:
        table = "mc_servers"

    @staticmethod
    async def add_server(
        name: str, instance_uuid: str, remote_uuid: str, ip: str
    ) -> bool:
        _, status = await MCServers.get_or_create(
            name=name,
            instance_uuid=instance_uuid,
            remote_uuid=remote_uuid,
            ip=ip,
        )
        if status:
            return True
        return False

    @staticmethod
    async def get_all_servers_ip() -> list[list[str]]:
        """
        :说明: `get_all_servers_ip`
        > 获取服务器的IP，提供ping使用
        """
        servers: list[list[str]] = []
        res = await MCServers.filter().all()
        for i in res:
            servers.append([i.name, i.ip])

        return servers

    @staticmethod
    async def get_server_data(server_name: str) -> dict[str, str]:
        res = await MCServers.get(name=server_name)
        return {
            "remote_uuid": res.remote_uuid,
            "instance_uuid": res.instance_uuid,
        }

    @staticmethod
    async def delete_server(server_name: str) -> bool:
        res = await MCServers.get(name=server_name)
        await res.delete()
        return True

    @staticmethod
    async def get_server_name_by_uuid(instance_uuid: str) -> str:

        res = await MCServers.get_or_none(instance_uuid=instance_uuid)
        if res:
            return res.name
        return "**已删除**"


class ServerCommandHistory(Model):
    id = fields.IntField(pk=True, unique=True, generated=True)
    time = fields.DatetimeField(auto_now_add=True)
    user_id = fields.IntField()
    command = fields.TextField()
    target_instance_uuid = fields.CharField(max_length=32)
    target_remote_uuid = fields.CharField(max_length=32)
    is_success = fields.BooleanField(default=False)

    class Meta:
        table = "server_command_history"

    @staticmethod
    async def add_command_record(
        user_id: int,
        command: str,
        target_instance_uuid: str,
        target_remote_uuid: str,
        is_success: bool,
    ) -> bool:
        res = await ServerCommandHistory.create(
            user_id=user_id,
            command=command,
            target_instance_uuid=target_instance_uuid,
            target_remote_uuid=target_remote_uuid,
            is_success=is_success,
        )

        if res:
            return True
        return False

    @staticmethod
    async def get_recent_history(
        time_start: datetime = datetime.now(tz=tz.tzlocal()) - timedelta(days=1),
        time_end: datetime = datetime.now(
            tz=tz.tzlocal(),
        ),
        user_id: int | None = None,
    ) -> List["ServerCommandHistory"]:
        if user_id:
            return (
                await ServerCommandHistory.filter(user_id=user_id).order_by("-id").all().limit(10)
            )
        return await ServerCommandHistory.all().order_by('-id').limit(10)
