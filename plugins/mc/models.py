from tortoise import fields
from tortoise.models import Model


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
