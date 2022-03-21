# getoutlier
ferramenta automática para execução de diversas análises em um arquivo .csv e geração de um arquivo log com os resultados das análises. É uma ferramenta para a exclusão dos outliers da base.
Esta ferramenta mapeia a base de dados e realiza a seleção das colunas quantitativas, assim pode-se optar pela metodologia de idenficação de outliers, estão disponíveis os métodos:
desvio padão;
z-score;
desvio absoluto mediano;
isolation forest;
boxplot;
Cada metodologia está definida em uma função específica, assim é possível usar este código como base para outras aplicações.
Ao final é retornado um novo arquivo .csv Tratado com as linhas que contém outliers excluidas.
