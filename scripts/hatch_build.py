import sys
from pathlib import Path

try:
    import tomllib as toml
except ImportError:
    try:
        import tomli as toml
    except ImportError:
        # This should only happen if Python < 3.11 and `pipx` is not used.
        print("No suitable TOML library found", file=sys.stderr)
        sys.exit(1)

from hatchling.metadata.plugin.interface import MetadataHookInterface


def dependencies_from_pixi_dependencies(pixi_deps: dict) -> list[str]:
    """Convert run-dependecies dict from a pixi manifest into a pip dependencies list.

    Drops unwanted dependencies and returns a list[str]
    """
    dependencies = []
    for k, v in pixi_deps.items():
        if k == "python":
            # This is not a valid dependency for a pip package
            continue

        dependencies.append(f"{k}{v}")

    return dependencies


class JSONMetaDataHook(MetadataHookInterface):
    """Hatchling build hook to inject pypi package metadata from pixi manifest."""

    def update(self, metadata) -> None:
        """Update method triggered by hatch build."""
        with open(Path(self.root, "pixi.toml"), "rb") as manifest_file:
            manifest = toml.load(manifest_file)
            metadata["version"] = manifest["package"]["version"]
            metadata["name"] = manifest["package"]["name"]
            metadata["license"] = manifest["package"]["license"]
            metadata["authors"] = [{"name": author} for author in manifest["package"]["authors"]]
            metadata["dependencies"] = dependencies_from_pixi_dependencies(manifest["package"]["run-dependencies"])
