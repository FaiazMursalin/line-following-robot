"""LFR controller."""


from controller import Robot


robot = Robot()


timestep = int(robot.getBasicTimeStep())

time_step=32
max_speed=3

left_motor = robot.getDevice('left wheel motor')
left_motor_2 = robot.getDevice('left wheel motor 2')

right_motor = robot.getDevice('right wheel motor')
right_motor_2 = robot.getDevice('right wheel motor 2')


left_motor.setPosition(float('inf'))
left_motor_2.setPosition(float('inf'))

right_motor.setPosition(float('inf'))
right_motor_2.setPosition(float('inf'))


left_motor.setVelocity(0.0)
left_motor_2.setVelocity(0.0)


right_motor.setVelocity(0.0)
right_motor_2.setVelocity(0.0)



right_ir=robot.getDevice('RIGHT')
right_ir.enable(time_step)
mid_ir=robot.getDevice('MID')
mid_ir.enable(time_step)
left_ir=robot.getDevice('LEFT')
left_ir.enable(time_step)



proportional=integral=derivative=last_propostional=error_value=0
sensor_average=sensor_sum=position=last_positon=0
last_error=0

# set_point=761.6905530832811
kp=0.5
ki=0
kd=0.15


def calc_turn(left_motor_speed, right_motor_speed):
    right_motor.setVelocity((right_motor_speed))
    right_motor_2.setVelocity((right_motor_speed))
    left_motor.setVelocity((left_motor_speed))
    left_motor_2.setVelocity((left_motor_speed))


while robot.step(timestep) != -1:
 
    right_ir_val=right_ir.getValue()
    mid_ir_val=mid_ir.getValue()
    left_ir_val=left_ir.getValue()
    sensors=[left_ir_val,mid_ir_val,right_ir_val]
    for i in range(3):
        if sensors[i]>700:
            sensors[i]=1
        else:
            sensors[i]=0
    sensor_average=0
    sensor_sum=0
    i=0
    sensor_calculator=[-100,0,100]#weight
    while i<3:
        sensor_sum=sensor_sum+(sensors[i]*sensor_calculator[i])
        
     
        i=i+1
    
    error=sensor_sum
    
    speed_control= kp*error+(ki/(error+last_error+1))+kd*(error-last_error)
    last_error=error
    left_motor_speed=max_speed+((speed_control/80)*5)
    right_motor_speed=max_speed-((speed_control/80)*5)
    calc_turn(left_motor_speed, right_motor_speed)
    
  
    
    
    print("left: {} mid: {} right:{}".format(sensors[0],sensors[1],sensors[2]))
    
    
    pass

