from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
    name="leap",
    version="0.1.0",
    author="Sid Abhinav",
    author_email="sidabhinav@gmail.com",
    description="AI-powered educational animation generator",
    url="https://github.com/sid-thephysicskid/leap",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        # Core dependencies
        "fastapi==0.115.11",
        "uvicorn==0.34.0",
        "pydantic==2.10.6",
        "pydantic-settings==2.8.1",
        "pydantic[email]==2.10.6",
        "openai==1.65.2",
        "python-dotenv==0.21.1",
        "manim==0.19.0",
        "manim-voiceover[transcribe]==0.3.7",
        "langsmith==0.3.11",
        "langgraph==0.3.2",
        "instructor==1.7.2",
        "sendgrid==6.11.0",
        "python-json-logger==3.2.1",
        "graphviz==0.20.3",
        "numpy==2.1.3",
        "supabase==2.13.0",
    ],
    extras_require={
        "dev": [
            "pytest==8.3.5",
            "pytest-asyncio==0.25.3",
            "pytest-cov==6.0.0",
            "pytest-mock",
            "pytest-xdist",
            "black==25.1.0",
            "isort",
            "mypy",
            "rich==13.9.4",
            "ipython==9.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "leap=leap.main:main",
            "leap-api=leap.api_server:app",
        ],
    },
    include_package_data=True,
    package_data={
        "leap": ["assets/*", "templates/*", "prompts/*"],
    },
)