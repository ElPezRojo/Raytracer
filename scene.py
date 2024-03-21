import objects
class scene:
    def __init__(self, l, o, v, c) -> None:
        self.lights = l
        self.object_list = o
        self.viewport = v
        self.canvas = c

    # reads in the file provided, and stores the values in 
    # its instance variables (lights, object_list, viewport, canvas)
    @staticmethod
    def read_file(fn):
        
        lights = []
        object_list = []
        viewport = None
        canvas = None
        
        back = []
        ambient = []
        output = ""
        
        f = open(fn, "r")
        viewport_params = {}
        for x in range(5):
            line = f.readline().split()
            viewport_params[line[0]] = int(line[1])
        line = f.readline().split()
        viewport_params["RESX"] = line[1]
        viewport_params["RESY"] = line[2]
        viewport = objects.viewport(
            viewport_params["NEAR"], viewport_params["LEFT"], viewport_params["RIGHT"], viewport_params["BOTTOM"],
            viewport_params["TOP"], viewport_params["RESX"], viewport_params["RESY"]
            )
        
                
        for l in f.readlines():
            print
            a = l.split()
            
            # if the next object is a sphere
            if(a[0] == "SPHERE"):
                x = 2
                while x < len(a):
                    a[x] = float(a[x])
                    x+=1 
                obj = objects.sphere(a[1], [a[2], a[3], a[4]], [a[5], a[6], a[7]], [a[8], a[9], a[10]], [a[11], a[12], a[13], a[14]], a[15])
                object_list.append(obj)
            
            # if the next object is a light
            elif(a[0] == "LIGHT"):
                x = 2
                while x < len(a):
                    a[x] = float(a[x])
                    x+=1
                light = objects.light(a[1], [a[2], a[3], a[4]], [a[5], a[6], a[7]])
                lights.append(light)
                
            # ETC
            elif(a[0] == "BACK"):
                x = 1
                while x < len(a):
                    a[x] = float(a[x])
                    x+=1
                back = [a[1], a[2], a[3]]
            
            # ETC
            elif (a[0] == "AMBIENT"):
                x = 1
                while x < len(a):
                    a[x] = float(a[x])
                    x+=1
                ambient = [a[1], a[2], a[3]]
            elif (a[0] == "OUTPUT"):
                output = a[1]
        canvas = objects.canvas(output, back, ambient)
        return lights, object_list, viewport, canvas
                
        
