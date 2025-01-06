from setuptools import setup, find_packages

# Read the contents of the README file for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyvo",
    version="0.1.0",
    author="Vincent_JvR",
    author_email="vjjvr.vincent@gmail.com",
    description="Pyvo: A monitoring, logging, performance tracking, and error handling system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/50RC3/pyvo",  # My Github profile
    packages=find_packages(where=".", include=["pyvo", "pyvo.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Monitoring",
    ],
    python_requires='>=3.6',
    install_requires=[
        "tkinter",  # GUI library (may require installation on some systems)
        "matplotlib",  # For plotting and graphing purposes
        "pandas",  # For storing and manipulating data (logs, performance metrics, etc.)
        "pyyaml",  # For handling YAML configuration files
        "requests",  # Useful for any HTTP requests if needed in plugins or scripts
    ],
    extras_require={
        "dev": [
            "pytest",  # For testing
            "tox",  # For managing testing environments
            "sphinx",  # For generating documentation
        ],
        "docs": [
            "sphinx",  # For documentation generation
            "sphinx_rtd_theme",  # For ReadTheDocs theme
        ],
    },
    entry_points={
        "console_scripts": [
            "pyvo-dashboard=pyvo.ui.dashboard:main",  # Defines the entry point for running the dashboard
            "pyvo-healthcheck=pyvo.scripts.health_check:main",  # Example script entry point
        ],
    },
    include_package_data=True,
    package_data={
        "pyvo": [
            "data/*.txt",  # Include non-Python files (e.g., text or configuration files)
            "data/*.csv",  # Include additional data files if any (e.g., CSV)
        ],
    },
    scripts=[
        "pyvo/scripts/health_check.py",  # List of utility scripts included in the installation
        "pyvo/scripts/test_integration.py",
        "pyvo/scripts/collect_system_stats.py",
        "pyvo/scripts/cleanup_pyvo_logs.py",
        "pyvo/scripts/backup_performance.py",
        "pyvo/scripts/monitor_system.py",
        "pyvo/scripts/generate_report.py",
    ],
    zip_safe=False,  # Indicates whether the package can be reliably used when installed as a .egg file
    test_suite="tests",  # Specifies the test suite location
    project_urls={
        "Documentation": "https://yourdocslink.com",
        "Bug Tracker": "https://github.com/50RC3/pyvo/issues",
        "Source Code": "https://github.com/50RC3/pyvo",
    },
    keywords="monitoring logging performance tracking error handling system",  # Helps in search results
)
