function pokahaslo(){

    let hasla = document.getElementsByClassName('passwd');
    Array.from(hasla).forEach(element => {
        element.setAttribute("password", "text");
    });

}