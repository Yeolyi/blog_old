const PostNum = 5;

$(function () {
  let startIdx = 1;
  $("#postNextPage").click(function () {
    if (startIdx + 3 > PostNum) { return }
    startIdx += 3;
    $("#postList li").css({
      "display": "none"
    })
    $("#postList li:nth-child(-n+" + Math.min(PostNum, startIdx + 2) + ")").css({
      "display": "block"
    })
    /* 괄호 쳐야되네???!?? */
    $("#postList li:nth-child(-n+" + (startIdx - 1) + ")").css({
      "display": "none"
    })
  })
  $("#postPrevPage").click(function () {
    if (startIdx - 3 < 1) { return }
    startIdx -= 3;
    $("#postList li").css({
      "display": "none"
    })
    $("#postList li:nth-child(-n+" + Math.max(0, startIdx + 2) + ")").css({
      "display": "block"
    })
    /* 괄호 쳐야되네???!?? */

    $("#postList li:nth-child(-n+" + Math.max(0, startIdx - 1) + ")").css({
      "display": "none"
    })
  })
})