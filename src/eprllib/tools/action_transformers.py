"""This script will be contain some action transformer methods to implement in
eprllib. Most of them are applied in the test section where examples to test the 
library are developed.
"""

def thermostat_dual(agent_id, action):
    """This method take a discret action in the range of [0,4) and transforms it
    into a temperature of cooling or heating setpoints, depending the agent id 
    involve.

    >>> thermostat_dual('cooling_setpoint', 0)
    23

    >>> thermostat_dual('coolind_setpoint', 1)
    24

    >>> thermostat_dual('heating_setpoint', 2)
    19

    >>> thermostat_dual('heating_setpoint', 3)
    18

    >>> thermostat_dual('bad_test', 1)
    -1
    """
    if agent_id == 'cooling_setpoint':
        transform_action = 23 + action
    elif agent_id == 'heating_setpoint':
        transform_action = 21 - action
    else:
        transform_action = -1
        print('The agent id it is not in the list of agents for this action_transform_method. The agent allowed are cooling_setpoint and heating_setpoint. Please notice that.')
    return transform_action
