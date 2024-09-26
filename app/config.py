import os

CURRENT_PATH = os.getcwd()
PASTA_BINARIOS = os.path.join(CURRENT_PATH, "bin")
PASTA_OUTPUT = os.path.join(CURRENT_PATH, "output")

PASTA_OUTPUT_BINARIOS = os.path.join(PASTA_OUTPUT, "bins")
PASTA_OUTPUT_PLOTS = os.path.join(PASTA_OUTPUT, "plots")


os.makedirs(PASTA_BINARIOS, exist_ok=True)
os.makedirs(PASTA_OUTPUT, exist_ok=True)
os.makedirs(PASTA_OUTPUT_BINARIOS, exist_ok=True)
os.makedirs(PASTA_OUTPUT_PLOTS, exist_ok=True)
