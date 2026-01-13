# Relatório — Passo 4  
## Detecção Visual da Mão e Inferência de Pressão na Escala da Guitarra

---

## 1. Objetivo do Passo 4

O Passo 4 tem como objetivo introduzir a **mão do músico** no pipeline visual, tratando-a inicialmente como um **oclusor físico** da escala da guitarra, e não como um conjunto de dedos individuais.

A partir dessa oclusão, o sistema passa a inferir **pressão corda × traste**, criando a base necessária para:

- identificar quais notas estão sendo pressionadas visualmente (Passo 5);
- cruzar informação visual com áudio (Passo 6);
- gerar tablatura final (Passo 7).

Este passo prioriza **robustez geométrica e musical**, evitando refinamentos prematuros (como detecção direta de dedos).

---

## 2. Princípio Conceitual

Em vez de perguntar imediatamente:

> “Qual dedo está em qual traste?”

o sistema passa a perguntar algo mais simples e fisicamente consistente:

> “Quais regiões da escala estão ocluídas pela mão?”

A partir disso, a pressão é inferida pela **interseção espacial** entre:

- o **grid fixo da escala** (cordas e trastes);
- a **região ocupada pela mão**.

Esse raciocínio respeita a física real do instrumento e reduz drasticamente falsos positivos.

---

## 3. Ferramentas e Técnicas Utilizadas

### 3.1 OpenCV
Utilizado para:
- manipulação de imagens;
- operações geométricas;
- visualização e debug;
- projeções e interseções espaciais.

### 3.2 Roboflow Inference API
Usada indiretamente no Passo 2 para:
- detectar a região da escala da guitarra em cada frame;
- fornecer um ROI confiável para todo o pipeline visual subsequente.

No Passo 4, assume-se que a escala já está corretamente localizada.

### 3.3 ORB (Oriented FAST and Rotated BRIEF)
Utilizado para:
- estabilização temporal do ROI;
- evitar jitter e colapso do grid entre frames consecutivos.

### 3.4 Heurísticas Geométrico-Musicais
Aplicadas para:
- fixar identidade de trastes e cordas ao longo do tempo;
- garantir coerência musical (trastes progressivamente mais próximos).

### 3.5 Segmentação da Mão
A mão é tratada como uma **máscara binária de oclusão**, não como objeto semântico complexo.

---

## 4. Arquitetura Geral do Pipeline no Passo 4

O Passo 4 é executado **frame a frame**, reutilizando a saída consolidada do Passo 2.

Pipeline lógico:

1. Receber frame bruto do vídeo
2. Detectar escala (já resolvido no Passo 2)
3. Estabilizar temporalmente o ROI
4. Retificar geometricamente a escala
5. Detectar trastes e cordas
6. Fixar identidade temporal do grid
7. Detectar a mão como oclusor
8. Inferir pressão corda × traste
9. Gerar visualizações e estados intermediários
10. Armazenar histórico completo de execução

---

## 5. Detecção da Mão como Oclusor

### 5.1 Entrada
- Frame da escala já retificado e estabilizado.

### 5.2 Processamento
- Conversão para espaço apropriado (ex: HSV ou YCrCb).
- Segmentação por cor/forma/movimento.
- Pós-processamento morfológico para eliminar ruído.
- Geração de:
  - máscara binária da mão;
  - bounding box aproximada da região oclusora.

### 5.3 Saída
- `hand_mask`: imagem binária indicando pixels ocupados pela mão.
- `hand_bbox`: bounding box para referência espacial.

A mão não é classificada por dedo nesta etapa.

---

## 6. Inferência de Pressão Corda × Traste

### 6.1 Princípio

Uma nota está pressionada se, e somente se:

> a região da mão intercepta uma interseção válida entre uma corda e um traste.

### 6.2 Entrada
- `hand_mask`
- lista de coordenadas das cordas
- lista de coordenadas dos trastes

### 6.3 Processamento
Para cada par `(corda, traste)`:
- define-se uma pequena região ao redor da interseção;
- verifica-se se há pixels da mão nessa região.

### 6.4 Saída
- `pressure_map`: matriz booleana  
- pressure_map[string_index, fret_index] = True / False


Essa estrutura é o **elo direto** entre visão computacional e teoria musical.

---

## 7. Visualizações Diagnósticas

Para garantir interpretabilidade e debug contínuo, o sistema gera visualizações automáticas:

- Frame bruto
- ROI da escala
- Frame estabilizado
- Frame retificado
- Grid (cordas + trastes)
- Máscara da mão sobreposta
- Mapa de pressão com marcações visuais

Esses frames são:
- exibidos automaticamente (amostragem de até 20);
- armazenados em disco por etapa.

---

## 8. Observer de Pipeline (Histórico Completo)

Foi introduzido um **PipelineObserver**, responsável por:

- salvar todos os frames intermediários;
- organizar saídas por etapa (`raw`, `roi`, `hand`, `pressure`, etc.);
- permitir validação offline e reprodutibilidade científica.

Isso transforma o pipeline em um **sistema auditável**, não uma caixa-preta.

---

## 9. Estado Atual ao Final do Passo 4

Ao final deste passo, o sistema é capaz de:

- localizar a escala da guitarra;
- estabilizar e retificar sua geometria;
- identificar trastes e cordas com identidade fixa;
- detectar a mão como oclusor;
- inferir pressão por corda e traste;
- fornecer dados estruturados para inferência de notas.

Nenhuma inferência musical ainda é feita — apenas a **base física e geométrica**.

---

## 10. Próximo Passo

### Passo 5 — Inferência Visual de Notas

Objetivo:
- mapear pressão `(corda, traste)` → nota musical;
- lidar com cordas soltas;
- preparar dados para fusão com áudio no Passo 6.

O sistema agora está pronto para sair do domínio puramente visual e entrar na **interpretação musical propriamente dita**.

---
