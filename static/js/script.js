$(document).ready(function () {
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
            <label for="ingredients${ingredient}">Add Another Ingredient</label>
            <button type="button" class="btn delete-ingredient">Delete Ingredient</button></div>`);
});

// Delete individual ingredient
$("form").on("click", ".delete-ingredient", function(e) {
    e.preventDefault();
    $(this).parent('div').remove();
    x--;
});

let method = 1;

$(".add-method").click(function (e) {
    e.preventDefault();
    ingredient++;
    $(".new-method").append(`
            <div class="input-field">
            <input id="method${method}" name="method" type="text" class="validate" minlength="3" required>
            <label for="method${method}">Add Another Step</label>
            <button type="button" class="btn delete-method">Delete Step</button></div>`);
});

// Delete individual step
$("form").on("click", ".delete-method", function(e) {
    e.preventDefault();
    $(this).parent('div').remove();
    x--;
});