#!/usr/bin/env python

from setuptools import setup


def main() -> None:
    setup(
        name="update-checker",
        version="0.1",
        description="Check repos for updated versions",
        author="Blake Riley <briley1@gc.cuny.edu>",
        zip_safe=True,
        python_requires=">=3.8,<4.0",
        install_requires=[
            "requests>=2.26,<2.30",
            "PyYAML>=6.0,<7.0",
            "pydantic>=1.8,<2.0",
            "mypy>=0.900,<1.000",
        ],
        dev_requires=[
            "types-requests>=2.26,<2.30",
            "pytest>=6.2,<7.0",
            "jupyterlab>=3.2,<4.0",
            "black>=21.4b0,<22",
            "pycodestyle>=2.8,<3.0",
            "pydocstyle>=6.1,<7.0",
        ],
        entry_points={
            "console_scripts": [
                "update-check = update_checker.update_check:_entrypoint",
            ],
        },
    )


if __name__ == "__main__":
    main()
