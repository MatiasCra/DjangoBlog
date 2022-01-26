// To get the tocken
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

// Remove the tags on click
const tagLis = document.getElementsByClassName("tag-item");
if (tagLis) {
  for (let index = 0; index < tagLis.length; index++) {
    const tagLi = tagLis[index];
    tagLi.addEventListener("click", () => {
      tagLi.parentNode.removeChild(tagLi);
      const tagList = document.getElementById("tagList");
      if (tagList.childElementCount === 1) {
        tagList.children[0].classList.remove("d-none");
      }
    });
  }
}

// Add to list and listener to remove them on click
const addToTags = (tagName, tagId = -1) => {
  const tagList = document.getElementById("tagList");
  if (tagList.childElementCount === 1) {
    tagList.children[0].classList.add("d-none");
  }
  const newLi = document.createElement("li");
  newLi.className = "card px-2 my-1 tag-item";
  newLi.innerHTML = tagName;
  // If it's not an existing tag, send the name to create it
  if (tagId === -1) {
    newLi.id = tagName;
  } else {
    newLi.id = tagId;
  }
  newLi.addEventListener("click", () => {
    newLi.parentNode.removeChild(newLi);
    // Show no tags message
    if (tagList.childElementCount === 1) {
      tagList.children[0].classList.remove("d-none");
    }
  });

  tagList.appendChild(newLi);
};

// HTMLCollection class does not seem to have a filter method
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
  return !isEmpty && !isNumeric;
};

// Add tag entered to the list
const addTagBtn = document.getElementById("addTagBtn");
if (addTagBtn) {
  addTagBtn.addEventListener("click", (e) => {
    e.preventDefault();
    const tagDataList = document.getElementById("tagDataList");
    if (isValidTag(tagDataList.value)) {
      options = document.getElementsByTagName("option");
      const opt = filterCollectionByValue(options, tagDataList.value);
      // If it's not an existing tag, send the name to create it
      if (opt) {
        addToTags(opt.value, opt.id);
      } else {
        addToTags(tagDataList.value);
      }
    }
    tagDataList.value = "";
    tagDataList.focus();
  });
}

// Add tags to form as hidden inputs
const submitPostBtn = document.getElementById("publishBtn");
if (submitPostBtn) {
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
    if (form.checkValidity()) {
      form.submit();
    }
  });
}

// Toggle the favourite of the post
const favIconI = document.getElementById("favIconI");
if (favIconI) {
  favIconI.addEventListener("click", (e) => {
    favIconI.classList.toggle("selected");
    favIconI.classList.toggle("bi-star");
    favIconI.classList.toggle("bi-star-fill");

    const csrftoken = getCookie("csrftoken");
    postId = favIconI.parentElement.id;

    // Adds/removes from favourites from the db
    fetch("/blog/post/favourite/" + postId, {
      headers: {
        "X-CSRFToken": csrftoken,
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "GET",
    })
      .then(function (res) {
        console.log(res);
      })
      .catch(function (res) {
        console.log(res);
      });
  });
}

// For search page
const tagsCheckLabels = document.getElementsByClassName("tagCheckBox");
if (tagsCheckLabels) {
  // Change (un)selected tag checkbox style
  for (let index = 0; index < tagsCheckLabels.length; index++) {
    const tagCheckLabel = tagsCheckLabels[index];
    tagCheckLabel.addEventListener("click", () => {
      tagCheckLabel.parentElement.classList.toggle("selected");
    });
  }

  // Filter tags
  const tagSearchBtn = document.getElementById("tagSearchBtn");
  if (tagSearchBtn) {
    tagSearchBtn.addEventListener("click", () => {
      tagSearchText = document.getElementById("tagSearchBar").value;
      for (let index = 0; index < tagsCheckLabels.length; index++) {
        const tagCheckLabel = tagsCheckLabels[index];
        if (!tagSearchText) {
          tagCheckLabel.parentElement.classList.remove("d-none");
        } else if (
          !tagCheckLabel.innerHTML
            .toLowerCase()
            .includes(tagSearchText.toLowerCase())
        ) {
          tagCheckLabel.parentElement.classList.add("d-none");
        } else {
          tagCheckLabel.parentElement.classList.remove("d-none");
        }
      }
    });
  }

  // Change behaviour of enter key when foccused on the tag searchbar
  tagSearchBar = document.getElementById("tagSearchBar")
  // Keydown ==> when press starts
  // Keyup ==> when press is released
  tagSearchBar.addEventListener("keydown", (e) => {
    // Number 13 is the "Enter" key on the keyboard
    if (e.keyCode === 13) {
      e.preventDefault();
      tagSearchBtn.click();
    }
  });

  tagSearchDelete = document.getElementById("tagSearchDelete")
  tagSearchDelete.addEventListener("click", (e) => {
    e.preventDefault()
    tagSearchBar.value = "";
    tagSearchBtn.click();
    tagSearchBar.focus();
  })
}
