"""This module contain the action spaces for diferent agents that operate devices in 
a centralized way.
"""
from typing import List, Tuple

class DualSetPoint:
    """This object is the Dual Set Point Thermostat in EnergyPlus to control the
    HVAC systems in a Thermal Zone.
    """
    def __init__(self, low:float=17., high:float=28., gap;float=1., step:float=1.) -> List[Tuple[int,int]]:
        """This class is inicializated as a List of Tuples that contain the possibles combinations
        of both thermostats, cooling and heating, with a gap between them. The step parameters give
        more or less granularity in the action space.

        Args:
            low (float): The lower temperature that the heating system allow to set the thermostat. Default is 17 ºC.
            high (float): The highest temperature that the cooing system allow to set the thermostat. Default is 17 ºC.
            gap (float): This parameter specify the minimal difference that both thermostats must to have, with a minimum of 1 ºC. Defaut is 1 ºC.
            step (float): This parameter ajust the precision and size of the action space. Default is 1 ºC.

        Returns:
            List[Tuple[int,int]]: The action space Tuple, with the heating and cooling thermostat, respectively.

        Example:
        >>> DualSetPoint(17,19,1,1)
        [(17,18),(17,19),(18,19)]
        """
        # The gap value is verify as >=1
        if gap < 1:
            print('The gap must be >=1. This is set in 1.')
            gap = 1
        # The step value is verify as >0.
        if not step > 0:
            print('The step must be a possitive number and different of 0. It is set in 1.')
            step = 1
        self.action_space = []
        
        for heat_setpoint in range(low, high, step):
            for cool_setpoint in range(low+gap, high+step, step):
                if cool_setpoint >= heat_setpoint+gap:
                    self.action_space.append([heat_setpoint,cool_setpoint])

        self.action_space_size = len(self.action_space)
    
    def dual_action(self, central_action: int) -> Tuple:
        """This method search in the action space with the central_action as index and returns
        the heating,cooling Tuple setpoints.

        Args:
            central_action (int): The centralize action taken by the agent.

        Returns:
            Tuple: (heating,cooling) setpoints for action=central_action.
        """
        if central_action < 0 or central_action > self.action_space_size:
            print('The action taken by the agent is out of the action space')
            return -1,-1
        return self.action_space[central_action]

class TwoWindowsCentralizedControl:
    def __init__(self):
        self.action_space = [
            [0,0],
            [0,1],
            [1,0],
            [1,1]
        ]
    
    def natural_ventilation_action(self, central_action: int):
        """_summary_

        Args:
            central_action (int): _description_

        Returns:
            _type_: _description_
        """
        return self.action_space[central_action]

    def natural_ventilation_central_action(self, action1: int, action2: int):
        """_summary_

        Args:
            action1 (int): _description_
            action2 (int): _description_

        Returns:
            _type_: _description_
        """
        index = 0
        for a in self.action_space:
            if a == [action1, action2]:
                central_action = index
                break
            else:
                index += 1
        
        return central_action
