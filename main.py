from blackjackAgent import BlackjackAgent
import gymnasium as gym
from gymnasium.wrappers import RecordEpisodeStatistics
from tqdm import tqdm
import dill 
import time
import sys

args = sys.argv
visual = None
sleep = 0
if(len(args)<3):
    print("Iniciando el juego en modo entrenamiento, no se visualizará el juego")
    print("--------------------------------------------------------------------")
    print("Para visualizar el juego ejecuta python main.py --train False\n")
elif(args[1]!="--train"):
    print("Error en los argumentos, iniciando el juego en modo entrenamiento")
    print("--------------------------------------------------------------------")
    print("Para visualizar el juego ejecuta python main.py --train False\n")
else:
    if(args[2]=="False"):
        visual = "human"
        sleep = 0.5
        print("Iniciando el juego en modo visual, se entrenará lentamente")
        print("--------------------------------------------------------------------")
        print("Para entrenar el juego ejecuta python main.py --train True\n")
    else:
        print("Iniciando el juego en modo entrenamiento, no se visualizará el juego")
        print("--------------------------------------------------------------------")
        print("Para visualizar el juego ejecuta python main.py --train False\n")

# Hiperparámetros
learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)
final_epsilon = 0.1

env = gym.make(
                "Blackjack-v1",
                render_mode=visual,           
               )
env = RecordEpisodeStatistics(env, buffer_length=n_episodes)

try:
    agent = dill.load(open('blackjackAgent.pkl', 'rb'))
except:
    agent = BlackjackAgent(
        env=env,
        learning_rate=learning_rate,
        initial_epsilon=start_epsilon,
        epsilon_decay=epsilon_decay,
        final_epsilon=final_epsilon,
    )

for episode in tqdm(range(n_episodes)):
    obs, info = env.reset()
    done = False

    # Juega hasta que el juego termine
    while not done:
        action = agent.get_action(obs)
        time.sleep(sleep)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # Actualiza el agente
        agent.update(obs, action, reward, terminated, next_obs)

        # Actualiza el estado actual y si el juego ha terminado
        done = terminated or truncated
        obs = next_obs

    agent.decay_epsilon()
    #print(f"episode-{episode}", info["episode"])
    
dill.dump(agent, open('blackjackAgent.pkl', 'wb'))
env.close()