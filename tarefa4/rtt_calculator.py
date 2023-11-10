from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Faz o parse do txt de cada algoritmo (coluna do meio a ser considerada)
def read_samples_from_file(file_path: str) -> List[float]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    samples = [line.split()[1] for line in lines] # pega coluna do meio (0 -> "1" <- 2)
    samples = [float(value.replace(',', '.')) for value in samples]
    return samples


# Vamos utilizar como sampleRTT inicial a média dos 3 valores calculados
def calculate_sampleRTT(samples: List[float]) -> float:
    return np.mean(samples)


# Inicializa variáveis com as fornecidas na questão
def initialize_variables(sampleRTT: float) -> Tuple[float, float, float, float, float]:

    DevRTT = 0.05 * sampleRTT # nosso devRTT inicial será 5% do nosso sampleRTT
    
    alfa = 0.125
    beta = 0.25
    EstimatedRTT = sampleRTT
    TimeoutInterval = EstimatedRTT + 4 * DevRTT
    return DevRTT, alfa, beta, EstimatedRTT, TimeoutInterval


# Faz o calculo de cada variavel com as 30 amostras
def calculate_metrics(samples: List[float], DevRTT: float, alfa: float, beta: float, EstimatedRTT: float, TimeoutInterval: float) -> Tuple[List[float], List[float], List[float]]:
    estimated_list = []
    dev_list = []
    timeouts = []
    for sample in samples:
        SampleRTT = sample
        EstimatedRTT = (1 - alfa) * EstimatedRTT + alfa * SampleRTT
        DevRTT = (1 - beta) * DevRTT + beta * abs(SampleRTT - EstimatedRTT)
        TimeoutInterval = EstimatedRTT + 4 * DevRTT
        estimated_list.append(EstimatedRTT)
        dev_list.append(DevRTT)
        timeouts.append(TimeoutInterval)
    return estimated_list, dev_list, timeouts


# Faz o plot em linha das variaveis ao longo das samples
def plot_metrics(algoName: str, x_values: List[int], samples: List[float], estimated_list: List[float], dev_list: List[float], timeouts: List[float]) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, samples, label='SampleRTT')
    plt.plot(x_values, estimated_list, label='EstimatedRTT')
    plt.plot(x_values, dev_list, label='DevRTT')
    plt.plot(x_values, timeouts, label='TimeoutInterval')
    plt.xlabel('N de Amostras')
    plt.ylabel('Valores de EstimatedRTT, DevRTT, TimeoutInterval, SampleRTT')
    plt.title(f'Algoritmo: {algoName.capitalize()}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{algoName}_plot.png')
    plt.show()


# Faz o tratamento dos dados para o boxplot do seaborn 
def prepare_data_for_boxplot(samples: List[float], estimated_list: List[float], dev_list: List[float], timeouts: List[float]) -> pd.DataFrame:
    data = pd.DataFrame({
        'SampleRTT': samples,
        'EstimatedRTT': estimated_list,
        'DevRTT': dev_list,
        'TimeoutInterval': timeouts
    })
    data = pd.melt(data)
    return data


# Gera o boxplot das variaveis usando seaborn 
def generate_boxplot(data: pd.DataFrame, algoName: str) -> None:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='variable', y='value', data=data, showfliers=False, width=0.4, boxprops=dict(alpha=0.5))
    sns.swarmplot(x='variable', y='value', data=data, color='black', alpha=0.8)
    plt.xlabel('Variaveis')
    plt.ylabel('Valores (ms)')
    plt.title(f'Algoritmo: {algoName.capitalize()}')
    plt.grid(True)
    plt.savefig(f'{algoName}_boxplot.png')
    plt.show()


def main(): 
    FILE_PATH = 'plista.txt'
    algoName = FILE_PATH.split('.')[0]

    samples = read_samples_from_file(FILE_PATH)
    sampleRTT = calculate_sampleRTT(samples)
    DevRTT, alfa, beta, EstimatedRTT, TimeoutInterval = initialize_variables(sampleRTT)
    
    estimated_list, dev_list, timeouts = calculate_metrics(samples, DevRTT, alfa, beta, EstimatedRTT, TimeoutInterval)
    
    x_values = list(range(1, len(samples) + 1))
    
    #plot_metrics(algoName, x_values, values, estimated_list, dev_list, timeouts)
    
    data_for_boxplot = prepare_data_for_boxplot(samples, estimated_list, dev_list, timeouts)
    generate_boxplot(data_for_boxplot, algoName)

if __name__ == '__main__':
    main()


