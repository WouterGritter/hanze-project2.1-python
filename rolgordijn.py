import serial


class Rolgordijn:
    def __init__(self, port):
        self.port = serial.Serial(port)
        self.yt = []
        self.yl = []
        self.error = 0
        ok_signal = self.read_raw(5)
        if ok_signal != 'OK':
            print(f'Warning! The OK signal for port {port} wasn\'t OK but {ok_signal}')
            raise Exception()

        print(f'{port} is ready!')

    def get_temperature(self):
        try:
            return int(self.get('T')) / 10.0
        except Exception:
            return None

    def get_light(self):
        try:
            return int(self.get('L'))
        except Exception:
            return None

    def get_distance(self):
        try:
            return int(self.get('D'))
        except Exception:
            return None

    def get_is_open(self):
        try:
            return self.get('S') == 'o'
        except Exception:
            return None

    def get_is_automatic(self):
        try:
            return self.get('A') == 'a'
        except Exception:
            return None

    def get_temperature_border(self):
        try:
            return int(self.get('t')) / 10.0
        except Exception:
            return None

    def get_light_border(self):
        try:
            return int(self.get('l'))
        except Exception:
            return None

    def get_open_distance_border(self):
        try:
            return int(self.get('o'))
        except Exception:
            return None

    def get_close_distance_border(self):
        try:
            return int(self.get('c'))
        except Exception:
            return None

    def set_is_open(self, is_open):
        try:
            return self.set('S', 'o' if is_open else 'c')
        except Exception:
            return False

    def set_is_automatic(self, is_automatic):
        try:
            return self.set('A', 'a' if is_automatic else 'm')
        except Exception:
            return False

    def set_temperature_border(self, temperature_border):
        try:
            return self.set('t', str(int(temperature_border * 10.0)))
        except Exception:
            return False

    def set_light_border(self, light_border):
        try:
            return self.set('l', str(int(light_border)))
        except Exception:
            return False

    def set_open_distance_border(self, open_distance_border):
        try:
            return self.set('o', str(int(open_distance_border)))
        except Exception:
            return False

    def set_close_distance_border(self, close_distance_border):
        try:
            return self.set('c', str(int(close_distance_border)))
        except Exception:
            return False

    def get(self, identifier):
        tries = 0
        while tries < 100:
            self.send_raw('G' + identifier)

            response = self.read_raw(0.25)
            if response[0] == identifier:
                return response[1::]

            tries += 1

        print(f'Warning! Could not execute get command after {tries} tries!')
        return None

    def set(self, identifier, value):
        tries = 0
        while tries < 100:
            self.send_raw('S' + identifier + value)

            response = self.read_raw(0.25)
            if response == identifier:
                return True

        print(f'Warning! Could not execute set command after {tries} tries!')
        return False

    def send_raw(self, command):
        self.port.write(('?' + command + '#').encode())

    def read_raw(self, timeout):
        self.port.timeout = timeout

        value = ''
        started = False

        while True:
            read = self.port.read(1)
            if len(read) == 0:
                return ''  # Timeout!

            try:
                x = read.decode()
            except UnicodeDecodeError:
                x = ' '

            if not started:
                if x == '?':
                    # Start!
                    started = True
            else:
                if x == '#':
                    # Stop!
                    break

                value += x

        return value
