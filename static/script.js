// IoT 종류
IoTs = ['light', 'boiler', 'fan'];
    
// 시간을 표시하는 함수
function displayClock() {
    var clock = document.getElementById("time");
    var todayDay = document.getElementById("day");
    var todayDate = document.getElementById("date");

    // 요일 배열
    var dayInString = ['일', '월', '화', '수', '목', '금', '토'];

    // 현재 시간을 불러온다
    var currentDate = new Date();

    // 연도 정보를 저장
    var year = currentDate.getFullYear();
    // 달 정보를 저장 (getMonth() 함수는 0~11을 반환하므로 끝에 1을 더해준다)
    var month = currentDate.getMonth() + 1;
    // 일 정보를 저장
    var date = currentDate.getDate();
    // 요일 정보를 저장 ()
    var day = currentDate.getDay();
    // 시 정보를 저장
    var hour = currentDate.getHours();
    // 분 정보 저장
    var min = currentDate.getMinutes();
    // 초 정보 저장
    var sec = currentDate.getSeconds();

    clock.innerHTML = `${hour<10 ? `0${hour}`:hour}:${min<10 ? `0${min}`:min}:${sec<10 ? `0${sec}`:sec}`;
    todayDay.innerHTML = `${dayInString[day]}요일`;
    todayDate.innerHTML = `${year}년 ${month}월 ${date}일`;
}

// setInterval() 함수로 1초마다 시간을 갱신
function init() {
    setInterval(displayClock, 1000);
}

var startAnnyang = document.getElementById('annyang-start');
var pauseAnnyang = document.getElementById('annyang-pause');
var result = document.getElementsByClassName('result')[0];

startAnnyang.addEventListener('click', function() {
    if (annyang) {
        /*// set commands
        var commands = {
            '조명 켜줘.' : function() {
                result.innerHTML = '조명을 켰습니다';
            },
            '불꺼' : function() {
                result.innerHTML = '조명을 껐습니다';
            }
        };*/
    
        //annyang.addCommands(commands);
        //annyang.debug();
        annyang.setLanguage('ko');
        annyang.start();
        console.log('annyang started');

        /*
        // 5초 동안 녹음하고 annyang을 끈다.
        setTimeout(function() {
            annyang.pause();
            console.log('annyang stopped');
            result.innerHTML = '';
        }, 5000);*/
    }
});

pauseAnnyang.addEventListener('click', function() {
    annyang.pause();
    console.log('annyang stopped');
});

/*
annyang.addCallback('resultMatch', function(userSaid, commandText, phrases) {
    console.log(userSaid); // sample output: 'hello'
    console.log(commandText); // sample output: 'hello (there)'
    console.log(phrases); // sample output: ['hello', 'halo', 'yellow', 'polo', 'hello kitty']
});*/

annyang.addCallback('result', function(userSaid) {
    //console.log(`You said : ${userSaid}`);
    result.innerHTML = userSaid;
    setTimeout(function() {
        result.innerHTML = ''
    }, 3000);
	
	// make json and send it to server
    const json_dict = {'speech_recog_result': userSaid};
    const stringify = JSON.stringify(json_dict);
	
	
	// 음성 인식 결과를 서버로 전송
    $.ajax({
        url: '/speech_recog',
        type: 'POST',
        contentType: 'application/json',
        //data: JSON.stringify(stringify),
		data: stringify,
        success: function(json_data) {
            console.log(json_data);
			changeIotUi(json_data);
        }
    });
	
	/*
	// 새로운 버전
	$.ajax({
		type: 'GET',
		url: '/post',
		contentType: 'application/json',
		data: stringify
	}).done(function(json_data) {
		console.log('success');
		console.log(json_data);
	}).fail(function(xhr, status, error) {
		console.log('error');
	});*/
	
	/*
	// 서버에서 IoT 제어 결과를 받아옴
	setTimeout(function() {
		$.ajax({
			url: '/post',
			type: 'GET',
			dataType: 'json',
			success: function(reply) {
				console.log(reply);
			}
		});
	}, 7000);*/
});

/////////////////////////////////// 최초 접속 시 IoT 상태 표시 ///////////////////////////////////

function setInitialIotStatus() {
    $.ajax({
        type: 'GET',
        url: '/initial_setting',
        contentType: 'application/json'
    }).done(function(json_data) {
        changeIotUi(json_data);
		console.log(json_data);
    }).fail(function(xhr, status, error) {
        console.log('error');
    });
}

/////////////////////////////////// 최초 접속 시 IoT 상태 표시 ///////////////////////////////////

function changeIotUi(json_data) {
    for (var key in json_data) {
        if (IoTs.includes(key)) {
            var ui = document.getElementById(key);
            
            if (json_data[key] === 'on') {
                ui.style.color = '#ffffff';
            }
            else {
                ui.style.color = '#000000';
            }
        }
    }
}

// 시간 표시 시작
init();

// 최초 접속 시 IoT 상태 UI 갱신
setInitialIotStatus();
