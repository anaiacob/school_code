import numpy as np
import matplotlib.pyplot as plt

# Parametrii semnalului
sample_rate = 44100  # Frecvența de eșantionare (Hz)
duration = 5  # Durata semnalului (secunde)
N_Gr = 9  # Numărul grupei

# Semnal de intrare cu frecvență modificată
freq_signal = 950  # Hz
freq_noise = N_Gr * 120  # Hz
amplitude_signal = 0.036  # 36mV
amplitude_noise = 0.045  # 45mV

# Vector de timp
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generare semnal
signal = amplitude_signal * np.sin(2 * np.pi * freq_signal * t)
noise = amplitude_noise * np.sin(2 * np.pi * freq_noise * t)
v_input = signal + noise

# Amplificare modificată
amplification_factor = 90
v_output = np.clip(v_input * amplification_factor, -3, 3)

# Plotare semnale
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, v_input, color='limegreen')
plt.title('V(input) - Semnal ușor modificat')
plt.xlabel('Timp (s)')
plt.ylabel('Tensiune (V)')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t, v_output, color='dodgerblue')
plt.title('V(output) - Semnal amplificat modificat')
plt.xlabel('Timp (s)')
plt.ylabel('Tensiune (V)')
plt.grid(True)

plt.tight_layout()
plt.savefig("modified_signal_plot.png")
plt.show()
