from setuptools import setup, find_packages

setup(
    name="ias2",
    version="0.1.0",
    description="Investment Analysis System 2.0",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "numpy",
        "requests",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy",
        ]
    },
    python_requires=">=3.8",
)