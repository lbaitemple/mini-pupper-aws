def parse_movement_string(movement_string):
    parts = movement_string.split(':')
    if len(parts) == 3:
        action = parts[0]
        value = float(parts[1])
        interval = float(parts[2])
        return {'action': action, 'value': value, 'interval': interval}
    else:
        raise ValueError("Invalid movement string format")

# Example usage:
movement_string = 'move_forward:0.3:0.5'
result = parse_movement_string(movement_string)
print(result)
