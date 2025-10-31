# Belajar Analisis Data Menggunakan Python

## Setup Environment - Anaconda
```
!pip install -q condacolab
import condacolab
condacolab.install()
!conda --version
!conda create --name main-ds python=3.9
!conda activate main-ds
```

## Setup Environment - Shell/Terminal
```
!pip install numpy pandas scipy matplotlib seaborn jupyter
!mkdir proyek_analisis_data
!cd proyek_analisis_data
!jupyter-notebook .
```

## Run steamlit app
```
streamlit run dashboard.py
```
