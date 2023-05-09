const registerButton = document.getElementById("register");
const loginButton = document.getElementById("login");
const container = document.getElementById("container");
var darkModeImageUrl = "./static/images/dark.mp4";
var lightModeImageUrl = "./static/images/light.mp4";

registerButton.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

loginButton.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

const toggleSwitch = document.querySelector('#dark-mode');
const source = document.querySelector('source');
function switchTheme() {
    
    if (this.checked) {
    video.loop = false;
    source.setAttribute('src', darkModeImageUrl);
    } else {
    video.loop = false;
    source.setAttribute('src', lightModeImageUrl);
    }
    video.load();
    video.play();
}
toggleSwitch.addEventListener('click', switchTheme);

const myVideo = document.getElementById('myVideo');
var video = document.querySelector('video'); 
myVideo.addEventListener('canplay', function() {
    video.muted = false;
    this.play();
    video.muted = false;
});
myVideo.addEventListener('canplaythrough', function() {
    video.muted = false;
    if(this.paused){
        this.play();
    video.muted = false;
    }
    video.muted = false;
});

var video = document.getElementById("myVideo");
video.addEventListener('ended', function() {
    src = source.getAttribute('src');
    var newUrl = src.replace(/(\.\w+)$/, '2$1');
    // dark2 = "{{ url_for('static', filename='images/dark2.mp4') }}";
    source.setAttribute('src', newUrl);
    video.load();
    video.play();
    video.loop = true;
});
const aa = document.querySelector(".toggle-input");
const toggleLabel = document.querySelector(".toggle-label");
let typeCypher = document.getElementById("typeCypher");

aa.addEventListener("change", function() {
  if (this.checked) {
    toggleLabel.classList.remove("aes");
    toggleLabel.classList.add("playfair");
    // typeCypher.classList.remove("aes");
    // typeCypher.classList.add("playfair");
    typeCypher.textContent = "PlayFair";
  } else {
    toggleLabel.classList.remove("playfair");
    toggleLabel.classList.add("aes");
    // typeCypher.classList.remove("playfair");
    // typeCypher.classList.add("aes");
    typeCypher.textContent = "AES";
  }
});


//////////////////
function copyTextDe() {
    var copyText = document.getElementById("decrypt-result");
    var btnDe = document.querySelector("#btn1");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value).then(function (){
      btnDe.textContent = "Copied"
    })
    setTimeout(function() {
    btnDe.textContent = 'Copy';
  }, 3000);
  }
  function copyTextEn() {
    var copyText = document.getElementById("encrypt-result");
    var btnEn = document.querySelector("#btn2");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(copyText.value).then(function (){
      btnEn.textContent = "Copied"
    })
    setTimeout(function() {
    btnEn.textContent = 'Copy';
  }, 3000);
  }