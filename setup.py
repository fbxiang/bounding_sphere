import os
import pathlib

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig
from wheel.bdist_wheel import bdist_wheel


class CustomExtension(Extension):
    def __init__(self, name, sources):
        super().__init__(name, sources=sources)


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_custom(ext)

    def build_custom(self, ext):
        extdir = (
            pathlib.Path(self.get_ext_fullpath(ext.name)).parent.absolute() / ext.name
        )
        extdir.mkdir(parents=True, exist_ok=True)

        self.spawn(
            [
                "g++",
                "-O3",
                "-fPIC",
                "-shared",
                *ext.sources,
                "-o",
                str(extdir / "_C.so"),
            ]
        )


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            return python, "abi3", plat

        return python, abi, plat


setup(
    name="bounding_sphere",
    version="0.1",
    packages=["bounding_sphere"],
    package_dir={"bounding_sphere": "bounding_sphere"},
    ext_modules=[
        CustomExtension(
            "bounding_sphere",
            sources=["src/main.cpp"],
        ),
    ],
    cmdclass={"build_ext": build_ext, "bdist_wheel": bdist_wheel_abi3},
)
