import math
import numpy as np

        
class plane:
    
    def __init__(self, components: list, offset: list) -> None:
        self.components = np.array(components)
        self.offset = offset
        
    def non_zero(self) -> int:
        if(self.components[0] != 0):
            return self.components[0]
        elif(self.components[1] != 0):
            return self.components[1]
        elif(self.components[2] != 0):
            return self.components[2]
    
        
class sphere:
    
    def __init__(self, o_n, coordinates, scale, colour, lighting, num) -> None:
        self.name = o_n
        self.coords = np.array(coordinates)
        
        self.scale = np.array(scale)
        
        self.colour = np.array(colour)
        
        self.lighting = np.array(lighting)
        
        self.n = num
    
    def get_normal(self, point: np.ndarray):
        return point - self.coords
    
class ray:
    
    def __init__(self, p, v) -> None:
        self.colour = np.zeros(3)
        self.is_dead = False
        self.t = 0
        self.point = np.array(p) 
        self.vector = np.array(v) 
    
    
    # does the computation to see if there is an intersection between 
    # current ray and sphere provided
    def does_intersect(self, obj: sphere):
        
        # make the transformed ray
        tr_point = ((self.point - obj.coords) / obj.scale)
        tr_vector = ((self.vector - obj.coords) / obj.scale) - tr_point
        tr = ray(tr_point, tr_vector)
        
        # calculate the discriminant
        t1 = np.power(np.dot(tr.point, tr.vector), 2)
        t2 = np.dot(tr.vector, tr.vector) * (np.dot(tr.point, tr.point) - 1)
        discr  = t1 - t2
        
        
        if(discr < 0):
            return None
        else:
            if(discr == 0):
                return None
            else:
                # calculate other terms if there are 2 intersections
                t1 = -(np.dot(tr.vector, tr.point) / np.dot(tr.vector, tr.vector))
                t2 = np.dot(tr.vector, tr.vector)
                
                # the t-value to plug into the transformed ray
                t_value =  np.minimum(t1 + (np.sqrt(discr) / t2), t1 - (np.sqrt(discr) / t2))
                
                
                # plug the t-value in and transform the point back
                return ((tr.point + t_value * tr.vector) * obj.scale + obj.coords)
            
            
            
            

class viewport:
    
    def __init__(self, n, l, r, b, t, res_x, res_y) -> None:
        self.near = n
        self.left = l
        self.right = r
        self.bottom = b
        self.top = t
        self.resx = int(res_x)
        self.resy = int(res_y)
        
class light:
    
    def __init__(self, name, coordinates, intensity) -> None:
        self.name = name
        
        self.coords = np.array(coordinates)
        
        self.intensity = np.array(intensity)
        
class canvas:
    
    def __init__(self, output, back, ambient) -> None:
        
        self.b_colour = np.array(back)
        
        self.ambient = np.array(ambient)
        
        self.output_name = output
