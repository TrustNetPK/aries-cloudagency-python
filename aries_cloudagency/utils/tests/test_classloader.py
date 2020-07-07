from unittest import TestCase, mock

from ...core.error import BaseError

from .. import classloader as test_module
from ..classloader import ClassLoader, ClassNotFoundError, ModuleLoadError


class TestClassLoader(TestCase):
    def test_import_loaded(self):
        assert ClassLoader.load_module("unittest")

    def test_import_local(self):
        with mock.patch.object(test_module.sys, "modules", {}):
            assert (
                ClassLoader.load_module("aries_cloudagency.transport").__name__
                == "aries_cloudagency.transport"
            )

    def test_import_relative(self):
        with mock.patch.object(test_module.sys, "modules", {}):
            assert (
                ClassLoader.load_module("transport", "aries_cloudagency").__name__
                == "aries_cloudagency.transport"
            )
        with mock.patch.object(test_module.sys, "modules", {}):
            assert (
                ClassLoader.load_module(".transport", "aries_cloudagency").__name__
                == "aries_cloudagency.transport"
            )
        with mock.patch.object(test_module.sys, "modules", {}):
            assert (
                ClassLoader.load_module(
                    "..transport", "aries_cloudagency.config"
                ).__name__
                == "aries_cloudagency.transport"
            )

    def test_import_missing(self):
        with mock.patch.object(test_module.sys, "modules", {}):
            assert ClassLoader.load_module("aries_cloudagency.not") is None
        with mock.patch.object(test_module.sys, "modules", {}):
            assert ClassLoader.load_module("aries_cloudagency.not.a-module") is None
        with mock.patch.object(test_module.sys, "modules", {}):
            assert ClassLoader.load_module("aries_cloudagency", "not.a-module") is None

    def test_import_error(self):
        with mock.patch.object(
            test_module, "import_module", autospec=True
        ) as import_module, mock.patch.object(test_module.sys, "modules", {}):
            import_module.side_effect = ModuleNotFoundError
            with self.assertRaises(ModuleLoadError):
                ClassLoader.load_module("aries_cloudagency.config")

    def test_load_class(self):
        assert ClassLoader.load_class("TestCase", "unittest") is TestCase
        assert ClassLoader.load_class("unittest.TestCase") is TestCase

    def test_load_class_missing(self):
        with self.assertRaises(ClassNotFoundError):
            # with no default module
            assert ClassLoader.load_class("NotAClass")
        with self.assertRaises(ClassNotFoundError):
            assert ClassLoader.load_class("aries_cloudagency.NotAClass")
        with self.assertRaises(ClassNotFoundError):
            assert ClassLoader.load_class("not-a-module.NotAClass")
        with self.assertRaises(ClassNotFoundError):
            # should be a string, not a type
            assert ClassLoader.load_class("aries_cloudagency.version.__version__")

    def test_load_subclass(self):
        assert ClassLoader.load_subclass_of(BaseError, "aries_cloudagency.config.base")

    def test_load_subclass_missing(self):
        with self.assertRaises(ClassNotFoundError):
            assert ClassLoader.load_subclass_of(
                TestCase, "aries_cloudagency.config.base"
            )
        with self.assertRaises(ClassNotFoundError):
            assert ClassLoader.load_subclass_of(
                TestCase, "aries_cloudagency.not-a-module"
            )

    def test_scan_packages(self):
        pkgs = ClassLoader.scan_subpackages("aries_cloudagency")
        assert "aries_cloudagency.transport" in pkgs
        pkgs = ClassLoader.scan_subpackages("aries_cloudagency.transport")
        assert "aries_cloudagency.transport.inbound" in pkgs

    def test_scan_packages_missing(self):
        with self.assertRaises(ModuleLoadError):
            ClassLoader.scan_subpackages("aries_cloudagency.not-a-module")
