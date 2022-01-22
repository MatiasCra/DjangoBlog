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

const addTagToCategories = (tagName, tagId) => {
  const cSelect = document.getElementById("tagsSelect");
  newOption = document.createElement("option");
  newOption.innerHTML = tagName;
  newOption.value = tagId;
  cSelect.appendChild(newOption);
};
