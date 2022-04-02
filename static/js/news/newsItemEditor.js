const form = document.getElementById("newsDeleting");
form.addEventListener("submit", (event) => {
    let result = confirm("Вы точно уверены, что хотите удалить эту новость?");
    if (!result) {
        event.preventDefault();
    }
});