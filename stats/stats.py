import os
import matplotlib.pyplot as plt


import pandas as pd
import numpy as np
import scipy.stats as st

from fitter import Fitter

plt.rcParams['axes.titlepad'] = 0

def create_plot_dir(subfolder):
    name = 'plots'
    if not os.path.exists(name):
        os.makedirs(name)

    fullpath = name+'/'+subfolder
    if not os.path.exists(fullpath):
      os.makedirs(fullpath)

    return fullpath + '/'


def gen_stats(path, date,pop_mean, skip=10, take=12):
  plot_dir = create_plot_dir(path)

  xls = pd.ExcelFile('Experimentos/{}-micros-{}.xlsx'.format(path, date))

  sheet_names = xls.sheet_names[1:take+1]

  sample_data = []
  for i in range(len(sheet_names)):
    sheet_name = sheet_names[i]
    sheet = pd.read_excel(xls, sheet_name=sheet_name, header=None)[0][skip:]
    sample_data.append(sheet)
    plt.figure(figsize=(6, 4))
    counts, bins = np.histogram(sheet, bins='auto')
    plt.stairs(counts, bins)
    plt.title(sheet_name)
    plt.xlabel('Interrupções')
    plt.ylabel('Frequência')
    plt.grid(True)
    plt.savefig(plot_dir+sheet_name+'.png')
    plt.close()

  combined_data = np.concatenate(sample_data)

  plt.hist(combined_data, bins='auto', color='blue', alpha=0.5, edgecolor='black')
  plt.xlabel('Interrupções')
  plt.ylabel('Frequência')
  plt.grid(True)
  plt.savefig(plot_dir+'concat.png', bbox_inches="tight")
  plt.show()

  plt.boxplot(sample_data, labels=[item.split()[-1] for item in sheet_names])
  plt.xlabel('Placa Arduino')
  plt.ylabel('Interrupções')
  plt.grid(True)
  plt.savefig(plot_dir+'boxplot.png', bbox_inches="tight")
  plt.show()
  plt.close()


  f = Fitter(combined_data, timeout=60)
  f.fit()


  return sample_data, combined_data, f.summary(), f.fitted_param, st.levene(*sample_data), st.ttest_1samp(combined_data, pop_mean)

skip = 10
exp1, exp1combo, exp1summary, exp1fitted, exp1levene, exp1ttest = gen_stats('Experimento1', '17-06', pop_mean=32768, skip=skip)
exp2, exp2combo, exp2summary, exp2fitted, exp2levene, exp2ttest = gen_stats('Experimento2', '17-06', pop_mean=np.power(10, 6), skip=skip)

data = (exp1combo, )

# Aplicação do bootstrap
res = st.bootstrap(data, np.median, vectorized=False, n_resamples=100000)
print(f"Mediana (95%): {res.standard_error}")
res = st.bootstrap(data, np.average, vectorized=False, n_resamples=100000)
print(f"Média (95%): {res.standard_error}")


# análise das médias sobre a referência dos experimentos

def mediaRef(array, ref):
  result = array.copy()

  for i in range(len(array)):
    result[i] = [round(number/ref, 6) for number in array[i]]

  return result


exp1Ref= mediaRef(exp1, 32768)
exp2Ref = mediaRef(exp2, np.power(10, 6))


x = [x+1 for x in range(len(exp1Ref))]  # Índices do array


plt.scatter(x, [np.average(array) for array in exp1Ref], label='exp1_norm')
plt.scatter(x, [np.average(array) for array in exp2Ref], label='exp2_norm')

# Definindo todos os ticks do eixo x
plt.xticks(range(len(exp1Ref)))

# Adicionando legendas e título
plt.xlabel('Arduino')
plt.ylabel('Média sobre referência')

plt.legend()

# Exibindo o gráfico
plt.show()


expRefMultiply = exp1Ref.copy()

for i in range(len(exp1Ref)):
  expRefMultiply[i] = exp1Ref[i].copy()
  for j in range(len(exp1Ref[i])):
    expRefMultiply[i][j] = round(exp1Ref[i][j] * exp2Ref[i][j],4)

yRefMultiply = [np.average(array) for array in expRefMultiply]
plt.ylim(0.99999,1.00001)
plt.scatter(x, yRefMultiply)
plt.xticks(range(len(exp1Ref)))
plt.xlabel('Arduino')
plt.ylabel('Produto das médias percentuais')
#plt.yscale('log')
plt.show()


