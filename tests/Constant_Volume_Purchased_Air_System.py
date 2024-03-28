"""
# Example 7. Constant Volume Purchased Air System

## Problem Statement

The simplest way to add HVAC control to an EnergyPlus thermal zone is to 
use the ZoneHVAC:IdealLoadsAirSystem. This was called purchased air in 
older versions. The ideal loads air system is intended for load calculations. 
You provide input for the supply air conditions of drybulb and humidity 
ratio, but the flow rate cannot be controlled. The model operates by 
varying the flow rate to exactly meet the desired setpoints. However, you 
may want to experiment with various designs in a slightly different way in 
which, given a prescribed supply air situation, then adjust the design to 
maximize the thermal comfort. It would be interesting to use the 
simple-toinput purchased air model to examine how a zone responds to a 
system, rather than how the system responds to a zone. We should ask, 
Can we use the EMS to prescribe the supply air flow rates for a purchased 
air model?

## EMS Design Discussion

For this example we begin with the input file from Example 6 (primarily 
because it already has purchased air). We examine the typical mass flow 
rates the air system provides to have some data to judge what an appropriate 
constant flow rate might be. A cursory review of the data indicates that 
cooling flow rates of 0.3 kg/s are chosen for two zones and 0.4 kg/s is 
chosen for the third. Heating flow rates of 0.1 and 0.15 kg/s are also chosen.

We want the model to respond differently for heating and cooling. We define 
two operating states and create global variables to hold that state for 
each zone. The first state is when the zone calls for heating; we will 
assign a value of 1.0. The second is when the zone calls for cooling; we 
assign 2.0.

To sense the state we will use EMS sensors associated with the output 
variable called “Zone/Sys Sensible Load Predicted.” We will set up one of 
these for each zone and use it as input data. If this value is less than 
zero, the zone is in the cooling state. If it is greater than zero, the zone 
is in the heating state. This predicted load is calculated during the 
predictor part of the model, so we choose the EMS calling point called 
“AfterPredictorAfterHVACManagers.”

An EMS actuator is available for the ideal loads air system that overrides 
the air mass flow rate (kg/s) delivered by the system when it is on. The 
override is not absolute in that the model will still apply the limits 
defined in the input object and overrides only if the system is “on.” 
The internal logic will turn off the air system if the zone is in the 
thermostat dead band or scheduled “off” by availability managers. This “off” 
state is modeled inside the ideal loads air system so it does not need to 
be calculated in Erl. This control leads to a constant volume system that 
cycles in an attempt to control the zone conditions. In practice, it can 
achieve relatively good control when loads do not exceed the available capacity.
"""

# import the necessary libraries
import time
from tempfile import TemporaryDirectory
from gymnasium.spaces import Discrete
import ray
from ray import air, tune
from ray.tune import register_env
from ray.rllib.algorithms.dqn.dqn import DQNConfig
from ray.rllib.policy.policy import PolicySpec
from eprllib.env.multiagent.marl_ep_gym_env import EnergyPlusEnv_v0
from eprllib.tools import rewards, utils, action_transformers

# define the eprllib configuration
env_config={
    # === ENERGYPLUS OPTIONS === #
    'epjson': "C:/EnergyPlusV23-2-0/ExampleFiles/RefBldgSmallOfficeNew2004_Chicago.idf",
    "epw_training": "C:/EnergyPlusV23-2-0/WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw",
    "epw": "C:/EnergyPlusV23-2-0/WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw",
    'output': TemporaryDirectory("output","eprllib",'path_to_outputs_folder'),
    'ep_terminal_output': False,
    
    # === EXPERIMENT OPTIONS === #
    'is_test': False,
    
    # === ENVIRONMENT OPTIONS === #
    'action_space': Discrete(4),
    'action_transformer': action_transformers.thermostat_dual,
    'reward_function': rewards.PPD_Energy_reward,
    "ep_variables":{
        "To": ("Site Outdoor Air Drybulb Temperature", "Environment"),
        "Ti": ("Zone Mean Air Temperature", "Core_ZN"),
        "v": ("Site Wind Speed", "Environment"),
        "d": ("Site Wind Direction", "Environment"),
        "RHo": ("Site Outdoor Air Relative Humidity", "Environment"),
        "RHi": ("Zone Air Relative Humidity", "Core_ZN"),
        "pres": ("Site Outdoor Air Barometric Pressure", "Environment"),
        "occupancy": ("Zone People Occupant Count", "Core_ZN"),
        "ppd": ("Zone Thermal Comfort Fanger Model PPD", "Core_ZN People")
    },
    "ep_meters": {
        "heating_meter": "Heating:Electricity: Core_ZN",
        "cooling_meter": "Cooling:Electricity: Core_ZN",
    },
    "ep_actuators": {
        "cooling_setpoint": ("Zone Temperature Control", "Cooling Setpoint", "Core_ZN"),
        "heating_serpoint": ("Zone Temperature Control", "Heating Setpoint", "Core_ZN"),
    },
    'time_variables': [
        'hour',
        'day_of_year',
        'day_of_the_week',
        ],
    'weather_variables': [
        'is_raining',
        'sun_is_up',
        "today_weather_beam_solar_at_time",
        ],
    "infos_variables": ["ppd", 'heating_meter', 'cooling_meter'],
    "no_observable_variables": ["ppd"],
    
    # === OPTIONAL === #
    "timeout": 10,
    'beta_reward': 0.5,
    "weather_prob_days": 2
}

# inicialize ray server and after that register the environment
ray.init()
register_env(name="EPEnv", env_creator=lambda args: EnergyPlusEnv_v0(args))

# configurate the algorithm
def policy_mapping_fn(agent_id, episode, worker, **kwargs):
    return "shared_policy"

algo = DQNConfig().training(
    # === General Algo Configs === #
    gamma = 0.99,
    lr = 0.01,
    grad_clip = 40,
    grad_clip_by = 'global_norm',
    train_batch_size = 256,
    model = {
        "fcnet_hiddens": [256,256,256],
        "fcnet_activation": "relu",
        },
    optimizer = {},
    # === DQN Configs === #
    num_atoms = 100,
    v_min = -343,
    v_max = 0,
    noisy = True,
    sigma0 = 0.7,
    dueling = True,
    hiddens = [256],
    double_q = True,
    n_step = 12,
    replay_buffer_config = {
        '_enable_replay_buffer_api': True,
        'type': 'MultiAgentPrioritizedReplayBuffer',
        'capacity': 5000000,
        'prioritized_replay_alpha': 0.7,
        'prioritized_replay_beta': 0.6,
        'prioritized_replay_eps': 1e-6,
        'replay_sequence_length': 1,
        },
    categorical_distribution_temperature = 0.5,
).environment(
    env="EPEnv",
    env_config=env_config,
).framework(
    framework = 'torch',
).rollouts(
    num_rollout_workers = 7,
    create_env_on_local_worker=True,
    rollout_fragment_length = 'auto',
    enable_connectors = True,
    num_envs_per_worker=1,
).experimental(
    _enable_new_api_stack = False,
).multi_agent(
    policies = {
        'shared_policy': PolicySpec(),
    },
    policy_mapping_fn = policy_mapping_fn,
).resources(
    num_gpus = 0,
)
algo.exploration(
    exploration_config={
        "type": "EpsilonGreedy",
        "initial_epsilon": 1.,
        "final_epsilon": 0.,
        "epsilon_timesteps": 6*24*365*100,
    }
)

# init the training loop
tune.Tuner(
    "DQN",
    tune_config=tune.TuneConfig(
        mode="max",
        metric="episode_reward_mean",
    ),
    run_config=air.RunConfig(
        stop={"episodes_total": 200},
        checkpoint_config=air.CheckpointConfig(
            checkpoint_at_end = True,
            checkpoint_frequency = 10,
        ),
    ),
    param_space=algo.to_dict(),
).fit()

# close the ray server
ray.shutdown()
