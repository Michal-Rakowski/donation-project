document.addEventListener("DOMContentLoaded", function(){
    let button = document.querySelector("#first-step");
    let checkBoxes = document.querySelectorAll("span.checkbox")
    button.disabled = true
    for (let i=0;i<checkBoxes.length;i++) {
        checkBoxes[i].addEventListener("click", function(){
            checkBoxes[i].classList.toggle('selected');
            let selected = document.querySelectorAll('span.checkbox.selected')
            if (selected.length <1 ) {
                button.disabled = true
            } else {
                button.disabled = false
            }      
        });
    }
});

document.addEventListener("DOMContentLoaded", function(){
    let quantity = document.querySelector('input#id_quantity');
    let step2button = document.querySelector('#second-step');
    quantity.addEventListener('change', function() {
        if (quantity.value < 1) {
            step2button.disabled = true
        } else {
            step2button.disabled = false
         }
    });
});

document.addEventListener("DOMContentLoaded", function(){
    let categories = document.querySelectorAll('span.checkbox.selected')
})