from setuptools import setup

setup(
    name="supervisor-manager",
    version="0.1.0",
    py_modules=["supervisor_manager"],
    install_requires=[
        "click==8.1.7",
        "rich==13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "supervisor-manager=supervisor_manager:cli",
        ],
    },
) 