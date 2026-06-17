# Edge-RL Irrigation: Autonomous Farm Control via Q-Learning

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Reinforcement%20Learning-Q--Learning-green?style=for-the-badge" alt="RL">
  <img src="https://img.shields.io/badge/MLOps-Guardrails%20%26%20Simulation-orange?style=for-the-badge" alt="MLOps">
</p>

---

## Project Overview
An autonomous smart greenhouse irrigation system powered by **Reinforcement Learning (Q-Learning)**. This project demonstrates an end-to-end MLOps pipeline, including agent training, data drift evaluation under severe drought, and hard-coded safety guardrails, culminating in a **virtual edge deployment** simulation over a socket network.

---

## System Architecture
Rather than a monolithic setup, the architecture simulates an industrial IoT deployment by decoupling the physical environment from the AI controller using **TCP/IP Socket Programming**:

```text
 ┌───────────────────────────────┐               ┌───────────────────────────────┐
 │   [Server: Greenhouse]      │               │   [Client: Raspberry Pi]    │
 │                               │               │                               │
 │  - Environment State Tracking │ ───(Data)───> │  - Pre-trained Q-Table Brain  │
 │  - Stochastic Weather (Drift) │ <──(Action)── │  - Inference & Guardrails     │
 └───────────────────────────────┘               └───────────────────────────────┘
                                 (Localhost via TCP/IP) 
```
---

## 📦 Project Structure

```text
├── 📄 smart_farm_rl.py       # Core training script with environment drift simulation
├── 🌐 greenhouse_server.py   # Decoupled server simulating the greenhouse state
└── 🤖 raspberry_bot.py       # Edge bot executing the smart actions via network sockets
```

---

## How to Run
### Step 1: Initialize the Physical Greenhouse (Server)
```Bash
python greenhouse_server.py
```
### Step 2: Boot the AI Controller (Virtual Raspberry Pi)
```Bash
python raspberry_bot.py
```

---

## Results & Key Learnings
- Baseline Performance: The agent achieves up to 185 points in steady-state environments.
- The Drift Challenge: Under unexpected severe weather anomalies (Data Drift), the model performance degrades to 50-120 points, highlighting the necessity of production monitoring.
- Hybrid Remediation: Integrating a Rule-Based Fallback System (Safety Override) successfully prevents crop failure, establishing a robust production-ready design.