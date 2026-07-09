from importlib import util
from pathlib import Path

_module_path = Path(__file__).resolve().parent.parent / "dashboard_page.py"
_spec = util.spec_from_file_location("pages._dashboard_page_module", _module_path)
_module = util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_module)

DashboardPage = _module.DashboardPage

__all__ = ["DashboardPage"]
