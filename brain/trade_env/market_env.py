"""
# -*- coding: UTF-8 -*-
# **********************************************************************************#
#     File: Market trade_env.
# **********************************************************************************#
"""
from gym import Env
from copy import deepcopy
from utils.exceptions import *
from . action_space import TradingActionSpace
from . env_snapshot import EnvSnapshot
from . step_info import StepInfo
from . bar_quote import BarQuote
from . state import PortfolioState
from .. trade import FuturesPosition
from .. const import DEFAULT_MARGIN_CASH


class FuturesMarketEnv(Env):
    """
    Base market trade_env inherited by gym Env.
    """
    action_space = TradingActionSpace()
    env_snapshot = EnvSnapshot()
    bar_quote = BarQuote()

    def __init__(self, **kwargs):
        """
        Initialize your trade_env parameter here.

        Args:
            **kwargs(**dict): key-word arguments when you initialize your trade_env.
        """
        valid_parameters = {
            'metadata',
            'reward_range',
            'spec',
            'action_space',
            'observation_space',
            'env_snapshot',
            'bar_quote'
        }
        if not set(kwargs).issubset(set(valid_parameters)):
            raise Exceptions.INVALID_INITIALIZE_PARAMETERS
        for item in kwargs.items():
            setattr(self, *item)
        self._init_setting = {_: deepcopy(getattr(self, _, None)) for _ in valid_parameters}

    @classmethod
    def from_configs(cls, margin_cash=None, symbol=None,
                     multiplier=1, margin_rate=1., reward_range=None):
        """
        Instantiated by some parameter configs.

        Args:
            margin_cash(float): initial margin cash
            symbol(string): initial futures symbol
            multiplier(int): multiplier
            margin_rate(float): margin rate
            reward_range(tuple): reward range as (min, max)

        Returns:
            FuturesMarketEnv: instance
        """
        margin_cash = margin_cash or DEFAULT_MARGIN_CASH
        position_holding = FuturesPosition(symbol=symbol)
        portfolio_state = PortfolioState(margin_cash=margin_cash,
                                         position_holding=position_holding,
                                         multiplier=multiplier,
                                         margin_rate=margin_rate)
        env_snapshot = EnvSnapshot(state=portfolio_state)

        kwargs = {
            'env_snapshot': env_snapshot,
        }
        if reward_range:
            kwargs.update(reward_range)
        return cls(**kwargs)

    def step(self, action, state_transition=None, reward_calculator=None, done_condition=None):
        """
        Run one time step of the trade_env's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this trade_env's state.

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

        bar_data = self.bar_quote.push()
        state = self.env_snapshot.state
        next_state = state_transition(action, state)
        current_reward = reward_calculator(next_state, bar_data)
        self.env_snapshot.action = action
        self.env_snapshot.state = next_state
        self.env_snapshot.reward += current_reward

        done = done_condition(self.env_snapshot.reward)
        step_info_parameters = {
            'observation': bar_data,
            'reward': self.env_snapshot.reward,
            'done': done,
            'info': dict()
        }
        step_info = StepInfo(**step_info_parameters)
        return step_info

    def reset(self):
        """
        Resets the state of the trade_env and returns an initial observation.

        Returns:
             observation(object): the initial observation of the space.
        """
        self.__dict__.update(self._init_setting)

    def render(self, mode='human'):
        """Renders the trade_env.

        The set of supported modes varies per trade_env. (And some
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
        """Sets the seed for this trade_env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

        Returns:
            list<bigint>: Returns the list of seeds used in this trade_env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        return

    @property
    def unwrapped(self):
        """Completely unwrap this trade_env.

        Returns:
            gym.Env: The base non-wrapped gym.Env instance
        """
        return self


__all__ = [
    'FuturesMarketEnv'
]
