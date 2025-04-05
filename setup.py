import importlib.util
import re
from glob import glob

from setuptools import Extension, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


class LazyCythonize(list):
    def __init__(self, callback):
        self._list, self.callback = None, callback

    def c_list(self):
        if self._list is None:
            self._list = self.callback()
        return self._list

    def __iter__(self):
        for e in self.c_list():
            yield e

    def __getitem__(self, ii):
        return self.c_list()[ii]

    def __len__(self):
        return len(self.c_list())


def extensions():
    from Cython.Build import cythonize

    hpf_module = Extension(
        "thinhpf._hpf",
        [
            "thinhpf/src/_hpf.pyx",
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],
    )
    return cythonize([hpf_module], compiler_directives={"language_level": "3"})


# Create templates.
def fill_templates(file_name, new_file_name, cap_types, label_order, root_order):
    with open(file_name, "r") as fh:
        content = fh.read()

    templates = re.search(
        r"<template>([\s\S]*)</template>", content, re.IGNORECASE
    ).groups()
    filled_templates = []

    for t in templates:
        full_template = []

        for ct in cap_types:
            # Insert CapType.
            t_ct = t.replace("<CapType>", ct)
            for lo in label_order:
                # Insert LabelOrder.
                t_at = t_ct.replace("<LabelOrder>", lo)
                for ro in root_order:
                    # Insert RootOrder.
                    t_nt = t_at.replace("<RootOrder>", ro)
                    # Class name.
                    t_nt = t_nt.replace("<ClassNameExt>", ct + lo + ro)
                    # Save full template.
                    full_template.append(t_nt)

        if full_template:
            filled_templates.append(full_template)

    new_content = content
    for t, ft in zip(templates, filled_templates):
        # Insert filled.
        new_content = new_content.replace(t, "\n".join(ft))

    # Remove template elements.
    new_content = new_content.replace("<template>", "")
    new_content = new_content.replace("</template>\n", "")

    with open(new_file_name, "w") as fh:
        fh.seek(0)
        fh.write(new_content)
        fh.truncate()


# Import types. We can't use normal import during setup, because _hpf isn't compiled yet.
types_spec = importlib.util.spec_from_file_location("thinhpf.types", "thinhpf/types.py")
types = importlib.util.module_from_spec(types_spec)
types_spec.loader.exec_module(types)

cap_types = list(types.capacity_types_lookup.values())
label_order = list(types.label_order_lookup.values())
root_order = list(types.root_order_lookup.values())
for file_name in glob("./thinhpf/**/*.template.pyx", recursive=True):
    fill_templates(
        file_name,
        file_name.replace(".template.pyx", ".pyx"),
        cap_types,
        label_order,
        root_order,
    )

setup(
    name="thinhpf",
    version="0.1.2",
    author="Niels Jeppesen",
    author_email="niejep@dtu.dk",
    description="A thin Python wrapper for the Hochbaum Pseudo Flow (HPF) fast s-t min-cut/max-flow algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Skielex/thinhpf",
    packages=["thinhpf"],
    install_requires=["numpy"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    ext_modules=LazyCythonize(extensions),
    setup_requires=["cython~=3.0.0a9"],
)
