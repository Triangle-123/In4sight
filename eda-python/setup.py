"""
EDA(Event-Driven Architecture) 패키지
"""

from setuptools import find_packages, setup

setup(
    name="eda-python",
    version="0.1.0",
    description="EDA(Event-Driven Architecture) 패키지",
    author="in4sight",
    packages=find_packages(),
    install_requires=[
        "kafka-python>=2.0.6",
        "pydantic>=2.10.6",
        "python-dotenv>=1.0.1",
    ],
    python_requires=">=3.8",
)
