import simpy
import random
import pandas as pd

# 1. Lista vazia para funcionar como nosso banco de dados temporário
dados_simulacao = [] 

def caminhao(env, nome, balanca):
    hora_chegada = env.now
    
    with balanca.request() as pedido:
        yield pedido 
        
        tempo_na_fila = env.now - hora_chegada
        tempo_servico = random.uniform(3, 6)
        
        yield env.timeout(tempo_servico) 
        hora_saida = env.now
        
        # 2. Em vez de apenas dar print, salvamos os dados em um dicionário
        dados_simulacao.append({
            'Veiculo': nome,
            'Momento_Chegada': round(hora_chegada, 2),
            'Tempo_Fila_min': round(tempo_na_fila, 2),
            'Tempo_Atendimento_min': round(tempo_servico, 2),
            'Momento_Saida': round(hora_saida, 2)
        })

def gerador_de_caminhoes(env, balanca, intervalo_medio_chegada):
    i = 0
    while True:
        i += 1
        env.process(caminhao(env, f'Caminhão {i:03d}', balanca))
        tempo_ate_proximo = random.expovariate(1.0 / intervalo_medio_chegada)
        yield env.timeout(tempo_ate_proximo)

# ==========================================
# 3. Executando e Exportando
# ==========================================
print("Rodando simulação...")

env = simpy.Environment()
balanca = simpy.Resource(env, capacity=1) # Capacidade = 1 balança
env.process(gerador_de_caminhoes(env, balanca, intervalo_medio_chegada=4))

# Vamos rodar por mais tempo para gerar mais dados (ex: 8 horas de turno = 480 minutos)
env.run(until=480) 

# 4. Transformando os dados em um DataFrame e exportando para CSV
df_resultados = pd.DataFrame(dados_simulacao)
df_resultados.to_csv('resultado_gargalo_balanca.csv', index=False)

print(f"Simulação concluída! {len(df_resultados)} caminhões processados.")
print("Arquivo 'resultado_gargalo_balanca.csv' gerado com sucesso na sua pasta.")