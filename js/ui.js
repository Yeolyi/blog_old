const PostNum = 1;
const PageSize = 10;

$(function () {
  let startIdx = 1;
  $("#postNextPage").click(function () {
    if (startIdx + PageSize > PostNum) { return }
    startIdx += PageSize;
    $("#postList li").css({
      "display": "none"
    })
    $("#postList li:nth-child(-n+" + Math.min(PostNum, startIdx + PageSize - 1) + ")").css({
      "display": "block"
    })
    /* 괄호 쳐야되네???!?? */
    $("#postList li:nth-child(-n+" + (startIdx - 1) + ")").css({
      "display": "none"
    })
  })
  $("#postPrevPage").click(function () {
    if (startIdx - PageSize < 1) { return }
    startIdx -= PageSize;
    $("#postList li").css({
      "display": "none"
    })
    $("#postList li:nth-child(-n+" + Math.max(0, startIdx + PageSize - 1) + ")").css({
      "display": "block"
    })
    /* 괄호 쳐야되네???!?? */

    $("#postList li:nth-child(-n+" + Math.max(0, startIdx - 1) + ")").css({
      "display": "none"
    })
  })
})