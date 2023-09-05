import numpy as np

class RoadSimulation:
    def __init__(self, time_limit, delta_t, a_max, delta, safety_dist):
        self.time_limit = time_limit

        self.pos = np.zeros((1,time_limit))
        self.acc = np.zeros((1,time_limit))
        self.spd = np.zeros((1,time_limit))
        self.delta_t = delta_t
        self.a_max = a_max
        self.delta = delta
        self.s_d = safety_dist

    def enter(self, a, t):
        if t != 0:
            new_agent = np.zeros((1,self.time_limit))
            self.pos = np.vstack((self.pos, new_agent))
            self.acc = np.vstack((self.acc, new_agent))
            self.spd = np.vstack((self.spd, new_agent))
        
        spd = np.random.uniform(low=8.33, high=11.11, size=1).item() # Entre 30 y 45 km/h
        self.pos[a,t] = 1
        self.spd[a,t] = spd
        self.acc[a,t] = 0

    def update(self, t):
        i = 0
        while i < len(self.pos[:,t]):
            # velocidad deseada v_0
            v_0 = 22.22
            if self.pos[i, t-1] > 13000:
                v_0 = 27.77
            
            v = self.spd[i, t-1]
            s = self.pos[i, t-1] - self.pos[i-1, t-1]
            
            self.pos[i, t] = self.pos[i, t-1] + self.spd[i, t-1] * self.delta_t
            self.spd[i, t] = max(0.0, v + self.acc[i, t-1] * self.delta_t)
            
            if i == 0 and t == 0:
                self.acc[i,t] = self.a_max
            else:
                if s == 0:
                    acc = 0
                else:
                    acc = self.a_max * (1- (v / v_0) ** self.delta - (self.s_d / s) ** 2)

                self.acc[i, t] = acc

            if i != 0:
                if self.pos[i-1,t] < self.pos[i,t]:
                    print("Choque de "+str(i)+" con "+str(i-1)+" en t="+str(t))

            i += 1

    def simulate(self):
        agents_enter = 0
        self.enter(agents_enter,0)
        t = 1
        agents_enter = 1

        while t < self.time_limit:
            self.update(t)
            p = np.random.random(size=1)
            # Con alguna proba entra un auto nuevo:
            if p > 0.5:
                self.enter(agents_enter, t)
                agents_enter += 1
            
            t += 1
    

