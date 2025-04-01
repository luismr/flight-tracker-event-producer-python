from setuptools import setup, find_packages

setup(
    name="flight-tracker-producer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "quixstreams==0.5.0",
    ],
    extras_require={
        "test": [
            "pytest==8.0.0",
            "pytest-mock==3.12.0",
            "pytest-cov==4.1.0",
        ],
    },
) 