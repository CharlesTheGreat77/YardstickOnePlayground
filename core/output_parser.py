#
# output_parser is used to deal with the output/input parsing 
# to a file from signals previously or currently captured signals
#

def parse_captured_file(input_file):
    '''
    Function to get frequency, modulation, deviation, blocksize, and signals
    from captured file
    type var: string [input_file]
    
    returns:
    type var: int [frequency]
    type var: string [modulation]
    type var: int [deviation]
    type var: int [baudrate]
    type var: int [blocksize]
    type var: array [signals]
    '''
    payloads = []
    with open(input_file, 'r') as file:
        for line in file:
            if 'Frequency:' in line:
                frequency = line.split(':')[1].strip()
            elif 'Modulation:' in line:
                modulation = line.split(':')[1].strip()
            elif 'Deviation:' in line:
                deviation = line.split(':')[1].strip()
            elif 'Blocksize:' in line:
                bs = line.split(':')[1].strip()
            elif 'Baudrate:' in line:
                baudrate = line.split(':')[1].strip()
            elif 'Payload:' in line:
                payload = line.split(':')[1].strip()
                payloads.append(payload)
    return int(frequency), modulation, int(deviation), int(baudrate), int(bs), payloads


def save_signal_output(output_file, frequency, modulation, deviation, baudrate, blocksize, signals):
    '''
    Function to save signals and ys1 configuration to output file
    with .cap extension
    type var: string [output_file]
    type var: int [frequency]
    type var: string [modulation]
    type var: int [deviation]
    type var: int [baudrate]
    type var: int [blocksize]
    type var: array [signals]
    '''
    print(f'[*] Saving signals to {output_file}')
    with open(f'{output_file}.cap', 'w') as file:
            file.write(f'Frequency: {frequency}\nModulation: {modulation}\nDeviation: {deviation}\nBaudrate: {baudrate}\nBlocksize: {blocksize}\n')
            for signal in signals:
                file.write(f'Payload: {signal}\n')