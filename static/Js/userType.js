groupName_input = document.getElementById("groupName-inp")
success_outlined = document.getElementById("success-outlined")
danger_outlined = document.getElementById("danger-outlined")
warningNormalUserAlert = document.getElementById("warningNormalUserAlert")

danger_outlined.addEventListener('click',function(e){
    groupName_input.setAttribute("disabled",'')
    groupName_input.setAttribute("readonly",'')
    if(warningNormalUserAlert.classList.contains("d-none")){
        warningNormalUserAlert.classList.add("d-block")
        warningNormalUserAlert.classList.remove("d-none")
    }

})
success_outlined.addEventListener('click',function(e){
    groupName_input.removeAttribute("disabled",'')
    groupName_input.removeAttribute("readonly",'')
    if(warningNormalUserAlert.classList.contains("d-block")){
        warningNormalUserAlert.classList.add("d-none")
        warningNormalUserAlert.classList.remove("d-block")
    }
})
