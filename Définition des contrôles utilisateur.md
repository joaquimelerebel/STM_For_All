# Définition des contrôles utilisateur

## Table des matières

[TOC]

## Contrôles

### Stepper Motors / Piezo scan unit

| Contrôle de position / Offset | Contrôle de sensitivité | Derating / Facteur de limitation | Bias Voltage |
| :---------------------------: | :---------------------: | -------------------------------- | ------------ |
|       Modification +- x       |    Sensibilité en x     | Modification x                   | + mV         |
|       Modification +- y       |    Sensibilité en y     | Modification y                   | - mV         |

### Image processing & Video processing

| Resizing    | Filtering                       | Capture    |
| ----------- | ------------------------------- | ---------- |
| Offset +- x | High Pass / Low Pass / All Pass | Screenshot |
| Offset +- y | FFT (Fast Fourier Transform)    | Zoom       |

| Coloring | Visual                 | Error correction |
| -------- | ---------------------- | ---------------- |
| Solid    | Bilinear interpolation | Line             |
| Gradient | Saturation             | Spiral           |

### Planification / Scheduling

| Lancement de l'analyse |
| ---------------------- |
| Jour                   |
| Heure                  |
| Minute                 |
| Seconde                |

### Tip

| PID                | Scan Lenght | Tip Correction |
| ------------------ | ----------- | -------------- |
| KP, KI, KD         | Scan Rate   | x width        |
| Statistical errors |             | y width        |

### Tools

| Measures       |
| -------------- |
| Size of image  |
| Size of sample |
|                |

## Sourcing

| Info                                                         | Link                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Linear Regression                                            | https://aip.scitation.org/doi/10.1063/1.2390633              |
| Quantitative Analysis of Scanning Tunneling Microscopy Images | https://pubs.acs.org/doi/10.1021/la403546c                   |
| STM FIles from INSP                                          | https://drive.google.com/drive/folders/1Q84imby-wI3LIF9ZEruzN_bNZ2ZKj3jO?usp=sharing |
| Post-processing correction                                   | https://aip.scitation.org/doi/abs/10.1063/1.4974271?fbclid=IwAR3cfx_8Uuut7slV57v4lEIKumroYCwv1TIPx5y3wG-Rsqv-tEviiW53XIM&casa_token=sHhZTao4AWcAAAAA%3AqBezMNGByvv6-qq__1YZpdVy6bjlMF0hsYvz0IWEZ7gS2E2qEYcBa4CegujOcrQWPqd5W0Yh450&journalCode=rsi |
| Maximising the resolving power of the scanning tunneling microscope | https://ascimaging.springeropen.com/articles/10.1186/s40679-018-0056-7 |

