let menuItems = document.getElementById('menu-items');

menuItems.style.maxHeight = "0px";

function menuToggle(params) {
    if(menuItems.style.maxHeight == "0px"){
        menuItems.style.maxHeight = "200px";
    } else{
        menuItems.style.maxHeight = "0px";
    }
}







