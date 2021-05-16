function addlike(photoId) {
  fetch("/add_like", {
    method: "POST",
    body: JSON.stringify({ photoId:photoId}),
  }).then((_res) => {
    window.location.href = "/our_post";
  })}
  