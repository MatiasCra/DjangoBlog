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

const addToTags = (tagName, tagId = -1) => {
  const tagList = document.getElementById("tagList");
  if (tagList.childElementCount === 1) {
    tagList.children[0].classList.add("d-none");
  }
  const newLi = document.createElement("li");
  newLi.className = "card px-2 my-1 tag-item";
  newLi.innerHTML = tagName;
  if (tagId === -1) {
    newLi.id = tagName;
  } else {
    newLi.id = tagId;
  }
  newLi.addEventListener("click", () => {
    newLi.parentNode.removeChild(newLi);
    if (tagList.childElementCount === 1) {
      tagList.children[0].classList.remove("d-none");
    }
  });

  tagList.appendChild(newLi);
};

const filterCollectionByValue = (collection, val) => {
  for (let index = 0; index < collection.length; index++) {
    const element = collection[index];
    if (element.value === val) {
      return element;
    }
  }
  return false;
};

const isValidTag = (tag) => {
  isEmpty = !tag.trim().length;
  isNumeric = !isNaN(tag) || !isNaN(parseFloat(tag));
  console.log(!isEmpty && !isNumeric);
  return !isEmpty && !isNumeric;
};

const addTagBtn = document.getElementById("addTagBtn");
addTagBtn.addEventListener("click", (e) => {
  e.preventDefault();
  const tagDataList = document.getElementById("tagDataList");
  if (isValidTag(tagDataList.value)) {
    options = document.getElementsByTagName("option");
    const opt = filterCollectionByValue(options, tagDataList.value);
    if (opt) {
      addToTags(opt.value, opt.id);
    } else {
      addToTags(tagDataList.value);
    }
  }
  tagDataList.value = "";
  tagDataList.focus();
});

const submitPostBtn = document.getElementById("publishBtn");
submitPostBtn.addEventListener("click", (e) => {
  e.preventDefault();
  form = document.getElementById("postForm");
  tags = document.getElementsByClassName("tag-item");
  for (let index = 0; index < tags.length; index++) {
    newInput = document.createElement("input");
    newInput.type = "hidden";
    newInput.name = "tags";
    newInput.value = tags[index].id;
    form.appendChild(newInput);
  }
  form.submit();
});
