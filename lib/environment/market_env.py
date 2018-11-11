"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Market environment.
# **********************************************************************************#
"""
from gym import Env
from utils.exceptions import *
from . action_space import TradingActionSpace
from . env_snapshot import EnvSnapshot
from . step_info import StepInfo
from . observer import Observer


class MarketEnv(Env):
    """
    Base market environment inherited by gym Env.
    """
    action_space = TradingActionSpace()
    env_snapshot = EnvSnapshot(state=0, next_state=0, reward=0)
    observer = Observer()

    def __init__(self, **kwargs):
        """
        Initialize your environment parameter here.

        Args:
            **kwargs(**dict): key-word arguments when you initialize your environment.
        """
        valid_parameters = {
            'metadata',
            'reward_range',
            'spec',
            'action_space',
            'observation_space',
            'env_snapshot',
            'observer'
        }
        if not set(kwargs).issubset(set(valid_parameters)):
            raise Exceptions.INVALID_INITIALIZE_PARAMETERS
        self.__dict__.update(kwargs)

    def step(self, action, state_transition=None, reward_calculator=None, done_condition=None):
        """
        Run one time step of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            action(object): an action provided from policy makers
            state_transition(func): state transition function with it's inputs are action and current state
            reward_calculator(func): reward calculating function
            done_condition(func): done condition

        Returns:
            StepInfo: step info instance
        """
        error_format = ExceptionsFormat.NOT_IN_ACTION_SPACE
        assert action in self.action_space, error_format.format(action, self.action_space)
        state_transition = state_transition or (lambda a, s: s)
        reward_calculator = reward_calculator or (lambda n_s, o: 0)
        done_condition = done_condition or (lambda r: not (self.reward_range[0] <= r <= self.reward_range[1]))

        state = self.env_snapshot.state
        next_state = state_transition(action, state)
        observation = self.observer.observe()
        current_reward = reward_calculator(next_state, observation)
        self.env_snapshot.action = action
        self.env_snapshot.state = next_state
        self.env_snapshot.reward += current_reward

        done = done_condition(self.env_snapshot.reward)
        step_info_parameters = {
            'observation': observation,
            'reward': self.env_snapshot.reward,
            'done': done,
            'info': dict()
        }
        step_info = StepInfo(**step_info_parameters)
        return step_info

    def reset(self):
        """
        Resets the state of the environment and returns an initial observation.

        Returns:
             observation(object): the initial observation of the space.
        """
        self.env_snapshot.reset(state=0, next_state=0, reward=0)
        self.observer.reset()

    def render(self, mode='human'):
        """Renders the environment.

        The set of supported modes varies per environment. (And some
        environments do not support rendering at all.) By convention,
        if mode is:

        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        - ansi: Return a string (str) or StringIO.StringIO containing a
          terminal-style text representation. The text can include newlines
          and ANSI escape sequences (e.g. for colors).

        Note:
            Make sure that your class's metadata 'render.modes' key includes
              the list of supported modes. It's recommended to call super()
              in implementations to use the functionality of this method.

        Args:
            mode (str): the mode to render with

        Example:

        class MyEnv(Env):
            metadata = {'render.modes': ['human', 'rgb_array']}

            def render(self, mode='human'):
                if mode == 'rgb_array':
                    return np.array(...) # return RGB frame suitable for video
                elif mode is 'human':
                    ... # pop up a window and render
                else:
                    super(MyEnv, self).render(mode=mode) # just raise an exception
        """
        raise NotImplementedError

    def close(self):
        """Override _close in your subclass to perform any necessary cleanup.

        Environments will automatically close() themselves when
        garbage collected or when the program exits.
        """
        return

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        return

    @property
    def unwrapped(self):
        """Completely unwrap this env.

        Returns:
            gym.Env: The base non-wrapped gym.Env instance
        """
        return self


__all__ = [
    'MarketEnv'
]
