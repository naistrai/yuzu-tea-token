from setuptools import setup, find_packages

setup(
    name="yuzu-tea-token",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "web3>=5.0.0",
        "requests>=2.0.0",
    ],
    author="Naistrai",
    author_email="rizkynaistrai@gmail.com",
    description="Python package to interact with Yuzu Tea Token (YZTEA) on Tea Sepolia",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/naistrai/yuzu-tea-token",
    download_url="https://github.com/naistrai/yuzu-tea-token/archive/refs/heads/main.zip",
    keywords = ['sepolia', 'token', 'bot', 'transfer', 'batch'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)