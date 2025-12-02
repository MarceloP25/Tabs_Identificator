# Relatório 1 — Sistema de Identificação Automática de Notas e Geração de Tablaturas via Visão Computacional

## 1. Introdução e Objetivo do Projeto

Este projeto visa o desenvolvimento de um sistema de **inteligência artificial multimodal**, capaz de **analisar vídeos de performances de guitarra, violão ou baixo** e identificar, em tempo real, as **notas, acordes e técnicas executadas**, gerando automaticamente uma **tablatura digital** correspondente à execução.

A abordagem combina **visão computacional** (para entender o posicionamento das mãos, dedos e o mapeamento do braço do instrumento) e **análise de áudio** (para detectar as notas e acordes emitidos). A fusão entre essas duas modalidades permite uma interpretação robusta da performance musical, tanto rítmica quanto harmônica e melódica.

---

## 2. Estrutura Geral do Sistema

O sistema segue um **pipeline em seis etapas principais**, cada uma com objetivos e ferramentas específicas:

| Etapa | Descrição | Objetivo | Ferramentas Principais |
| --- | --- | --- | --- |
| **1. Entrada e Pré-processamento** | Leitura do vídeo, extração de frames e áudio, correção de iluminação e ruído. | Preparar dados padronizados para análise. | OpenCV, MoviePy, Pydub |
| **2. Mapeamento visual do braço** | Identificar trastes e cordas com base em grid manual e detecção automática. | Construir referência espacial do instrumento. | YOLOv8, OpenCV |
| **3. Rastreamento de mãos e dedos** | Detectar e acompanhar landmarks das mãos do músico. | Associar posições visuais às notas tocadas. | MediaPipe Hands |
| **4. Processamento de áudio** | Extrair pitch, notas e acordes sincronizados com o vídeo. | Analisar o conteúdo sonoro da execução. | Librosa |
| **5. Fusão multimodal** | Combinar dados visuais e sonoros temporalmente. | Determinar notas exatas e localização no instrumento. | Pandas, NumPy |
| **6. Geração da tablatura** | Criar tablatura final legível. | Transformar dados em partitura textual. | Music21 |

---

## 3. Bases de Dados Referenciadas

Para treinar, calibrar e validar o sistema, são utilizadas as seguintes bases de dados:

| Base | Tipo de Dado | Utilização |
| --- | --- | --- |
| **GuitarSet (NYU)** | Áudio multitrack + tablaturas sincronizadas | Treinamento e validação de notas e acordes. |
| **IDMT-SMT-Guitar** | Notas isoladas, técnicas e timbres | Reconhecimento de solos e dedilhados. |
| **MusicNet** | Gravações + anotações musicais alinhadas | Refinamento do modelo de pitch. |
| **FIID (Fretted Instrument Image Dataset)** | Imagens de guitarras com anotações de trastes | Treinamento da detecção visual do braço. |
| **EgoHands / FreiHAND** | Rastreamento de mãos em vídeo | Treinamento do modelo MediaPipe. |

Essas bases cobrem todos os aspectos do sistema — da detecção visual ao reconhecimento sonoro.

---

## 4. Ferramentas e Bibliotecas

### 🔹 4.1. OpenCV

- **Função:** manipulação de vídeo e imagem (captura, processamento, segmentação).
- **Uso no código:**
    - Extração de frames (`cv2.VideoCapture`);
    - Conversão de cores (`cv2.cvtColor`);
    - Aplicação de filtros (Gaussiano, bilateral, mediana);
    - Equalização de histograma (`cv2.createCLAHE`);
    - Detecção de bordas (`cv2.Canny`).
- **Instalação:**
    
    ```bash
    pip install opencv-python
    
    ```
    
- **Resultado esperado:** frames tratados com iluminação uniforme e bordas nítidas.

---

### 🔹 4.2. MoviePy

- **Função:** leitura e manipulação de vídeos, extração de áudio.
- **Uso no código:**
    
    ```python
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip("video.mp4")
    clip.audio.write_audiofile("audio.wav")
    
    ```
    
- **Resultado esperado:** áudio sincronizado em `.wav` para análise pelo Librosa.

---

### 🔹 4.3. Pydub

- **Função:** tratamento e normalização de áudio.
- **Uso no código:**
    
    ```python
    from pydub import AudioSegment
    audio = AudioSegment.from_wav("audio.wav")
    audio = audio.set_channels(1).set_frame_rate(44100)
    audio.export("audio_clean.wav", format="wav")
    
    ```
    
- **Resultado esperado:** áudio limpo e padronizado (mono, 44.1kHz).

---

### 🔹 4.4. Librosa

- **Função:** extração de características sonoras (pitch, MFCCs, cromas, acordes).
- **Uso no código:** análise no domínio da frequência.
- **Resultado esperado:** lista temporal de notas tocadas.

---

### 🔹 4.5. MediaPipe Hands

- **Função:** detecção e rastreamento 3D das mãos e dedos.
- **Uso:** reconhecer posição dos dedos sobre o braço.
- **Resultado:** coordenadas (x, y, z) para cada dedo em cada frame.

---

### 🔹 4.6. YOLOv8

- **Função:** detecção automática de regiões (braço, trastes, cordas).
- **Uso:** localizar o braço do instrumento e segmentar trastes.
- **Resultado:** mapa de bounding boxes com classes detectadas.

---

### 🔹 4.7. Music21

- **Função:** modelagem e exportação da tablatura.
- **Uso:** traduz notas e posições em representação musical textual.
- **Saída:** `.txt`, `.musicxml` ou `.gp5`.

---

## 5. Passo 1 — Pré-Processamento e Tratamento Visual

O **Passo 1** é o ponto de partida do pipeline e envolve a preparação dos dados visuais e sonoros para as etapas seguintes.

---

### 5.1. Subetapas

| Subetapa | Descrição | Ferramentas |
| --- | --- | --- |
| **1. Leitura e extração de frames** | Conversão do vídeo em sequência de imagens. | OpenCV |
| **2. Extração e limpeza de áudio** | Separação do áudio e padronização. | MoviePy, Pydub |
| **3. Conversão de cor e equalização** | Ajuste de brilho, contraste e tonalidade. | OpenCV (YCrCb + CLAHE) |
| **4. Redução de ruído** | Filtro bilateral preservando bordas. | OpenCV |
| **5. Detecção de bordas** | Realce de contornos de trastes e cordas. | OpenCV (Sobel/Canny) |
| **6. Normalização e salvamento** | Padronização e exportação. | NumPy |

---

### 5.2. Pipeline Visual

O tratamento visual é aplicado a cada frame extraído do vídeo, seguindo esta ordem:

1. **Carregamento e conversão de cor:**
    
    ```python
    frame = cv2.imread("frame_001.jpg")
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    
    ```
    
2. **Equalização adaptativa (CLAHE):**
    
    ```python
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    y_eq = clahe.apply(y)
    ycrcb_eq = cv2.merge((y_eq, cr, cb))
    frame_eq = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)
    
    ```
    
3. **Filtragem de ruído:**
    
    ```python
    smooth = cv2.bilateralFilter(frame_eq, d=9, sigmaColor=75, sigmaSpace=75)
    
    ```
    
4. **Realce de bordas:**
    
    ```python
    edges = cv2.Canny(smooth, 50, 150)
    
    ```
    
5. **Combinação ponderada:**
    
    ```python
    enhanced = cv2.addWeighted(smooth, 0.8, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), 0.2, 0)
    
    ```
    
6. **Normalização e salvamento:**
    
    ```python
    norm = cv2.normalize(enhanced, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite("data/processed/frames_enhanced/frame_001.jpg", norm)
    
    ```
    

---

### 5.3. Resultados e Métricas

Cada frame tratado gera:

- **Imagem aprimorada:** com contraste uniforme e bordas bem definidas.
- **Metadados:** armazenando brilho médio, contraste e densidade de bordas (para calibrar o CLAHE).
- **Logs:** um CSV com as métricas por frame, permitindo autocalibração futura.

Essas imagens alimentam diretamente o **Passo 2**, que fará o reconhecimento do braço e a geração do grid.

---

### Estrutura de Diretórios

```
data/
 ├── raw/
 │   └── video_original.mp4
 ├── processed/
 │   ├── frames/
 │   ├── frames_enhanced/
 │   ├── audio/
 │   ├── metadata.json
 │   └── logs/

```

---

## 6. Próximos Passos (Passo 2)

O **Passo 2 — Mapeamento visual do braço** terá como objetivo:

- Detectar o braço e trastes com YOLOv8;
- Calibrar manualmente um grid de referência;
- Associar trastes às notas (em Hz e nomes musicais);
- Preparar o mapa para a fusão com o áudio e rastreamento de mãos.