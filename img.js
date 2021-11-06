const dateBox = document.querySelector(".date_box");
// querySelector : css 선택자 가져오기, 클래스는 '.', id는 '#'
const timeBox = document.querySelector(".time_box");
const timeTitle = timeBox.querySelector("h2");
const dateTitle = dateBox.querySelector("h2");

function getTime() {
  const today = new Date();

  let year = today.getFullYear(); // 년도
  let month = today.getMonth() + 1; // 월
  let date = today.getDate(); // 날짜

  const minutes = today.getMinutes();
  const hours = today.getHours();
  const seconds = today.getSeconds();
  timeTitle.innerText = `${hours < 10 ? `0${hours}` : hours}:${
    minutes < 10 ? `0${minutes}` : minutes
  }:${seconds < 10 ? `0${seconds}` : seconds}`;
  dateTitle.innerText = `🗓${year}/${month < 10 ? `0${month}` : month}/${
    date < 10 ? `0${date}` : date
  }🗓`;
}

function audio() {
  const date_audio = new Date();

  let minutes_audio = date_audio.getMinutes();
  let seconds_audio = date_audio.getSeconds();
  // 55분에 time_5 실행
  if (minutes_audio == 55) {
    if (seconds_audio == 00) {
      var audio = new Audio("time_5.mp3")
      audio.play();
    }
  }
  // 59분에 time_1 실행
  if (minutes_audio == 59) {
    if (seconds_audio == 00) {
      var audio = new Audio("time_1.mp3")
      audio.play();
    }
  }
}

function selectParamsFirst() {
  clearInterval(attend_pa);
  // 변수를 만들어서 그 변수로 멈춤 -> setInterval를 멈춤
  load_name(params1);
  t_attend(params1);
  var attend_pa = setInterval(t_attend, 1000)
  // 1초마다 t_attend 함수를 계속 호출
}

function selectParamsSecond() {
  clearInterval(attend_pa);
  load_name(params2);
  t_attend(params2);
  var attend_pa = setInterval(t_attend, 1000)
}

function selectParamsThird() {
  clearInterval(attend_pa);
  load_name(params3);
  t_attend(params3);
  var attend_pa = setInterval(t_attend, 1000)
}

function selectParamsFourth() {
  clearInterval(attend_pa);
  load_name(params4);
  t_attend(params4);
  var attend_pa = setInterval(t_attend, 1000)
}

function selectParamsFifth() {
  clearInterval(attend_pa);
  load_name(params5);
  t_attend(params5);
  var attend_pa = setInterval(t_attend, 1000)
}

function selectParamsSixth() {
  clearInterval(attend_pa);
  load_name(params6);
  t_attend(params6);
  var attend_pa = setInterval(t_attend, 1000)
}

function load_name(params) {
  // params : 매개변수
  for (var i in params) {
    num.push(params[i].seatNum);
    stu.push(params[i].name);
    time.push(params[i].attendTime);
    attend.push(params[i].attend);
    for (i = 0; i < stu.length; i++) {
      for (j = 0; j < stu.length; j++) {
        if (params[i].seatNum == params[j].seatNum) {
          // 출석순서와 상관없이 seatNum로 읽어서 같을 때 조건문 실행
          time[i] = params[i].attendTime.replace(/[^0-9]/g, "");
          // 숫자는 놔두고, 나머지의 모든 문자는 지우기
          hourTime[j] = time[i].substr(0, 2);
          // 0번부터 2개만 잘라서 시간 추출
          minuteTime[j] = time[i].substr(2, 2);
        }
      }
    }
  }
}


function t_attend(params) {
  var arr = [];
  for (let i = 0; i < stu.length; i++) {
  
    // id가 1번부터 학생수만큼 배열에 넣기

    for (let j = 0; j < 26; j++) {
      arr[j] = document.getElementById(j + 1);
      if (arr[j].id == num[i]) {
        // 출석 순서와 상관없이 지정좌석일 때, 좌석에 이름을 넣기
        arr[j].innerText = stu[i];

        if(params[i].runOut == 0){
          if (00 < minuteTime[i] && minuteTime[i] < 11) {
            arr[j].style.backgroundColor = "blue";
            params[i].attend = 2;
            // 00분 초과 11분 미만일 때, 둘 다 포함일때
          } else if ((10 < minuteTime[i] && minuteTime[i] < 50 ) || (hourTime[i] == 0)) {
            arr[j].style.backgroundColor = "red";
            params[i].attend = 0;
            // 10분 초과거나 50분 미만일 때
          } else if (49 < minuteTime[i] || minuteTime[i] == 00) {
            arr[j].style.backgroundColor = "green";
            params[i].attend = 1;
            // 49분 초과이거나, 00분일 때
          }
        }
        else {
          arr[j].style.backgroundColor = "red";
          params[i].attend = 3;
        }
      }
    }
    
  }
  countAttend(params)
}

function countAttend(params) {
  for (i = 0; i < stu.length; i++) {
    if (params[i].attend == 1) {
      attendanceCount++;
    }
    if (params[i].attend == 0) {
      absenceCount++;
    }
    if (params[i].attend == 2) {
      lateCount++;
    }
    if (params[i].attend == 3) {
      runCount++;
    }
  }
  document.getElementById('absence').innerHTML = "결석 학생수 : " + absenceCount;
  document.getElementById('attendance').innerHTML = "출석 학생수 : " + attendanceCount;
  document.getElementById('late').innerHTML = "지각 학생수 : " + lateCount;
  document.getElementById('run').innerHTML = "도망 학생수 : " + runCount;
}

num = new Array;
stu = new Array;
time = new Array;
attend = new Array;
out = new Array;

var lateCount = 0;
var attendanceCount = 0;
var absenceCount = 0;
var runCount = 0;

hourTime = new Array;
minuteTime = new Array;

getTime();
setInterval(getTime, 1000);
// 1초마다 현재시간 갱신

audio();
setInterval(audio, 1000);
// 1초마다 현재시간에 맞춰서 오디오