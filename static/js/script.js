console.log("Connected");
const pages = ["index", "postings", "users", "dashboard", "signup", "login"]
pages.forEach((page)=>{
       if (document.URL.includes(`${page}`)){
            document.querySelector(`#${page}`).style.color = 'white';
            console.log(`it includes ${page}`);
       }
    }
)

const fullnameText = document.getElementById("fullnameText");
const locationText = document.getElementById("locationText");
const majorText = document.getElementById("majorText");
const githubText = document.getElementById("githubText");
const pictureText = document.getElementById("pictureText");
const editButton = document.getElementById("editButton");
const saveButton = document.getElementById("saveButton");

editButton.addEventListener("click", function() {
  console.log("edit button is being clicked")
  fullnameText.readOnly = false;
  fullnameText.style.backgroundColor = "#dddbdb";
  locationText.readOnly = false;
  locationText.style.backgroundColor = "#dddbdb";
  majorText.readOnly = false;
  majorText.style.backgroundColor = "#dddbdb";
  githubText.readOnly = false;
  githubText.style.backgroundColor = "#dddbdb";
  pictureText.readOnly = false;
  pictureText.style.backgroundColor = "#dddbdb";
} );

saveButton.addEventListener("click", function() {
  console.log("save button is being clicked")
  fullnameText.readOnly = true;
  fullnameText.style.backgroundColor = "white";
  locationText.readOnly = true;
  locationText.style.backgroundColor = "white";
  majorText.readOnly = true;
  majorText.style.backgroundColor = "white";
  githubText.readOnly = true;
  githubText.style.backgroundColor = "white";
} )