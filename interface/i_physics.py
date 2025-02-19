import glm



class IPhysics:
    def __init__(self, mass=0.0, velocity=glm.vec3(0.0, 0.0, 0.0), acceleration=glm.vec3(0.0, 0.0, 0.0)):
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration

    def update(self, delta_time: float = 0.0):
        """Update the physics state based on the elapsed time."""
        # self.velocity += self.acceleration * dt
        # self.position += self.velocity * dt
        raise NotImplementedError
