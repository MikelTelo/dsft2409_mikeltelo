from setuptools import setup, find_packages

setup(
    name="datautilityhub",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Una biblioteca de utilidades para análisis de datos y machine learning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/DataUtilityHub",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=0.24.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "category-encoders>=2.3.0",
        "plotly>=5.3.0",
        "ipywidgets>=7.6.0",
        "scipy>=1.7.0",
        "statsmodels>=0.13.0",
        "xgboost>=1.5.0",
        "lightgbm>=3.3.0",
        "optuna>=2.10.0",
        "python-dateutil>=2.8.2",
    ],
) 