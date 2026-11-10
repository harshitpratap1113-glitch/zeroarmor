import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="zeroarmor",
    version="2.0.0",
    description="ZeroArmor Titanium: 32-Vector 1-Line Runtime Application Self-Protection (RASP) Shield.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ZeroArmor Cyber Defense Labs",
    author_email="security@zeroarmor.dev",
    url="https://github.com/harshitpratap1113-glitch/zeroarmor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "zeroarmor=zeroarmor.cli:main",
        ],
    },
)
