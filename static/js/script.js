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
const emailText = document.getElementById("emailText");
const locationText = document.getElementById("locationText");
const majorText = document.getElementById("majorText");
const githubText = document.getElementById("githubText");
const editButton = document.getElementById("editButton");
const saveButton = document.getElementById("saveButton");

editButton.addEventListener("click", function() {
  console.log("edit button is being clicked")
  fullnameText.contentEditable = true;
  fullnameText.style.backgroundColor = "#dddbdb";
  emailText.contentEditable = true;
  emailText.style.backgroundColor = "#dddbdb";
  locationText.contentEditable = true;
  locationText.style.backgroundColor = "#dddbdb";
  majorText.contentEditable = true;
  majorText.style.backgroundColor = "#dddbdb";
  githubText.contentEditable = true;
  githubText.style.backgroundColor = "#dddbdb";
} );

saveButton.addEventListener("click", function() {
  console.log("save button is being clicked")
  fullnameText.contentEditable = false;
  fullnameText.style.backgroundColor = "white";
  emailText.contentEditable = false;
  emailText.style.backgroundColor = "white";
  locationText.contentEditable = false;
  locationText.style.backgroundColor = "white";
  majorText.contentEditable = false;
  majorText.style.backgroundColor = "white";
  githubText.contentEditable = false;
  githubText.style.backgroundColor = "white";
} )