"""Test the plugin with a MkDocs demo site."""
import tempfile
from pathlib import Path

from mkdocs import config
from mkdocs.commands import build


def test_demo(caplog):
    demo_config_file = Path(__file__).parents[1] / "demo" / "mkdocs.yml"
    cfg = config.load_config(config_file=str(demo_config_file.absolute()))
    cfg["plugins"].run_event("startup", command="build", dirty=False)
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg["site_dir"] = tmpdir
        with caplog.at_level("WARNING"):
            build.build(cfg)
        assert (Path(tmpdir) / "index.html").exists()
        assert caplog.text == ""


if __name__ == "__main__":
    test_demo()
