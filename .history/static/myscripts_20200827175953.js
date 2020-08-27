function hide(id) {
  var x = document.getElementById(`tohide${id}`);
  var b = document.getElementById(`button${id}`)
  if (x.style.visibility === "hidden") {
    b.innerHTML = "Hide"
    x.style.visibility = "visible";
  } else {
    b.innerHTML = "Show"
    x.style.visibility = "hidden";
  }
} 

function delete(id) {
  window.location.replace("http:127.0.0.1:500-.com");
}