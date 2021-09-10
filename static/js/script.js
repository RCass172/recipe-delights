$(document).ready(function(){
    $('.sidenav').sidenav();
    $(".dropdown-trigger").dropdown();
    $('.collapsible').collapsible();
    $('select').formSelect();
});

// Used following website to help create dynamic add button 
// https://jquerylove.com/content/how-to-use-jquery-to-dynamically-add-text-field-in-form-2004/
let ingredient = 1;

    $(".add-ingredient").click(function (e) {
        e.preventDefault();
            ingredient++;
            $(".new-ingredient").append(`
            <div class="input-field">
            <input id="ingredients${ingredient}" name="ingredients" type="text" class="validate" minlength="3" required>
            <label for="ingredients${ingredient}">Add Another Ingredient</label></div>`);
    });