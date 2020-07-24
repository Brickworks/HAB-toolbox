STANDARD_GRAVITY = 9.80665  # [m/s^2] Standard acceleration from gravity (g0)
MEAN_EARTH_RADIUS = 6371007.2  # [m] mean radius of Earth


def gravity(altitude):
    ''' Acceleration due to gravity (m/s^2) as a function of altitude (m).
    
    Gravity is negative because it assumes positive up coordinate frame.
    '''
    return -STANDARD_GRAVITY * (
        MEAN_EARTH_RADIUS / (altitude + MEAN_EARTH_RADIUS)
        ) ** 2
