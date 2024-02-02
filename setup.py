import pathlib

from setuptools import find_namespace_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="Protectimus Platform Automation Test Framework",
    version="0.0.0",
    license="",
    author="fluxofdelight",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fluxofdelight/protectimus_platform_python_fw",
    package_dir={"": "src"},
    py_modules=[],
    packages=find_namespace_packages(where="src"),
    python_requires=">=3.11, <4",
    install_requires=[
        "pytest==7.4.0",
        "selenium==4.12.0",
        "pre-commit==3.4.0",
        "pytest-html==3.2.0",
        "attrs==23.1.0",
        "psycopg==3.1.10",
        "loguru==0.7.1",
        "selene==2.0.0rc4",
        "allure-pytest==2.13.2",
        "PyYAML==6.0.1",
        "requests==2.31.0",
        "pyotp==2.9.0",
    ],
    extras_require={},
    package_data={},
)
