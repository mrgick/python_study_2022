const form = document.getElementById("newsDeleting");
form.addEventListener("submit", (event) => {
    let result = confirm("Вы точно уверены, что хотите удалить эту новость?");
    if (!result) {
        event.preventDefault();
    }
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

var newWindowOpened = false;
async function newBlogWindow() {
    if (!newWindowOpened) {
        w = window.open('/blog/add/', "_blank", "toolbar=yes,top=300,left=300,width=300,height=250,resizable=no,status=no");
        newWindowOpened = true;
        while (!w.closed) {
            elem = w.document.getElementsByClassName('info');
            if (elem.length != 0) {
                elem = elem[0].innerText.split(':');
                blogId = elem[0].split(' ');
                blogId = blogId[blogId.length - 1];
                blogName = elem[1].split(' ')[0];
                let select = document.getElementById('id_blog');
                let opt = new Option('Категория: ' + blogName, blogId);
                select.add(opt);
                console.log('Добавлено:', blogId, blogName);
                newWindowOpened = false
                return 0;
            }
            await sleep(1000)
        }
        newWindowOpened = false

    } else {
        alert("Открыто другое окно добавления блога.")
    }
}