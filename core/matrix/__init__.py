import importlib.util as _ilu
import sys as _sys
from pathlib import Path as _P


def _load_dotted(alias: str, filename: str) -> None:
    if alias in _sys.modules:
        return
    spec = _ilu.spec_from_file_location(alias, _P(__file__).parent / filename)
    mod = _ilu.module_from_spec(spec)
    _sys.modules[alias] = mod
    spec.loader.exec_module(mod)


_load_dotted("core.matrix.keymaker", "vault_keymaker.secret_manager.py")
_load_dotted("core.matrix.grid_oracle_database", "grid_oracle_database.manager.py")
_load_dotted("core.matrix.kiwi", "kiwi_oracle_morpheme_analyzer.py")
_load_dotted("core.matrix.ollama", "ollama_neo_local_model.py")
