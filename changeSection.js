const stories = 0;
const apps = 1;
const about = 2;
const sectionPath = [
  "Posts/postMain.html",
  "Apps/appsMain.html",
  "about/about.html"
];
let cur = 0;
function changeSection(section) {
  $(".sectionButton button:nth-child("+(cur+1)+")").css('color', 'dimgrey')
  cur = section;
  $("#contents").load(sectionPath[cur]);
  $(".sectionButton button:nth-child("+(cur+1)+")").css('color', 'royalblue')
}