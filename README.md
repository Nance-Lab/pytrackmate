# pytrackmate
Python code to automate running the Trackmate plugin from ImageJ.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About

Performing particle tracking with [Trackmate](https://imagej.net/plugins/trackmate/) requires users to enter many different parameters, which is especially time-consuming if/when one wants to process many different videos with the same parameters. The code in this repository will automate the process of analyzing several `.tif` videos with a set of parameters, ultimately making it easier to test queries about the effect of different combinations of parameters applied in Trackmate on the analysis of the videos. 

## Features


## Demo



## Getting Started


### Prerequisites
- [Python (version 3.8.13)](https://www.python.org/downloads/)
- [Fiji](https://imagej.net/software/fiji)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)


### Installation

```bash
# Clone the repository
git clone https://github.com/Nance-Lab/pytrackmate.git

# Navigate to the project folder
cd pytrackmate

# Install dependencies (create conda environment)
conda env update --name <env name> -f environment.yml
```

## Usage
```bash
# Set up Trackmate
python ~/trackmate_script.py

# Run a single video through automated trackmate tracking
python ~/pytrackmate/trackmate_mpt_script.py

# Run several .tif files with the same parameters by Trackmate
python ~/pytrackmate/trackmate_parallel.py <path to videos> <trackmate function> <trackmate function args> <num threads>
```

## Contributing


## License
```
MIT License

Copyright (c) 2023 Nance Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgements


