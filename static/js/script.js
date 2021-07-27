console.log("Connected");
const pages = ["index", "postings", "users", "dashboard", "signup", "login"]
pages.forEach((page)=>{
       if (document.URL.includes(`${page}`)){
           document.querySelector(`#${page}`).style.color = 'white';
            console.log(`it includes ${page}`);
       }
    }
)