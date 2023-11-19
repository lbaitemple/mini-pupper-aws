def parse_movement_string(movement_string):
    parts = movement_string.split(':')
    value = parts[1] if len(parts) > 1 and parts[1].lower() != 'off' else False
    interval = parts[2] if len(parts) > 2 else None

    action = parts[0]
    
    if action == 'music':
        value = True if value and value.lower() == 'on' else False

    elif action == 'volume':
        value = True if value and value.lower() == 'on' else False
        interval = int(parts[2]) 
    else:
        tm= value
        value = float(interval)
        interval = float(tm)
        
        
        
    if len(parts) == 3 or len(parts) == 2:
        action = parts[0]
        return {'action': action, 'value': interval, 'interval': value}
    else:
        raise ValueError("Invalid movement string format")


def enhanced_parse_movement_string(movement_string):
    parts = movement_string.split(':')
    value = parts[1] if len(parts) > 1 and parts[1].lower() != 'off' else "off"
    interval = parts[2] if len(parts) > 2 else None

    action = parts[0]
    
    if action == 'music':
        if value.lower() == 'on' or value.lower() == 'off':
            interval = False if value and value.lower() == 'off' else True  
        else:
            interval = float(interval)

    elif action == 'volume':
        interval = True if value and value.lower() == 'on' else False
        value = int(parts[2]) 
    else:
        tm= value
        value = float(value)
        interval = float(interval)
        
        
        
    if len(parts) == 3 or len(parts) == 2:
        action = parts[0]
        return {'action': action, 'value': value, 'interval': interval}
    else:
        raise ValueError("Invalid movement string format")
        
# Example usage:
movement_string = 'look_up:-0.3:0.5'
result = enhanced_parse_movement_string(movement_string)
print(result)

command2 = 'music:robot1.wav:6.0'
result= enhanced_parse_movement_string(command2)
print(result)
command2 = 'look_up:-0.3:0.5'
result= enhanced_parse_movement_string(command2)
print(result)
command3 = 'volume:on:100'
result= enhanced_parse_movement_string(command3)
print(result)