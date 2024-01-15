# Firewall AI

This work consists of building a system that acts as a firewall for detecting denial-of-service attacks. To perform these detections, Machine Learning and Deep Learning techniques have been employed to train models with these capabilities. In addition, a graphical interface has been implemented through which the traffic received by the system can be observed in real-time, as well as the predictions it makes about whether or not the traffic is an attack.

Firstly, to train an artificial intelligence model, training data is required. A dataset has been chosen that contains different characteristics about a large number of network flows and a label indicating whether it is an attack, and if so, what type of attack it is. After choosing the dataset, a preprocessing stage is necessary, which consists of preparing the data so that the training phase is good. Once the data is ready, two models have been trained. The first is a neural network, specifically, a multilayer perceptron, and the second is a gradient boosting algorithm based on decision trees. After training, evaluating, and comparing them, it has been found that the gradient boosting model outperforms the neural network, achieving 99\% accuracy on the validation dataset, so this model has been used when launching the system.

On the other hand, it has been necessary to implement a tool to capture network traffic, which is also capable of obtaining the same characteristics about network flows that are used for model training. To do this, an existing tool developed by the same university that created the dataset used has been used as a base. However, this tool does not meet all the requirements necessary to be included in this work, so a version of it that does meet the requirements has been implemented.

Finally, a graphical interface has been implemented that allows traffic to be visualized and all of this has been integrated under the same system. After conducting several experiments, quite promising results have been obtained, as the system has been able to detect denial-of-service attacks.

***

# Installation

This system has been developed Debian, but similar distributions should work as well. 

First, you have to install the dependencies and clone this repository:

```bash
sudo apt install libpcap0.8
sudo apt install tcpdump
git clone https://github.com/DavidRamosArchilla/Firewall-AI.git
cd Firewall-AI
```

Then, it is advisable to create a Python virtual environment

```bash
python -m venv venv
source venv/bin/activate
```
and install the libraries
```bash
pip install -q --upgrade pip
pip install -q pyflowmeter
pip install -q -r Firewall-AI/requirements.txt
```

Lastly, run the command to start the server:

```
sudo venv/bin/python app.py
```

## Demo

There is a Google Colab notebook available with a demo of this project.

<a href="https://colab.research.google.com/github/DavidRamosArchilla/Firewall-AI/blob/main/notebooks/server_firewall_ai.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

Note: to obtain a free Ngrok token you need to access https://dashboard.ngrok.com/get-started/your-authtoken
