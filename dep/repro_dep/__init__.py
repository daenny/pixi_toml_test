"""Marker module: reports which branch of the repo this package was built from."""

# Changed on every branch, so the installed value tells you which git ref pixi used.
BRANCH = "feature/dep-v4"
VERSION = "4.0.0"


def main() -> None:
    print(f"repro_dep {VERSION} built from branch {BRANCH!r}")
