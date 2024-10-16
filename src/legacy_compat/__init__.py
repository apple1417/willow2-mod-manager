from mods_base.mod_list import base_mod

__all__: tuple[str, ...] = (
    "__author__",
    "__version__",
    "__version_info__",
    "legacy_compat",
)

__version_info__: tuple[int, int] = (1, 0)
__version__: str = f"{__version_info__[0]}.{__version_info__[1]}"
__author__: str = "bl-sdk"

# Kill switch. May have to update this at some point if we decide to keep this around longer.
if base_mod.version.partition(" ")[0] not in {"3.0", "3.1", "3.2", "3.3", "3.4"}:
    import warnings
    from collections.abc import Iterator
    from contextlib import contextmanager

    from unrealsdk import logging

    logging.warning("Legacy SDK Compatibility has been disabled")

    @contextmanager
    def legacy_compat() -> Iterator[None]:
        """Context manager which enables legacy SDK import compatibility while active."""
        warnings.warn(
            "Legacy import compatibility has been removed.",
            DeprecationWarning,
            stacklevel=3,
        )
        yield
        return
else:
    import ctypes
    import inspect
    import sys
    import warnings
    from collections.abc import Iterator, Sequence
    from contextlib import contextmanager
    from importlib.machinery import ModuleSpec
    from importlib.util import spec_from_file_location
    from pathlib import Path
    from types import ModuleType

    from . import ModMenu
    from . import unrealsdk as old_unrealsdk

    base_mod.components.append(base_mod.ComponentInfo("Legacy SDK Compat", __version__))

    """
    There are two parts to legacy SDK compatibility.

    The first is creating aliases and proxy objects for absolutely everything. While extensive, this
    is relatively simple. This is handled by the two `unrealsdk` and `ModMenu` submodules.

    The second more difficult part is dealing with imports. In the legacy SDK, ill advisedly, the
    `Mods` folder was part of the packaging, `mods/xyz` was packaged under `Mods.xyz`. This is no
    longer the case in this version, it's just under a top level `xyz`. We can't trust users to
    extract legacy mods any differently to updated ones, so we need to redirect these imports
     automatically.
    """

    # First, create a fake mods module
    Mods = ModuleType("Mods")

    """
    To allow importing submodules at all, to convert the module into a package, we need to set
     __path__. But to what? This requires a bit of reading between the lines.

    > The find_spec() method of meta path finders is called with two or three arguments. The first
    > is the fully qualified name of the module being imported, for example foo.bar.baz. The second
    > argument is the path entries to use for the module search. For top-level modules, the second
    > argument is None, but for submodules or subpackages, the second argument is the value of the
    > parent package's __path__ attribute.

    When importing a submodule, it copies the value of the parent's __path__. When importing a top
    level module, it uses None. We want importing a submodule of Mods to actually import a top level
    module - so we set it directly to None, to trick the import system into doing this for us.
    """
    Mods.__path__ = None  # type:  ignore

    # This is needed for some mods
    Mods.__file__ = str(Path(__file__).parent.parent)

    # This is essentially an extra version of sys.modules which we swap during legacy compat
    # When we exit compat, we'll move any new imports under `Mods` into this, since we don't want to
    # keep them around for normal mods
    legacy_modules: dict[str, ModuleType] = {
        "bl2sdk": old_unrealsdk,
        "unrealsdk": old_unrealsdk,
        "Mods": Mods,
        "Mods.ModManager": ModMenu.ModObjects,
        "Mods.ModMenu": ModMenu,
        "Mods.OptionManager": ModMenu.OptionManager,
        # Mod-specific compat
        # This normally points at an older version, we can point it at the current
        "Mods.UserFeedback.ctypes": ctypes,
    }

    # On top of this, we do actually need a full import hook to redirect other mod-specific imports

    class LegacyCompatMetaPathFinder:
        @staticmethod
        def get_importing_file() -> Path:
            """
            Gets the file which triggered the in progress import.

            Returns:
                The importing file.
            """
            # Skip the frame for this function and find_spec below
            for frame in inspect.stack()[2:]:
                # Then skip everything in the import machinery
                if "importlib" in frame.filename:
                    continue
                return Path(frame.filename)
            raise RuntimeError

        @classmethod
        def find_spec(
            cls,
            fullname: str,
            path: Sequence[str] | None = None,  # noqa: ARG003
            target: ModuleType | None = None,  # noqa: ARG003
        ) -> ModuleSpec | None:
            # EridiumLib adds it's dist folder with a path relative to the executable - fix that
            # We also have some problems with it's copy of requests, so redirect that to our copy
            if fullname == "requests" and cls.get_importing_file().parent.name == "EridiumLib":
                return spec_from_file_location(
                    "Mods.EridiumLib.fake_dist.requests",
                    Path(__file__).parent / "eridiumlib_requests.py",
                )
            if (
                fullname == "semver"
                and (mod_folder := cls.get_importing_file().parent).name == "EridiumLib"
            ):
                return spec_from_file_location(
                    "Mods.EridiumLib.fake_dist.semver",
                    mod_folder / "dist" / "semver.py",
                )

            return None

    @contextmanager
    def legacy_compat() -> Iterator[None]:
        """Context manager which enables legacy SDK import compatibility while active."""
        warnings.warn(
            "Using deprecated legacy import compatibility.",
            DeprecationWarning,
            stacklevel=3,
        )

        # Backup any current modules with the same name as a legacy one
        overwritten_modules = {
            name: mod for name, mod in sys.modules.items() if name in legacy_modules
        }
        # Overwrite with legacy modules
        sys.modules |= legacy_modules

        # And add our import hook
        sys.meta_path.insert(0, LegacyCompatMetaPathFinder)

        try:
            yield
        finally:
            # Remove the import hook
            sys.meta_path.remove(LegacyCompatMetaPathFinder)

            # Move the legacy modules out of sys.modules back into our legacy dict
            for name in tuple(sys.modules.keys()):
                if name in legacy_modules or name.startswith("Mods."):
                    legacy_modules[name] = sys.modules.pop(name)
            # And add any overwritten modules back in
            sys.modules |= overwritten_modules
