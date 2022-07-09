from bluetooth import *

commands = [
    '불켜줘',
    '불꺼줘',
    '조명켜줘',
    '조명꺼줘',
    '가스잠가줘',
    '가스밸브잠가줘',
    '보일러켜줘',
    '보일러꺼줘',
    '창문열어줘',
    '창문닫아줘',
    '커튼쳐줘',
    '커튼걷어줘',
    '환풍기켜줘',
    '환풍기꺼줘',
    '스마트미러명령어'
]

# 각 IoT 기기에 사용된 블루투스 모듈의 MAC 주소
# 조명, 가스밸브, 보일러, 창문, 커튼, 환풍기 순으로 저장
mac = [
    '98:D3:31:FB:86:EE',
    '98:DA:60:01:C3:37'
    ]
    
iot = ['light', 'boiler', 'fan']

class IoT:
    
    # command를 인자로 받아와 클래스 생성
    def __init__(self, command=None):
        if command:
            self.command = command
        else:
            self.command = None
        
    # 최초 접속 시 IoT on / off 여부 확인
    def get_initial_state(self):
        socket = BluetoothSocket( RFCOMM )
        socket.connect((mac[0], 1))
        socket.send('i')
        
        data = ''
        idx = 0
        return_dict = {}
    
        while data is not 'q':
            byte_data = socket.recv(4096)
            data = byte_data.decode('utf-8')
            if data == ' ':
                continue
            if data == 'q':
                continue
            #print("Received: %s" %data)
            return_dict[iot[idx]] = data
            idx += 1
            
    
        socket.close()
        return return_dict
    
    # command에 따른 IoT 제어
    def control_iot(self):
        '''
        IoT 기기를 제어하는 함수
        어느 IoT를 제어했는 지에 대한 정보를 dictionary 형태로 반환
        '''
        
        if (self.command == commands[0]) or (self.command == commands[1]) or (self.command == commands[2]) or (self.command == commands[3]):
            result = self.control_light(self.command)
            return result
            
        elif (self.command == commands[4]) or (self.command == commands[5]):
            result = self.control_valve(self.command)
            return result
            
        elif (self.command == commands[6]) or (self.command == commands[7]):
            result = self.control_boiler(self.command)
            return result
            
        elif (self.command == commands[8]) or (self.command == commands[9]):
            result = self.control_window(self.command)
            return result
            
        elif (self.command == commands[12]) or (self.command == commands[13]):
            result = self.control_fan(self.command)
            return result
        
    # control light    
    def control_light(self, cmd):
        '''
        return : control results in dictionary
        
        cmd : smart mirror command
        '''
        print(f'command : {cmd}')
        
        if cmd == (commands[0] or commands[2]):
            # send 1 to turn on the light
            self.send_bluetooth(mac[0], '1')
            return {'light' : 'on'}
            
        else:
            # send 0 to turn off the light
            self.send_bluetooth(mac[0], '0')
            return {'light' : 'off'}

    # control gas valve   
    def control_valve(self, cmd):
        # send 0 to close the valve
        self.send_bluetooth(mac[1], '0')

    # control boiler // 블루투스 모듈이 부족해서 지금은 LED에 쓰는 모듈이랑 같이 사용  
    def control_boiler(self, cmd):
        print(f'command : {cmd}')
        
        if cmd == commands[6]:
            # send 3 to turn on the boiler
            self.send_bluetooth(mac[0], '3')
            return {'boiler' : 'on'}
        else:
            # send 2 to turn off the boiler
            self.send_bluetooth(mac[0], '2')
            return {'boiler' : 'off'}
        
        print('Boiler control success')

    # control window   
    def control_window(self, cmd):
        pass

    # control curtain   
    def control_curtain(self, cmd):
        pass

    # control fan   
    def control_fan(self, cmd):
        print(f'command : {cmd}')
        
        if cmd == commands[12]:
            # send 3 to turn on the boiler
            self.send_bluetooth(mac[0], '5')
            return {'fan' : 'on'}
        else:
            # send 2 to turn off the boiler
            self.send_bluetooth(mac[0], '4')
            return {'fan' : 'off'}
    
    # connect IoT via bluetooth
    def send_bluetooth(self, mac, msg):
        
        # 블루투스 통신을 위한 소켓 객체을 만들고 지정한 MAC 주소로 연결
        socket = BluetoothSocket( RFCOMM )
        socket.connect((mac, 1))
        
        # 음성 인식 결과에 따라 다른 메시지를 아두이노로 전송
        socket.send(msg)

        socket.close()