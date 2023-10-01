var closeError = document.querySelector(".closeError")
var errorDialogue = document.querySelector(".errorDialogue")
var body = document.querySelector(".body")

closeError.addEventListener("click",()=>{
    console.log("Hello Guys!")
    body.removeChild(errorDialogue)
})