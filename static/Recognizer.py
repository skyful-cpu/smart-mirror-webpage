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

class Recognizer:

    # threshold를 인자로 받는 생성자
    def __init__(self, threshold):
        self.threshold = threshold
    
    # 인식된 음성과 명령어 간의 유사도를 계산해
    # 가장 높은 유사도의 명령어를 정답으로 간주
    def what_user_said(self, user_said):
    
        user_said = user_said.strip()
        user_said = user_said.replace(' ', '')
        
        # 100% 일치하는 명령어는 그대로 반환
        # 아닌 경우 유사도 비교
        for command in commands:
            if user_said == command:
                #print(f'recognizer, 100% match : {command}')
                return command
        
        # 100% 일치하지 않은 경우
        user_said_split = list(user_said)
        answer_candidate = []
        
        for index, command in enumerate(commands):
            command_split = list(command.replace(' ', ''))
            
            # 음절 단위로 자카드 유사도 계산
            union = set(command_split).union(user_said_split)
            intersection = set(command_split).intersection(user_said_split)
            jacad = len(intersection) / len(union)
            
            if jacad >= self.threshold:
                answer_candidate.append(index)
        
        if len(answer_candidate) == 0:
            print('no match')
            return
        else:
            #print(f'recognizer, not perfectly match : {commands[max(answer_candidate)]}')
            return commands[max(answer_candidate)]
