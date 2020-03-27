"""
The parameter classes wrap controller parameters.
The fields are wrapped into properties in order to allow transparent usage of the MutableFloat wrapper

"""

from typing import Tuple, Union

from gym_microgrid.agents.util import MutableFloat


class FilterParams:
    """
    Defines Filter Parameters
    
    """

    def __init__(self, gain: Union[MutableFloat, float], tau: Union[MutableFloat, float]):
        self._gain = gain
        self._tau = tau

    @property
    def gain(self):
        return float(self._gain)

    @property
    def tau(self):
        return float(self._tau)


class DroopParams(FilterParams):
    """
    Defines Droop Parameters needed for the droop-controller
    """

    def __init__(self, gain: Union[MutableFloat, float], tau: Union[MutableFloat, float], nom_value: float = 0):
        """
        :param gain: The droop gain
        :param tau: The first order time constant [s]
        :param nom_value: An offset to add to the output of the droop
        
        EG for a P-f droop controller (for voltage forming inverter)
        Inverter of 10kW, droop of 10% , timeConstant of 1 sec, 50Hz
            Droop = gain = 1000 [Watt/Hz]
            tau = 1
            nomValue = 50 [Hz]
        """
        super().__init__(gain, tau)
        self.nom_val = nom_value

    @property
    def gain(self):
        if float(self._gain) != 0:
            return 1 / float(self._gain)
        return 0


class InverseDroopParams(DroopParams):
    """
    Implements a basic P,f droop controller
    """

    def __init__(self, droop: Union[MutableFloat, float], tau: Union[MutableFloat, float], nom_value: float = 0,
                 tau_filt: Union[MutableFloat, float] = 0):
        """
        :param droop: The droop gain
        :param tau: The first order time constant [s]
        :param nom_value: An offset to add to the output of the droop
        :param tau_filt: timeresolution for filter
        
        EG for a P-f droop controller (for voltage forming inverter)
        Inverter of 10kW, droop of 10% , timeConstant of 1 sec, 50Hz
            Droop = 1000 [Watt/Hz]
            tau = 1
            nomValue = 50 [Hz]
        """

        super().__init__(droop, tau, nom_value)
        self.derivativeFiltParams = FilterParams(1, tau_filt)


class PI_params:
    """
    The params for a basic PI Controller
    All fields are represented by properties to allow passing MutableFloats
    """

    def __init__(self, kP: Union[MutableFloat, float], kI: Union[MutableFloat, float],
                 limits: Union[Tuple[MutableFloat, MutableFloat], Tuple[float, float]], kB: float = 1):
        self._kP = kP
        self._kI = kI
        self._limits = limits
        self._kB = kB

    @property
    def kP(self):
        return float(self._kP)

    @property
    def kI(self):
        return float(self._kI)

    @property
    def limits(self):
        return [float(l) for l in self._limits]

    @property
    def kB(self):
        return float(self._kB)


class PLLParams(PI_params):
    """
    The params for a basic PI Controller
    """

    def __init__(self, kP: Union[MutableFloat, float], kI: Union[MutableFloat, float],
                 limits: Union[Tuple[MutableFloat, MutableFloat], Tuple[float, float]],
                 kB: Union[MutableFloat, float] = 1, f_nom: float = 0, theta_0: float = 0):
        super().__init__(kP, kI, limits, kB)
        self._f_nom = f_nom
        self._theta_0 = theta_0

    @property
    def f_nom(self):
        return float(self._f_nom)

    @property
    def theta_0(self):
        return float(self._theta_0)
