# Relatório – Passo 5: Inferência Visual de Notas

## Objetivo do Passo 5

O Passo 5 tem como objetivo **inferir notas musicais a partir da informação visual**, utilizando exclusivamente:

- a geometria estabilizada da escala (cordas e trastes)
- a detecção da mão como oclusor
- o mapa de pressão corda × traste

Neste estágio, **nenhuma informação de áudio é utilizada**. A meta é produzir uma hipótese visual consistente das notas tocadas em cada frame, que será posteriormente validada e refinada no Passo 6 por meio da fusão áudio–visão.

---

## Entradas do Passo 5

O Passo 5 consome dados produzidos por etapas anteriores do pipeline:

1. **Imagem retificada da escala**
   - Proveniente do Passo 2 (retificação geométrica)
   - Perspectiva estabilizada e consistente entre frames

2. **Grid estabilizado da escala**
   - Lista ordenada de trastes (coordenadas x)
   - Lista ordenada de cordas (coordenadas y)
   - Identidade temporal fixa via `FretboardGridTracker`

3. **Máscara binária da mão (`hand_mask`)**
   - Resultado do Passo 4
   - Representa regiões ocluídas pela mão/dedos

---

## Ferramentas e Bibliotecas Utilizadas

- **NumPy**
  - Operações matriciais
  - Construção e análise do mapa de pressão

- **OpenCV** (indiretamente)
  - Produção da máscara da mão
  - Visualização de resultados

- **PipelineObserver (infraestrutura própria)**
  - Registro das saídas intermediárias
  - Inspeção frame a frame

---

## Descrição do Algoritmo

### 1. Construção do Mapa de Pressão

O núcleo do Passo 5 é o **mapa de pressão**, que estabelece a relação:

```
corda × traste → pressionado / não pressionado
```

#### Estratégia adotada

Ao invés de verificar um único pixel na interseção corda–traste, o algoritmo:

- define uma **janela espacial de tolerância** ao redor da interseção
- verifica se **qualquer pixel da janela** pertence à máscara da mão

Isso torna o sistema robusto a:
- imprecisão geométrica
- variações de pose
- jitter temporal

#### Resultado

O mapa final assume a forma:

```
pressure_map[string_id] = [lista de trastes pressionados]
```

Cada corda pode ter zero ou mais trastes detectados como pressionados no frame.

---

### 2. Inferência de Notas Musicais

A partir do mapa de pressão, o sistema aplica uma regra musical simples e consistente:

- Para cada corda:
  - considera-se **o traste mais próximo do corpo** (maior índice)
  - este traste representa a nota efetivamente pressionada

Isso reflete a prática musical real:
- múltiplos dedos podem aparecer visualmente
- apenas o traste mais agudo define o comprimento vibrante da corda

O resultado é uma estrutura lógica do tipo:

```
notes[string_id] = fret_id
```

ou `None` caso a corda esteja solta.

---

## Fluxo do Pipeline no Passo 5

```
Imagem retificada
      ↓
Grid estabilizado (cordas + trastes)
      ↓
Máscara da mão
      ↓
Mapa de pressão corda × traste
      ↓
Seleção do traste efetivo por corda
      ↓
Notas visuais inferidas
```

---

## Saídas do Passo 5

Para cada frame processado, o Passo 5 produz:

1. **Mapa de pressão**
   - Estrutura intermediária observável
   - Útil para depuração e análise futura

2. **Notas visuais inferidas**
   - Uma nota por corda
   - Base para cruzamento com áudio no Passo 6

3. **Visualização diagnóstica**
   - Grid da escala
   - Indicação visual das notas detectadas

---

## Limitações Conhecidas

- Não diferencia dedos individuais
- Não resolve ambiguidade de oitava
- Pode gerar falsos positivos em oclusões não musicais

Essas limitações são **intencionais** neste estágio e serão tratadas no Passo 6.

---

## Conclusão

O Passo 5 estabelece, pela primeira vez no pipeline, uma **ponte direta entre visão computacional e semântica musical**. Ele transforma geometria e oclusão em hipóteses de notas, criando uma base sólida para a fusão multimodal subsequente.

Com este passo concluído, o sistema já é capaz de:

- observar a execução musical
- interpretar posições na escala
- produzir uma leitura musical visual frame a frame

O próximo passo natural é a validação cruzada com o áudio, reduzindo incertezas e preparando o terreno para a geração de tablatura.

