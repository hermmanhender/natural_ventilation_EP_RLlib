from typing import Any, Dict


def reward_function_T3(config: Dict[str, Any], obs: Dict, infos: Dict) -> float:
    """This function returns the reward calcualted as the absolute value of the cube in the 
    difference between set point temperatur for comfort and the temperature measured in the 
    thermal zone when there are people in the zone but zero when is not.

    Args:
        config (Dict[str, Any]): env_config dictionary. Optionaly you can configurate the 'T_confot' variable.
        obs (Dict): Zone Mean Air Temperature for the Thermal Zone in °C.
        infos (Dict): infos dict must to provide the occupancy level and the Zone Mean Temperature.

    Returns:
        float: reward value
    """
    agent_ids = config['agent_ids']
    T_confort = config.get('T_confort', 22)
    occupancy = infos[agent_ids[0]]['occupancy']
    T_zone = infos[agent_ids[0]]['Ti']
    if occupancy > 0: # When there are people in the thermal zone, a reward is calculated.
        reward = -(min(abs((T_confort - T_zone)**3),343.))
    else:
        # If there are not people, only the reward is calculated when the environment is far away
        # from the comfort temperature ranges. This limits are recommended in EnergyPlus documentation:
        # InputOutput Reference p.522
        if T_zone > 29.4:
            reward = -343.
        elif T_zone < 16.7:
            reward = -343.
        else:
            reward = 0.
    return reward

def reward_function_T2(config: Dict[str, Any], obs: Dict, infos: Dict) -> float:
    """This function returns the reward calcualted as the absolute value of the square in the 
    difference between set point temperatur for comfort and the temperature measured in the 
    thermal zone when there are people in the zone but zero when is not.

    Args:
        config (Dict[str, Any]): env_config dictionary. Optionaly you can configurate the 'T_confot' variable.
        obs (Dict): Zone Mean Air Temperature for the Thermal Zone in °C.
        infos (Dict): infos dict must to provide the occupancy level and the Zone Mean Temperature.

    Returns:
        float: reward value
    """
    agent_ids = config['agent_ids']
    T_confort = config.get('T_confort', 22)
    occupancy = infos[agent_ids[0]]['occupancy']
    T_zone = infos[agent_ids[0]]['Ti']
    if occupancy > 0: # When there are people in the thermal zone, a reward is calculated.
        reward = -(min(abs((T_confort - T_zone)**2),49.))
    else:
        # If there are not people, only the reward is calculated when the environment is far away
        # from the comfort temperature ranges. This limits are recommended in EnergyPlus documentation:
        # InputOutput Reference p.522
        if T_zone > 29.4:
            reward = -49.
        elif T_zone < 16.7:
            reward = -49.
        else:
            reward = 0.
    return reward

def reward_function_T3_Energy(config: Dict[str, Any], obs: Dict, infos: Dict) -> float:
    """This function returns the reward calcualted as the absolute value of the cube in the 
    difference between set point temperatur for comfort and the temperature measured in the 
    thermal zone when there are people in the zone but zero when is not.

    Args:
        config (Dict[str, Any]): env_config dictionary. Optionaly you can configurate the 'T_confot' variable.
        obs (Dict): Zone Mean Air Temperature for the Thermal Zone in °C.
        infos (Dict): infos dict must to provide the occupancy level and the Zone Mean Temperature.

    Returns:
        float: reward value
    """
    agent_ids = config['agent_ids']
    
    beta_reward = config['beta_reward'] if config.get('beta_reward', False) else 0.5
    T_confort = config.get('T_confort', 22)
    occupancy = infos[agent_ids[0]]['occupancy']
    T_zone = infos[agent_ids[0]]['Ti']
    cooling_meter = infos[agent_ids[0]]['cooling_meter']
    heating_meter = infos[agent_ids[0]]['heating_meter']
    
    if occupancy > 0: # When there are people in the thermal zone, a reward is calculated.
        reward = -beta_reward*(cooling_meter+heating_meter) -(1-beta_reward)*(min(abs((T_confort - T_zone)**3),343.))
    else:
        # If there are not people, only the reward is calculated when the environment is far away
        # from the comfort temperature ranges. This limits are recommended in EnergyPlus documentation:
        # InputOutput Reference p.522
        if T_zone > 29.4:
            reward = -beta_reward*(cooling_meter+heating_meter) -(1-beta_reward)*343.
        elif T_zone < 16.7:
            reward = -beta_reward*(cooling_meter+heating_meter) -(1-beta_reward)*343.
        else:
            reward = -beta_reward*(cooling_meter+heating_meter)
    return reward
    
def PPD_Energy_reward(config: Dict[str, Any], obs: Dict, infos: Dict) -> float:
    """This function returns the reward calcualted as the absolute value of the cube in the 
    difference between set point temperatur for comfort and the temperature measured in the 
    thermal zone when there are people in the zone but zero when is not.

    Args:
        config (Dict[str, Any]): env_config dictionary. Optionaly you can configurate the 'T_confot' variable.
        obs (Dict): Zone Mean Air Temperature for the Thermal Zone in °C.
        infos (Dict): infos dict must to provide the occupancy level and the Zone Mean Temperature.

    Returns:
        float: reward value
    """
    agent_ids = config['agent_ids']
    
    beta_reward = config['beta_reward'] if config.get('beta_reward', False) else 0.5
    cooling_meter = infos[agent_ids[0]]['cooling_meter']
    heating_meter = infos[agent_ids[0]]['heating_meter']
    PPD = infos[agent_ids[0]]['ppd']
    
    return -beta_reward*(cooling_meter + heating_meter) -(1-beta_reward)*PPD
    
