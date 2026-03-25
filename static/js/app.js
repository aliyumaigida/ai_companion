
let currentQuestion=""

// ----------------------
// AI Voice
// ----------------------
function speak(text){

window.speechSynthesis.cancel()

const speech=new SpeechSynthesisUtterance(text)

speech.lang="en-US"
speech.rate=1
speech.pitch=1

window.speechSynthesis.speak(speech)

}

// ----------------------
// Add Chat Bubble
// ----------------------
function addMessage(text,type){

const chat=document.getElementById("chat")

const msg=document.createElement("div")

msg.classList.add("message")
msg.classList.add(type)

msg.innerText=text

chat.appendChild(msg)

chat.scrollTop=chat.scrollHeight

}

// ----------------------
// AI Typing Animation
// ----------------------
function typeMessage(text,type){

const chat=document.getElementById("chat")

const msg=document.createElement("div")

msg.classList.add("message")
msg.classList.add(type)

chat.appendChild(msg)

let i=0

function typing(){

if(i<text.length){

msg.innerHTML+=text.charAt(i)

i++

chat.scrollTop=chat.scrollHeight

setTimeout(typing,25)

}

}

typing()

}

function showTyping() {
    const chat = document.getElementById("chat");

    // Remove existing typing if any
    const existing = document.getElementById("typing");
    if (existing) existing.remove();

    const typing = document.createElement("div");
    typing.classList.add("message", "ai");
    typing.id = "typing";

    // Create the spinner element
    const spinner = document.createElement("div");
    spinner.classList.add("ai-spinner");

    typing.appendChild(spinner);
    chat.appendChild(typing);
    chat.scrollTop = chat.scrollHeight;
}


function removeTyping(){

const typing=document.getElementById("typing")

if(typing){
typing.remove()
}

}

// ----------------------
// Start Tutor
// ----------------------
async function startTutor(){

const topic=document.getElementById("topic").value

const response=await fetch("/api/start/",{

method:"POST",

headers:{"Content-Type":"application/json"},

body:JSON.stringify({topic})

})

const data=await response.json()

currentQuestion=data.question

typeMessage(data.question,"ai")

speak(data.question)

}

// ----------------------
// Send Answer
// ----------------------
async function sendAnswer(){

const answer=document.getElementById("answer").value

if(answer==="") return

addMessage(answer,"user")

document.getElementById("answer").value=""

showTyping()

const response=await fetch("/api/answer/",{

method:"POST",

headers:{"Content-Type":"application/json"},

body:JSON.stringify({

question:currentQuestion,
answer:answer

})

})

removeTyping()

const data=await response.json()

if(data.end_session==="YES"){

const evalRes=await fetch("/api/evaluate/")

const result=await evalRes.json()

showChart(result)

speak("Session complete. Showing evaluation.")

}

else{

currentQuestion=data.question

typeMessage(data.question,"ai")

speak(data.question)

}

}

// ----------------------
// Voice Input
// ----------------------
function startVoiceInput(){

if(!('webkitSpeechRecognition' in window)){

alert("Speech recognition not supported in this browser")

return

}

const recognition=new webkitSpeechRecognition()

recognition.lang="en-US"

recognition.start()

recognition.onresult=function(event){

const text=event.results[0][0].transcript

document.getElementById("answer").value=text

}

}

// ----------------------
// Show Evaluation Scores
// ----------------------
function showChart(result){

const box = document.getElementById("chartBox")

box.innerHTML = "<h2>Final Evaluation</h2>"

for(const key in result){

const score = document.createElement("p")

score.innerHTML = `<strong>${key}</strong>: ${result[key]}`

box.appendChild(score)

}

}

// // ----------------------
// // Show Evaluation Chart
// // ----------------------
// // Show Evaluation Chart
// // ----------------------
// function showChart(result){

// const ctx=document.createElement("canvas")

// document.getElementById("chartBox").appendChild(ctx)

// const labels = Object.keys(result)

// const values = Object.values(result).map(v => parseInt(v.replace("%","")))

// new Chart(ctx,{

// type:"bar",

// data:{

// labels:labels,

// datasets:[{

// label:"Reasoning Score (%)",

// data:values,

// borderWidth:1

// }]

// },

// options:{

// scales:{

// y:{

// beginAtZero:true,

// max:100,

// ticks:{

// callback:function(value){

// return value + "%"

// }

// }

// }

// },

// plugins:{

// tooltip:{

// callbacks:{

// label:function(context){

// return context.raw + "%"

// }

// }

// }

// }

// }

// })

// }
