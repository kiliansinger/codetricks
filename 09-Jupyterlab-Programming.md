# Scientific plotting with python: jupyter notebooks

## Installation

Install the [jupyter extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)

We want to use the jupyter notebooks not only with python but also with C++ and C and thus need to stick to python 3.11 for now. Thus open your previously installed miniforge prompt and type

```bash
conda create -n "py311" python=3.11conda activate py311
pip install ipykernel
```
The following lines are only needed if you want to rename the names of the python environment for the jupyter notebook
```
python -m ipykernel install --user --name py311
python -m ipykernel install --user --name py311 --display-name "Python (py311)"
```

if you also want to run jupyter notebooks in the browser then also do:

```bash
pip install jupyter-notebook
jupyter notebook
```

In order to plot with ROOT from cern that uses c++ you can additionally install [ROOT from cern](https://root.cern/install/all_releases/)


edit C:\root_v6.36.04\etc\notebook\kernels\root\kernel.json
change the version in above path and also below according to your recent installation of ROOT.
```json
{
    "language": "python",
    "display_name": "ROOT python",
    "argv": [
       "C:\\Users\\k\\miniforge3\\envs\\py311\\python.exe",
        "-m",
        "ipykernel_launcher",
        "-f",
        "{connection_file}"
        ],
        "env": {
            "PYTHONPATH": "c:\\root_v6.36.04\\bin"
        }
}
```

```bash
pip install metakernel
jupyter kernelspec install c:\root_v6.36.04\etc\notebook\kernels\root
```
