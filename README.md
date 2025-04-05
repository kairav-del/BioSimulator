# 🧬 BioSimulator

**BioSimulator** is a biological world simulation built using Python and Pygame. In a dynamic environment, red blobs (predators) hunt green blobs (prey). Prey multiply over time, while predators rely on consuming them to survive — mimicking real-life ecological balance.

This simulation provides a visual and interactive way to understand basic population dynamics and predator-prey interactions.

---

## 🌱 Features

- Predators (Red) actively chase prey blobs.
- Prey (Green) multiply naturally over time.
- Basic simulation of population balance and survival.
- Graphs to visually show population
- Visually dynamic environment using Pygame.
- Realistic movement and interaction patterns.

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/BioSimulator.git
   
   cd BioSimulator
   ```
2. **Install the requirements**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the program**
   ```bash
   python main.py
   ```

---

## 💻 Tweaks
src -> entites.
There will be a `config.py`

The file will look as such:
```python
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60 

...
```

Make changes as you feel free to test out the program in different parameters/conditions. 


## 🤝 Contributing
We welcome contributions! Here’s how you can help:

Fork the project.
Create your feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/your-feature).
Create a Pull Request.

Ideas for contributions:

- Improving predator/prey logic
- Adding GUI sliders for controls
- Optimizing performance (Numba, JIT, etc.)
- Enhancing visual aesthetics



## 🤔 FAQ
Q: How many agents can this handle?
A: Around 300+ agents can be simulated before performance starts dropping. Code not fully optimized. 



