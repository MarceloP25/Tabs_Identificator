import cv2
import numpy as np


class ORBStabilizer:
    """
    Estabilizador temporal baseado em ORB.
    Objetivo:
      - reduzir jitter entre frames
      - manter coerência geométrica do braço da guitarra
      - não interferir quando o frame já está estável
    """

    def __init__(
        self,
        max_features: int = 1000,
        min_matches: int = 15,
        det_threshold: float = 0.4,
        identity_eps: float = 0.02
    ):
        self.orb = cv2.ORB_create(max_features)

        self.prev_gray = None
        self.prev_kp = None
        self.prev_des = None

        self.min_matches = min_matches
        self.det_threshold = det_threshold
        self.identity_eps = identity_eps

    # --------------------------------------------------
    # Pré-processamento estrutural para ORB
    # --------------------------------------------------
    def _structural_view(self, frame):
        """
        Gera uma visão estrutural do frame:
        reduz influência de iluminação, dedos e textura fina.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)

        structural = cv2.convertScaleAbs(
            cv2.addWeighted(grad_x, 0.5, grad_y, 0.5, 0)
        )

        return structural

    # --------------------------------------------------
    # Validação da homografia estimada
    # --------------------------------------------------
    def _is_valid_homography(self, H):
        if H is None:
            return False

        # Determinante da parte afim (evita colapso ou explosão)
        det = np.linalg.det(H[:2, :2])
        if abs(det) < self.det_threshold:
            return False

        # Verifica se é praticamente identidade
        identity = np.eye(3)
        if np.linalg.norm(H - identity) < self.identity_eps:
            return False

        return True

    # --------------------------------------------------
    # Estabilização principal
    # --------------------------------------------------
    def stabilize(self, frame):
        """
        Retorna:
          - frame estabilizado
          - homografia aplicada (ou None)
        """

        structural = self._structural_view(frame)
        kp, des = self.orb.detectAndCompute(structural, None)

        # Inicialização
        if self.prev_des is None or des is None:
            self.prev_gray = structural
            self.prev_kp = kp
            self.prev_des = des
            return frame, None

        # Matching
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(self.prev_des, des)

        # Poucos matches → reset
        if len(matches) < self.min_matches:
            self.prev_gray = structural
            self.prev_kp = kp
            self.prev_des = des
            return frame, None

        # Pontos correspondentes
        src_pts = np.float32(
            [self.prev_kp[m.queryIdx].pt for m in matches]
        ).reshape(-1, 1, 2)

        dst_pts = np.float32(
            [kp[m.trainIdx].pt for m in matches]
        ).reshape(-1, 1, 2)

        H, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        # Atualiza estado interno
        self.prev_gray = structural
        self.prev_kp = kp
        self.prev_des = des

        # Homografia inválida → não aplica
        if not self._is_valid_homography(H):
            return frame, None

        # Aplica estabilização
        h, w = frame.shape[:2]
        stabilized = cv2.warpPerspective(frame, H, (w, h))

        return stabilized, H
