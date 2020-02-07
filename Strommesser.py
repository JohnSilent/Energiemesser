import time
import minimalmodbus


class Resource_Monitor:
    def __init__(self):
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 0.2
        self.instrument.mode = minimalmodbus.MODE_RTU
        self.data = {}
        self.input_register = {"Voltage": {
            "port": 0, "digits": 2, "Unit": "V", "use": True},
            "Ampere":
                {"port": 6, "digits": 2, "Unit": "A", "use": True},
            "Wirkleistung":
                {"port": 12, "digits": 2, "Unit": "W", "use": True},
            "Scheinleistung":
                {"port": 18, "digits": 2, "Unit": "VA", "use": False},
            "Blindleistung":
                {"port": 24, "digits": 2, "Unit": "VAr", "use": False},
            "Leistungsfaktor":
                {"port": 30, "digits": 2, "Unit": "", "use": False},
            "Phasenwinkel":
                {"port": 36, "digits": 2, "Unit": "Grad", "use": False},
            "Frequenz":
                {"port": 70, "digits": 2, "Unit": "Hz", "use": True},
            "ImportActiveEnergy":
                {"port": 72, "digits": 2, "Unit": "kWh", "use": False},
            "ExportActiveEnergy":
                {"port": 74, "digits": 2, "Unit": "kWh", "use": False},
            "ImportReactEnergy":
                {"port": 76, "digits": 2, "Unit": "kVArh", "use": False},
            "ExportReactEnergy":
                {"port": 78, "digits": 2, "Unit": "kVArh", "use": False},
            "TotalSystemPowerDemand":
                {"port": 84, "digits": 2, "Unit": "W", "use": False},
            "MaxTotalSystemPowerDemand":
                {"port": 86, "digits": 2, "Unit": "W", "use": True},
            "CurrentSystemPositivePowerDemand":
                {"port": 88, "digits": 2, "Unit": "W", "use": False},
            "MaximumSystemPositivePowerDemand":
                {"port": 90, "digits": 2, "Unit": "W", "use": False},
            "CurrentSystemReversePowerDemand":
                {"port": 92, "digits": 2, "Unit": "W", "use": False},
            "MaximumSystemReversePowerDemand":
                {"port": 258, "digits": 2, "Unit": "W", "use": False},
            "CurrentDemand":
                {"port": 258, "digits": 2, "Unit": "A", "use": False},
            "MaximumCurrentDemand":
                {"port": 264, "digits": 2, "Unit": "A", "use": True},
            "TotalActiveEnergy":
                {"port": 342, "digits": 2, "Unit": "kWh", "use": True},
            "TotalReactiveEnergy":
                {"port": 344, "digits": 2, "Unit": "kVArh", "use": False},
            "CurrentResettableTotalActiveEnergy":
                {"port": 384, "digits": 2, "Unit": "kWh", "use": False},
            "CurrentResettableTotalReactiveEnergy":
                {"port": 386, "digits": 2, "Unit": "kVArh", "use": False}
        }

    def read_input_values(self, input_register_keys=None):
        """
        Read all in self.input_register defined data points and stored the result as float value
        into self.data dictionary
        :return: self.data dictionary
        """

        if input_register_keys is None:
            input_register_keys = self.get_input_keys()
        if self.instrument is not None:
            for key in input_register_keys:
                
                if self.input_register[key]["use"] is True:
                    fehler = 0
                    while True:  # Anzahl der Versuche
                        try:
                            messwert = self.instrument.read_float(functioncode=4,  # fix (!) for this model
                                                                  registeraddress=self.input_register[key]["port"],
                                                                  number_of_registers=self.input_register[key][
                                                                      "digits"])
                        except OSError:
                            fehler += 1
                            print("Kommunikationserror Nr. {}".format(fehler))
                            if fehler > 5:  # Anzahl der Versuche
                                raise OSError
                        else:
                            break

                    if messwert is None:
                        print("Value '{}' not available".format(key))
                    else:
                        # TODO: messwertrunden abhängig des Registers machen
                        self.data[key] = round(messwert, 4)
                    print("Value '{}' = '{}' '{}'".format(key, self.data[key],self.input_register[key]["Unit"]))
                else:
                    #print("Value '{}' not used!".format(key))
                    pass

        else:
            err_msg = "No instrument available!"
            print(err_msg)
            return None

        return self.data


    def get_input_keys(self):
        """
        Hilfsmethode zur Erstellung der Intervallklassen
        :return:
        """
        input_register_keys = [key for key in self.input_register]
        return input_register_keys


if __name__ == '__main__':
    try:
        while True:
            read_sens = Resource_Monitor()
            read_sens.read_input_values()
            time.sleep(5)

    except KeyboardInterrupt:
        print("Beendet durch Benutzer")