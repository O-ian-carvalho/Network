document.querySelector('#sendpost').addEventListener('submit', ()=>{
    event.preventDefault();
    fetch('/newpost', {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector("#content").value
        })
      })
      .then(response => response.json())
      .then(result => {
        document.querySelector("#content").value = "Publishing..."
        setTimeout(()=>{
            document.querySelector("#content").value = "Publication successfully done!!"
            setTimeout(()=>{
                document.querySelector("#content").value = ""
            }, 4000)
        }, 1000)
        loadall()   
    });
})

function like(id){
   fetch('/like',{
    method:"POST",
    body: JSON.stringify({
        id: id
    })
   })
   .then(response => response.json())
   .then(result => {
        loadall()
   })
}

document.addEventListener("DOMContentLoaded", ()=>{

     loadall()
   
})

function loadall(){
    fetch('/allposts')
    .then(response => response.json())
    .then(result => {
        // Print emails
        const allposts = document.querySelector("#allposts")
        allposts.innerHTML = ''
        result['allposts'].forEach(element => {
             allposts.innerHTML += `
             <div class="post">
                <div id="top"> <h3>${element.user}</h3> <p>${element.month}/${element.day}/${element.year}</p></div>
                <div id="middle"><p>${element.content}</p></div>
                <div id="down"> ${element.liked ? '<i class="fa-solid fa-heart" onClick="like(' + element.id + ')"></i>' : '<i class="fa-regular fa-heart" onClick="like(' + element.id + ')"></i>'} </i> <p>${element.like_count}</p></div>
            </div>`
        });
    });
}
