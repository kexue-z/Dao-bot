"""Custom loader."""

from __future__ import annotations

import os
from io import StringIO, TextIOWrapper
from pathlib import Path
from typing import Any, TextIO
from nonebot.log import logger
import yaml


try:
    from yaml import CSafeLoader as FastestAvailableSafeLoader

    HAS_C_LOADER = True
except ImportError:
    HAS_C_LOADER = False
    from yaml import SafeLoader as FastestAvailableSafeLoader

from propcache import cached_property

from .const import SECRET_YAML

JSON_TYPE = dict | list | str


class YamlTypeError(Exception):
    """Raised by load_yaml_dict if top level data is not a dict."""


class Secrets:
    """Store secrets while loading YAML."""

    def __init__(self, config_dir: Path) -> None:
        """Initialize secrets."""
        self.config_dir = config_dir
        self._cache: dict[Path, dict[str, str]] = {}

    def get(self, requester_path: str, secret: str) -> str:
        """Return the value of a secret."""
        current_path = Path(requester_path)

        secret_dir = current_path
        while True:
            secret_dir = secret_dir.parent

            try:
                secret_dir.relative_to(self.config_dir)
            except ValueError:
                # We went above the config dir
                break

            secrets = self._load_secret_yaml(secret_dir)

            if secret in secrets:
                logger.debug(
                    "Secret %s retrieved from secrets.yaml in folder %s",
                    secret,
                    secret_dir,
                )
                return secrets[secret]

        raise Exception(f"Secret {secret} not defined")

    def _load_secret_yaml(self, secret_dir: Path) -> dict[str, str]:
        """Load the secrets yaml from path."""
        if (secret_path := secret_dir / SECRET_YAML) in self._cache:
            return self._cache[secret_path]

        logger.debug("Loading", secret_path)

        try:
            secrets = load_yaml(str(secret_path))

            if not isinstance(secrets, dict):
                raise Exception("Secrets is not a dictionary")

        except FileNotFoundError:
            secrets = {}

        self._cache[secret_path] = secrets

        return secrets


class _LoaderMixin:
    """Mixin class with extensions for YAML loader."""

    name: str
    stream: Any

    @cached_property
    def get_name(self) -> str:
        """Get the name of the loader."""
        return self.name

    @cached_property
    def get_stream_name(self) -> str:
        """Get the name of the stream."""
        return getattr(self.stream, "name", "")


class FastSafeLoader(FastestAvailableSafeLoader, _LoaderMixin):
    """The fastest available safe loader, either C or Python."""

    def __init__(self, stream: Any, secrets: Secrets | None = None) -> None:
        """Initialize a safe line loader."""
        self.stream = stream

        # Set name in same way as the Python loader does in yaml.reader.__init__
        if isinstance(stream, str):
            self.name = "<unicode string>"
        elif isinstance(stream, bytes):
            self.name = "<byte string>"
        else:
            self.name = getattr(stream, "name", "<file>")

        super().__init__(stream)
        self.secrets = secrets


class PythonSafeLoader(yaml.SafeLoader, _LoaderMixin):
    """Python safe loader."""

    def __init__(self, stream: Any, secrets: Secrets | None = None) -> None:
        """Initialize a safe line loader."""
        super().__init__(stream)
        self.secrets = secrets


type LoaderType = FastSafeLoader | PythonSafeLoader


def load_yaml(fname: str | os.PathLike[str], secrets: Secrets | None = None) -> dict:
    """Load a YAML file.

    If opening the file raises an OSError it will be wrapped in a Exception,
    except for FileNotFoundError which will be re-raised.
    """

    with open(fname, encoding="utf-8") as conf_file:
        return parse_yaml(conf_file, secrets)


def load_yaml_dict(
    fname: str | os.PathLike[str], secrets: Secrets | None = None
) -> JSON_TYPE:
    """Load a YAML file and ensure the top level is a dict.

    Raise if the top level is not a dict.
    Return an empty dict if the file is empty.
    """
    loaded_yaml = load_yaml(fname, secrets)
    if loaded_yaml is None:
        loaded_yaml = {}
    if not isinstance(loaded_yaml, dict):
        raise YamlTypeError(f"YAML file {fname} does not contain a dict")
    return loaded_yaml


def parse_yaml(
    content: str | TextIO | StringIO, secrets: Secrets | None = None
) -> JSON_TYPE:
    """Parse YAML with the fastest available loader."""
    if not HAS_C_LOADER:
        return _parse_yaml_python(content, secrets)
    try:
        return _parse_yaml(FastSafeLoader, content, secrets)
    except yaml.YAMLError:
        # Loading failed, so we now load with the Python loader which has more
        # readable exceptions
        if isinstance(content, (StringIO, TextIO, TextIOWrapper)):
            # Rewind the stream so we can try again
            content.seek(0, 0)
        return _parse_yaml_python(content, secrets)


def _parse_yaml_python(
    content: str | TextIO | StringIO, secrets: Secrets | None = None
) -> dict:
    """Parse YAML with the python loader (this is very slow)."""
    try:
        return _parse_yaml(PythonSafeLoader, content, secrets)
    except yaml.YAMLError as exc:
        logger.error(str(exc))
        raise Exception(exc) from exc


def _parse_yaml(
    loader: type[FastSafeLoader | PythonSafeLoader],
    content: str | TextIO,
    secrets: Secrets | None = None,
) -> JSON_TYPE:
    """Load a YAML file."""
    return yaml.load(content, Loader=lambda stream: loader(stream, secrets))  # type: ignore[arg-type]


def secret_yaml(loader: LoaderType, node: yaml.nodes.Node) -> JSON_TYPE:
    """Load secrets and embed it into the configuration YAML."""
    if loader.secrets is None:
        raise Exception("Secrets not supported in this YAML file")

    return loader.secrets.get(loader.get_name, node.value)


def add_constructor(tag: Any, constructor: Any) -> None:
    """Add to constructor to all loaders."""
    for yaml_loader in (FastSafeLoader, PythonSafeLoader):
        yaml_loader.add_constructor(tag, constructor)


add_constructor("!secret", secret_yaml)
