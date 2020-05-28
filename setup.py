import pathlib
from setuptools import setup


CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text(encoding="utf-8")


packages = [
    "d3dshot",
    "d3dshot.dll",
    "d3dshot.capture_outputs",
]


requires = [
    "comtypes>=1.1.5",
    "Pillow>=5.0.0"
]


setup(
    name="D3DShot",
    version="0.1.3",
    description="Extremely Fast and Robust Screen Capture on Windows with the Desktop Duplication API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Nicholas Brochu",
    author_email="nicholas@serpent.ai",
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    license="MIT",
    url="https://github.com/SerpentAI/D3DShot",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
    ]
)
