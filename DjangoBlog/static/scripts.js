function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(";");
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

const addTagToCategories = (tagName, tagId) => {
  const cSelect = document.getElementById("tagsSelect");
  newOption = document.createElement("option");
  newOption.innerHTML = tagName;
  newOption.value = tagId;
  cSelect.appendChild(newOption);
};

const addTagBtn = document.getElementById("addTagBtn");
addTagBtn.addEventListener("click", () => {
  const tagName = prompt("Name of the new tag:");
  const csrftoken = getCookie("csrftoken");
  myData = new FormData();
  myData.append("tag", tagName);

  fetch("/blog/tag/add/", {
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({ tag: tagName }),
  })
    .then(function (res) {
      console.log(res);
      if (res.ok) {
        res.text().then((tagId) => addTagToCategories(tagName, tagId));
      }
    })
    .catch(function (res) {
      console.log(res);
    });
});
