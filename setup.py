from setuptools import setup, find_packages

setup(
      name="net-tracker",
      version="0.0.1",
      packages=find_packages(
            include=["nettrackercore", "nettrackercore.*"],
            exclude=["*test*"],
      ),
      install_requires=[],
      entry_points={
            "console_scripts": [
                  "net-tracker=nettrackercore.__main__:main",
            ]
      }
)
