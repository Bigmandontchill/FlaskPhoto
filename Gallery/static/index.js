function addlike(photoId) {
  console.log("haha")
  fetch("/add_like", {
    method: "POST",
    body: JSON.stringify({photoId:photoId}),
  }).then((_res) => {
    window.location.href = "/";
  })}

 