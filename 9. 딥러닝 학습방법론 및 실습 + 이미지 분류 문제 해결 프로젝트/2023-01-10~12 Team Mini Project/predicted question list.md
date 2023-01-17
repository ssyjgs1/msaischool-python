# 예상되는 공?격 질문 목록

- canva p.10 Augmentation 선정 사유
    - 새와 드론이 관측되는 날씨 고려
    - 거꾸로 나는 가능성 희박하다고 판단
    - etc
- canva p.14
    - CNN 구조가 왜 성능이 제한되거나 전성비에 중요한 곳에서 사용되는지?
    - depthwise separable convolutions, width multiplier & resolution multiplier parameter가 어떤 이유로 모델의 경량화와 이유가 있는지?
    - mobilenet에서 사용했다는 2개의 hyper-parameter는 무엇이고 어떤 영향을 미쳤길래 네트워크의 크기가 감소했는지?
- canva p.15 ~ 21
    - threshold 값 채택 이유?
        - 오차 범위 고려해서 95%로 선정. 한 번 발견되면 경고 발송
    - 낮은 확률임에도 드론으로 판정했을 때 경보 안 보내는 이유?
    - Not Label로 인한 판정 결과에 따른 대책?
- addition prediction(2023-01-17 회의)
    - 이미지 데이터셋 어떻게 구했고 뭐 썼냐?
    - 데이터셋의 크기가 너무 작지 않냐?
