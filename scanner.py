#DEVELOPED BY <PRIYANSHUL SHARMA>
#WEBPAGE PRIYANSHUL.is-a.dev


from pyfingerprint.pyfingerprint import PyFingerprint
import pyfingerprint
import json
import os
try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)

def register_fingerprint():
    name = input('Enter your name: ')
    print('Waiting for finger...')
    while ( f.readImage() == False ):
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()

    positionNumber = result[0]

    if ( positionNumber == -1 ):
        print('Registering new fingerprint...')
        f.downloadCharacteristics(0x01, 0x05)
        characteristics = f.downloadCharacteristics(0x05)
        characteristics_str = ''.join(map(str, characteristics))

    
        data = {
            'name': name,
            'fingerprint': characteristics_str
        }

        with open(f'{name}.json', 'w') as f:
            json.dump(data, f)

        print('Fingerprint registered successfully!')
    else:
        print('Fingerprint already exists at position #' + str(positionNumber))

def detect_fingerprint():
    try:
        print('Waiting for finger...')
        while ( f.readImage() == False ):
            pass

        f.convertImage(0x01)

        result = f.searchTemplate()

        positionNumber = result[0]

        if ( positionNumber == -1 ):
            print('No match found!')
        else:
            print('Fingerprint found at position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

def load_fingerprints():
    fingerprints = {}
    for filename in os.listdir():
        if filename.endswith('.json'):
            with open(filename, 'r') as f:
                data = json.load(f)
                fingerprints[data['name']] = data['fingerprint']
    return fingerprints

def verify_fingerprint():
    fingerprints = load_fingerprints()
    print('Waiting for finger...')
    while ( f.readImage() == False ):
        pass

    f.convertImage(0x01)
    characteristics = f.downloadCharacteristics(0x05)
    characteristics_str = ''.join(map(str, characteristics))

    for name, fingerprint in fingerprints.items():
        if characteristics_str == fingerprint:
            print(f'Fingerprint matches {name}!')
            return

    print('No match found!')

while True:
    print('1. Register fingerprint')
    print('2. Detect fingerprint')
    print('3. Verify fingerprint')
    print('4. Exit')
    choice = input('Enter your choice: ')

    if choice == '1':
        register_fingerprint()
    elif choice == '2':
        detect_fingerprint()
    elif choice == '3':
        verify_fingerprint()
    elif choice == '4':
        break
    else:
        print('Invalid choice. Please try again.')
