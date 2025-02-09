from setuptools import setup, find_packages

setup(
    name="chatbot",
    version="1.0.0",
    description="A ChatGPT-powered desktop chatbot application",
    author="Code25356",
    packages=find_packages(),
    install_requires=[
        'openai>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'chatbot=chatbot.main:main',
        ],
    },
    python_requires='>=3.8',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)