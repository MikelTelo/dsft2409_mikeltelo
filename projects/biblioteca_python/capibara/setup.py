from setuptools import setup, find_packages

setup(
    name='capibara',
    version='0.1.0',
    description='A comprehensive Python library for data science and machine learning',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'plotly>=5.1.0',
        'xgboost>=1.5.0',
        'scipy>=1.7.0',
    ],
    python_requires='>=3.9.6,<3.10',
)