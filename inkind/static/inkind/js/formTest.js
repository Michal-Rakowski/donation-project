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
    let step3button = document.querySelector('#third-step')
    step3button.disabled = true
    let ajax = document.querySelector("#ajax");
    ajax.addEventListener("click", function(){
        step3button.disabled = false
        });    
});

document.addEventListener("DOMContentLoaded", function() {
    let lastStep = document.getElementById('summary-step');
    lastStep.addEventListener('click', function (){
        /* let categories = document.querySelectorAll('span.checkbox.selected') */
        let quantity = document.getElementById('id_quantity').value;
        let address = document.getElementById('id_address').value;
        let city = document.getElementById('id_city').value;
        let zip_code = document.getElementById('id_zip_code').value;
        let phone = document.getElementById('id_phone_number').value;
        let date = document.getElementById('id_pick_up_date_time_0').value;
        let time = document.getElementById('id_pick_up_date_time_1').value;
        let comment = document.getElementById('id_pick_up_comment').value;
        let selected = document.querySelector("input[name='organization']:checked");
        let org = selected.getAttribute('data-desc')
        document.getElementById('summarybox1').innerHTML = "Przekazujesz worki w ilości: " + quantity
        document.getElementById('summarybox2').innerText = "Dla " + org;
        document.getElementById('address').innerHTML = address
        document.getElementById('city').innerHTML = city
        document.getElementById('zip').innerHTML = zip_code
        document.getElementById('phone').innerHTML = phone
        document.getElementById('date').innerHTML = date
        document.getElementById('time').innerHTML = time
        document.getElementById('comments').innerHTML = comment
    })
});
