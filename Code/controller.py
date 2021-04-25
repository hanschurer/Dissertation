import sys, os
import math
import itertools
import json
import time
from vehicle import Driver


sensorMax = 1000

driver = Driver()


for i in range(driver.getNumberOfDevices()):
    device = driver.getDeviceByIndex(i)
    print(i,device.getName(),type(device))


refresh = 50

printCounter=0

camera_enabled=False

#camera
camera_name= "camera"
camera_finder = driver.getDevice(camera_name)
camera_finder.enable(refresh)

if camera_finder.hasRecognition():
    camera_finder.recognitionEnable(refresh)
    camera_enabled= True

#ineritial 
inertial_name = "inertial unit"
inertial = driver.getDevice(inertial_name)
inertial.enable(refresh)

targets = ( ( -60,  0,  88), \

             )
targetId = 0

folder = "images"
annotations_folder="annotations"
maxImages = 50

def local_point( point, origin, heading ):
    relative = [ p-o for p, o in zip(point,origin) ]
    return relative[0]*math.cos(-heading) + relative[2]*math.sin(-heading), \
           relative[1], \
           relative[2]*math.cos(-heading) - relative[0]*math.sin(-heading)


def save_annotated_image( camera_finder, position, heading ):
    filename = str(int(time.time()*1000))

    #camera.saveImage( os.path.join( folder, "images", filename+".png" ), 100 )
    #rangeFinder.saveImage( os.path.join( folder, "depth", filename+".jpg" ), 100 )
    camera_finder.saveImage(os.path.join(folder,filename+".png"),100)

    positions = ( ( *object.get_position_on_image(), *object.get_size_on_image() )

                  for object in camera_finder.getRecognitionObjects()
                  if "advertising board" in object.get_model().decode())

    filtered = ( (x, y, w, h) for x, y, w, h in positions
                  if y<=510 and x>10 and x <camera_finder.getWidth()-10)
    
    for object in camera_finder.getRecognitionObjects():
        print(object.get_model().decode())
                  

    
    width = camera_finder.getWidth()
    height = camera_finder.getHeight()
    scaled = ( (x/width, y/height, w/width, h/height) for x, y, w, h in filtered )

    
    with open(os.path.join("D:\\HOME\\Informatics\\controllers\\test00",folder,filename+".txt" ), "w" ) as f:
        for object in scaled:
            print( "0 {} {} {} {}".format( *object ), file=f )
    

while driver.step() != -1:     
        
    # get current position
    position = driver.getSelf().getPosition()
    heading = inertial.getRollPitchYaw()[2]
    if heading == float('nan'): continue

    # get next target
    target = targets[targetId% len(targets)]
    localTarget = local_point( target, position, heading )
   
    print( "target> {:.3f} {:.3f} {:.3f}".format(*target) )
       
    print( "local > {:.3f} {:.3f} {:.3f}".format(*localTarget) )
 
    localHeading = math.atan2( localTarget[0], localTarget[2] )
    
    while localHeading > math.pi: localHeading -= math.pi*2
    while localHeading < -math.pi: localHeading += math.pi*2
    
    print( "head  > {:.3f}".format(math.degrees(localHeading)) )
    
    localHeading = math.atan2(localTarget[0],localTarget[2])

    distance = math.sqrt( abs(localTarget[0]**2) + abs(localTarget[2]**2) )
    if distance <1:
        targetId +=1

    print( "dist  > {:.3f}".format(distance) )

       
    driver.setSteeringAngle( -localHeading )
    driver.setCruisingSpeed( 6 )

    save_annotated_image(camera_finder,position, heading )
    
        
sys.exit()
 