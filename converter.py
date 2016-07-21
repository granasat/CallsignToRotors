
class CallSignConverter:

    def __init__(self, cs):
        self.callsign = cs

    def getGPSPosition(self):
        self.callsign
        # Llamar con requests a aprs.fi con cs
        # pillar datos
        # sacar lat long el
        return [lat, lng, el]

    def getRotorsPosition(self):
        gpsPos = self.getGPSPosition()
        # calculos
        return [az, el]
