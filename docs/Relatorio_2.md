# Relatório — Passo 2  
## Visão Computacional do Braço da Guitarra

### Objetivo do Passo

O objetivo do Passo 2 é estabelecer uma **representação geométrica estável, consistente e temporalmente coerente do braço da guitarra** ao longo de todos os frames do vídeo.

Este passo não busca ainda identificar notas ou dedos, mas sim:
- localizar o braço da guitarra,
- estabilizá-lo ao longo do tempo,
- retificá-lo geometricamente,
- detectar e fixar a identidade dos **trastes** e **cordas**.

O resultado final deste passo é um **grid fretboard (corda × traste)** confiável, que servirá de base para as etapas posteriores de detecção da mão, dedos e inferência de notas.

---

## Ferramentas e Tecnologias Utilizadas

### OpenCV
Biblioteca principal de visão computacional, utilizada para:
- conversões de cor,
- detecção de bordas (Canny),
- transformadas de Hough,
- homografias e warping geométrico,
- ORB (Oriented FAST and Rotated BRIEF).

### Roboflow (Inference API)
Utilizado para **detecção do braço da guitarra** via modelo previamente treinado:
- Entrada: frame completo
- Saída: bounding box da escala da guitarra
- Substitui o uso de YOLO treinado localmente

Motivação:
- modelo já treinado e validado,
- redução de custo de setup e debug,
- compatível com processamento frame-a-frame.

### ORB (OpenCV)
Usado como **estabilizador temporal**:
- detecta pontos-chave no braço da guitarra,
- realiza matching entre frames consecutivos,
- estima homografia para reduzir jitter e drift temporal.

### Heurísticas Musicais
Aplicadas após a detecção geométrica para:
- filtrar falsos trastes,
- respeitar espaçamento progressivamente decrescente entre trastes,
- limitar o número máximo de trastes detectados.

---

## Estrutura Geral do Pipeline

Abaixo está o fluxo lógico completo do Passo 2, executado **para cada frame** do vídeo:

# Relatório — Passo 2  
## Visão Computacional do Braço da Guitarra

### Objetivo do Passo

O objetivo do Passo 2 é estabelecer uma **representação geométrica estável, consistente e temporalmente coerente do braço da guitarra** ao longo de todos os frames do vídeo.

Este passo não busca ainda identificar notas ou dedos, mas sim:
- localizar o braço da guitarra,
- estabilizá-lo ao longo do tempo,
- retificá-lo geometricamente,
- detectar e fixar a identidade dos **trastes** e **cordas**.

O resultado final deste passo é um **grid fretboard (corda × traste)** confiável, que servirá de base para as etapas posteriores de detecção da mão, dedos e inferência de notas.

---

## Ferramentas e Tecnologias Utilizadas

### OpenCV
Biblioteca principal de visão computacional, utilizada para:
- conversões de cor,
- detecção de bordas (Canny),
- transformadas de Hough,
- homografias e warping geométrico,
- ORB (Oriented FAST and Rotated BRIEF).

### Roboflow (Inference API)
Utilizado para **detecção do braço da guitarra** via modelo previamente treinado:
- Entrada: frame completo
- Saída: bounding box da escala da guitarra
- Substitui o uso de YOLO treinado localmente

Motivação:
- modelo já treinado e validado,
- redução de custo de setup e debug,
- compatível com processamento frame-a-frame.

### ORB (OpenCV)
Usado como **estabilizador temporal**:
- detecta pontos-chave no braço da guitarra,
- realiza matching entre frames consecutivos,
- estima homografia para reduzir jitter e drift temporal.

### Heurísticas Musicais
Aplicadas após a detecção geométrica para:
- filtrar falsos trastes,
- respeitar espaçamento progressivamente decrescente entre trastes,
- limitar o número máximo de trastes detectados.

---

## Estrutura Geral do Pipeline

Abaixo está o fluxo lógico completo do Passo 2, executado **para cada frame** do vídeo:

Frame bruto
->
Detecção do braço (Roboflow)
->
Recorte da ROI (escala)
->
Estabilização temporal (ORB)
->
Retificação geométrica
->
Detecção de trastes
->
Detecção de cordas
->
Fixação de identidade temporal do grid
->
Refinamento por homografia
->
Visualização diagnóstica

---

## Descrição Detalhada das Etapas

### 1. Detecção do Braço da Guitarra
Cada frame é enviado ao modelo do Roboflow, que retorna a bounding box correspondente à escala da guitarra.

Saída:
- ROI contendo apenas o braço
- coordenadas da bounding box no frame original

Essa etapa garante que todas as análises subsequentes operem em uma região de interesse consistente.

---

### 2. Estabilização Temporal (ORB)
Mesmo após o recorte, pequenas variações de câmera e movimento do músico geram instabilidade.

O ORB é utilizado para:
- detectar keypoints na ROI,
- fazer matching com o frame anterior,
- estimar uma homografia entre frames consecutivos,
- suavizar jitter e microdeslocamentos.

Resultado:
- braço da guitarra estabilizado no tempo,
- redução de ruído temporal nas etapas estruturais.

---

### 3. Retificação Geométrica do Braço
O braço é rotacionado e alinhado para que:
- os trastes fiquem aproximadamente verticais,
- as cordas aproximadamente horizontais.

Técnicas utilizadas:
- detecção de linhas dominantes com Hough,
- cálculo do ângulo médio,
- rotação afim,
- homografia inicial para normalização da perspectiva.

Essa etapa reduz a variabilidade geométrica e facilita a detecção estrutural.

---

### 4. Detecção de Trastes
Os trastes são detectados como **linhas quase verticais** usando:
- Canny para bordas,
- HoughLinesP para segmentos longos.

Em seguida, aplica-se uma heurística musical:
- elimina linhas muito próximas,
- garante espaçamento progressivamente menor,
- limita o número máximo de trastes detectados.

Saída:
- lista ordenada de coordenadas `x` dos trastes.

---

### 5. Detecção de Cordas
As cordas são detectadas como **linhas quase horizontais**:
- mesma base de Canny + Hough,
- filtragem por orientação.

Saída:
- lista ordenada de coordenadas `y` das cordas.

---

### 6. Fixação de Identidade Temporal do Grid
Detecções frame-a-frame podem oscilar levemente.

Para resolver isso, é utilizado um **tracker temporal do grid**:
- associa trastes e cordas atuais aos anteriores,
- suaviza posições com média exponencial,
- mantém identidade consistente ao longo do tempo.

Resultado:
- cada traste e corda mantém seu índice ao longo do vídeo.

---

### 7. Refinamento da Homografia com Base no Grid
Com trastes e cordas já identificados, o grid é usado como referência para:
- refinar a homografia,
- garantir que o espaço final seja retangular,
- padronizar o sistema de coordenadas.

Essa etapa fecha o ciclo geométrico do Passo 2.

---

### 8. Visualizações Diagnósticas
Para validação visual e debug, o sistema:
- desenha trastes (linhas verticais),
- desenha cordas (linhas horizontais),
- exibe até 20 frames amostrados aleatoriamente,
- pausa a execução até o fechamento das janelas.

Essas visualizações são essenciais para validar:
- estabilidade temporal,
- consistência geométrica,
- robustez estrutural.

---

## Saída Final do Passo 2

Para cada frame válido, o sistema produz:
- imagem do braço retificado,
- grid estável de trastes e cordas,
- correspondência temporal consistente.

Esses dados alimentam diretamente o **Passo 4 (detecção da mão e dedos)** e o **Passo 5 (inferência visual de notas)**.

---

## Status do Passo

✔️ Passo 2 concluído  
✔️ Pipeline funcional e validado visualmente  
✔️ Base geométrica sólida para as etapas seguintes
