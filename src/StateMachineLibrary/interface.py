"""
Library interface.
"""

from typing import Union, Any, List, Dict

from .facade import StateMachineFacade


class StateMachineLibrary:
    """
    Library contains implementation of state machine to control or to test software components
    which can be in many states.

    .. contents ::


    Usage
    =====

    An example of using the library for LED blinking:

    .. code:: robotframework

        *** Settings ***
        Library  StateMachineLibrary

        *** Tasks ***
        Blink
            [setup]  Task Setup
            Run State Machine  start_from=Turn On Light  max_updates=10

        *** Keywords ***
        Task Setup
            Create State Machine  sm_name=blink-machine
            Add State  state=Turn On Light   on_update=On Update Turn On Light
            Add State  state=Turn Off Light  on_update=On Update Turn Off Light

        Turn On Light
            Log To Console  I am ONcc

        On Update Turn On Light
            Sleep  0.25s
            Go To State  state=Turn Off Light

        Turn Off Light
            Log To Console  I am OFF

        On Update Turn Off Light
            Sleep  0.25s
            Go To State  state=Turn On Light


    Flow diagram:

    .. image:: https://raw.githubusercontent.com/marcinooo/robot-framework-state-machine/main/states_flow.png
        :width: 760
        :alt: Flow diagram for above code


    Installation
    ============

    Install from PyPI:

    ``$ pip install robotframework-statemachinelibrary``

    Install from github:

    ``$ pip install git+https://github.com/marcinooo/robot-framework-state-machine``


    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_DOC_FORMAT = 'reST'

    def __init__(self) -> None:
        self._facade = StateMachineFacade()

    def create_state_machine(self, sm_name: str) -> None:
        """
        Creates state machine object. State machine controls flow in your tests suite or tasks suite definition.

        Example of flow:

        .. code::

            state A  ->  state B  ->  state C  ->  state A  ->  state B
                                              `->  state C

        |

        Example:

        +----------------------+-----------------------+
        | Create State Machine | sm_name=blink-machine |
        +----------------------+-----------------------+

        |

        :param sm_name: name of state machine given by you
        :return: None
        """

        self._facade.create_state_machine(sm_name)

    def destroy_state_machine(self, sm_name: str) -> None:
        """
        Destroys state machine object. Indicated state machine will not be available after call it.

        Example:

        +-----------------------+-----------------------+
        | Destroy State Machine | sm_name=blink-machine |
        +-----------------------+-----------------------+

        |

        :param sm_name: name of created state machine
        :return: None
        """

        self._facade.destroy_state_machine(sm_name)

    def run_state_machine(self,
                          start_from: Union[str, None] = None,
                          max_updates: Union[int, None] = -1,
                          sm_name: Union[str, None] = None) -> None:
        """
        Runs state machine. It calls continuously keyword to update state.

        ..warning::
            If "max_updates" argument is -1 it starts infinite loop.
            If this case you can use `Stop State Machine` keyword to stop loop.

        |

        Example:

        +---------------------+----------------------------+----------------+-----------------------+
        | | Go To State       | | state=Turn On Light      |                |                       |
        | | Run State Machine | |                          |                |                       |
        +---------------------+----------------------------+----------------+-----------------------+
        | Run State Machine   | start_from=Turn On Light   |                |                       |
        +---------------------+----------------------------+----------------+-----------------------+
        | Run State Machine   | start_from=Turn On Light   | max_updates=10 |                       |
        +---------------------+----------------------------+----------------+-----------------------+
        | Run State Machine   | start_from=Turn On Light   | max_updates=10 | sm_name=blink-machine |
        +---------------------+----------------------------+----------------+-----------------------+

        |

        :param start_from: name of keyword where to jump before updates
        :param max_updates: number of updates of state machine
        :param sm_name: name of state machine
        :return: None
        """

        self._facade.run_state_machine(sm_name, start_from, max_updates)

    def stop_state_machine(self, sm_name: Union[str, None] = None) -> None:
        """
        Stops state machine. It interrupts loop in `Run State Machine...` keyword.

        Example:

        +----------------------+-----------------------+
        | Stop State Machine   |                       |
        +----------------------+-----------------------+
        | Stop State Machine   | sm_name=blink-machine |
        +----------------------+-----------------------+

        |

        :param sm_name: name of state machine
        :return: None
        """

        self._facade.stop_state_machine(sm_name)

    def get_state_machine_states(self, sm_name: Union[str, None] = None) -> List[str]:
        """
        Gets list of states added to given state machine.

        Example:

        +------------+--------------------------+-----------------------+
        | @{states}= | Get State Machine States |                       |
        +------------+--------------------------+-----------------------+
        | @{states}= | Get State Machine States | sm_name=blink-machine |
        +------------+--------------------------+-----------------------+

        |

        :param sm_name: name of state machine
        :return: list of states
        """

        return self._facade.get_state_machine_states(sm_name)

    def add_state(self, state: str, on_update: str, sm_name: Union[str, None] = None) -> None:
        """
        Adds single state to state machine. To creates state you have to define state keyword
        which contains main code of state to execute. In addition, you have to define a method that contains
        the transition logic to the next state.

        Example:

        +-----------+---------------------+-----------------------------------+-----------------------+
        | Add State | state=Turn On Light | on_update=On Update Turn On Light |                       |
        +-----------+---------------------+-----------------------------------+-----------------------+
        | Add State | state=Turn On Light | on_update=On Update Turn On Light | sm_name=blink-machine |
        +-----------+---------------------+-----------------------------------+-----------------------+

        |

        :param state: name of keyword with main state logic
        :param on_update: name of keyword with transition logic to the next state
        :param sm_name: name of state machine
        :return: None
        """

        self._facade.add_state(state, on_update, sm_name)

    def go_to_state(self, state: str, sm_name: Union[str, None] = None) -> None:
        """
        Jumps to specified state. State is identified by name of main keyword.

        .. warning::
            You can not use it in main keyword for given state.

        |

        Example:

        +-------------+----------------------+-----------------------+
        | Go To State | state=Turn Off Light |                       |
        +-------------+----------------------+-----------------------+
        | Go To State | state=Turn Off Light | sm_name=blink-machine |
        +-------------+----------------------+-----------------------+

        |

        :param state: name of next keyword
        :param sm_name: name of state machine
        :return: None
        """

        self._facade.go_to_state(state, sm_name)

    def update_state(self, sm_name: Union[str, None] = None) -> None:
        """
        Goes to next state. It calls keyword with transition logic to the next state and main keyword from next state.
        Next state is indicated in keyword with transition logic for current state.

        Example:

        +--------------+-----------------------+
        | Update State |                       |
        +--------------+-----------------------+
        | Update State | sm_name=blink-machine |
        +--------------+-----------------------+

        |

        :param sm_name: name of state machine
        :return: None
        """

        self._facade.update_state(sm_name)

    def get_context(self, sm_name: Union[str, None] = None) -> Dict:
        """
        Returns context for given state machine. Context is dictionary where you can store common resources
        for state machine.

        Example:

        +-------------+-------------+-----------------------+
        | &{context}= | Get Context |                       |
        +-------------+-------------+-----------------------+
        | &{context}= | Get Context | sm_name=blink-machine |
        +-------------+-------------+-----------------------+

        |

        :param sm_name: name of state machine
        :return: context as dictionary
        """

        return self._facade.get_context(sm_name)

    def set_context(self, context: Dict, sm_name: Union[str, None] = None) -> None:
        """
        Overwrites context for given state machine. All common resources for state machine will be overwritten.

        Example:

        +----------------+----------------------+-------------------------+
        | | &{context}=  | | Create Dictionary  | | required_status=OFF   |
        | | Set Context  | | context=${context} | |                       |
        +----------------+----------------------+-------------------------+
        | | &{context}=  | | Create Dictionary  | | required_status=OFF   |
        | | Set Context  | | context=${context} | | sm_name=blink-machine |
        +----------------+----------------------+-------------------------+

        |

        :param context: context to set
        :param sm_name: name of state machine
        :return: None
        """

        self._facade.set_context(context, sm_name)

    def update_context(self, sm_name: Union[str, None] = None, **items: Any) -> None:
        """
        Updates context for given state machine. It adds or overwrites passed items to existing context.

        Example:

        +---------------------+----------------------+-------------------------+
        | Update Context      | user=Leo             |                         |
        +---------------------+----------------------+-------------------------+
        | | &{items}=         | | Create Dictionary  | | status=FINISHED       |
        | | Update Context    | | result=${items}    | | sm_name=blink-machine |
        +---------------------+----------------------+-------------------------+
        | Update Context      | errors=1             |                         |
        +---------------------+----------------------+-------------------------+

        =>

        +----------------------+-----------------------------------+-------------------------------------+
        | **existing context** | **new items**                     | **results**                         |
        +----------------------+-----------------------------------+-------------------------------------+
        | {'time':'00:00'}     | {'user':'Leo'}                    | {'time':'00:00','user':'Leo'}       |
        +----------------------+-----------------------------------+-------------------------------------+
        | {'result':{}}        | {'result':{'status':'FINISHED'}}  | {'result':{'status':'FINISHED'}}    |
        +----------------------+-----------------------------------+-------------------------------------+
        | {'errors':0}         | {'errors':1}                      | {'errors':1}                        |
        +----------------------+-----------------------------------+-------------------------------------+

        |

        :param sm_name: name of state machine
        :param items: objects to add to context
        :return: None
        """

        self._facade.update_context(sm_name, **items)
