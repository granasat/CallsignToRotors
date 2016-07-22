from converter import CallSignConverter,GPSConverter
import serial 
if __name__ == "__main__":
    c = CallSignConverter("EA5DOM-11")
    # c.getGPSPosition()
    auxi=c.getRotorsPosition()
    _az='%03d' % int(auxi[0])
    _el='%03d' % int(auxi[1])
    
    g=GPSConverter([37,10,47.05,"N",3,36,34.66,"W",10000])
    print g.getRotorsPosition()

    #conectar puerto serie de los rotores
    ser = serial.Serial(
        port=config.serial_port,
        baudrate=config.serial_baudrate,
        timeout=0,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    print "Intentando transmitir esta cadena: "+ 'W'+_az+' '+_el
    if ser.isOpen():
        ser.write(('W'+_az+' '+_el).encode())
        print("Go to: az: "+_az+", el: "+_el)
            
    else:
        print "Error Reading COM Port"