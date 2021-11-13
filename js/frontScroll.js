class ScrollBlock {
    constructor(startH, fadingH, endH, appearAnim, disappearAnim) {
        this.startH = startH;
        this.fadingH = fadingH;
        this.endH = endH;
        this.animation = function (height, target) {
            let ret;
            if (height <= fadingH) {
                ret = appearAnim(height, target);
            } else {
                ret = disappearAnim(height, target);
            }

            function defaultMove(height) {
                return easeInOut(startH, Math.min(startH+1000, endH), height, 0, 0.5);
            }
            if (ret.hasOwnProperty("padding-bottom")) {
                ret["padding-bottom"] += defaultMove(height)
            } else {
                ret["padding-bottom"] = defaultMove(height)
            }
            for (let key in ret) {
                if (key == "padding-bottom") {
                    ret[key] += "em";
                }
            }
            target.css(ret)
        }
    }
}

function easeInOut(startH, endH, curH, startVal, endVal) {
    const p = Math.min(1, (curH - startH) / (endH - startH))

    function easeInOutQuart(x) {
        return x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2;
    }
    return startVal + (endVal - startVal) * easeInOutQuart(p)
}

const scrollBlockOne = new ScrollBlock(0, 600, 1000,
    function (height) {
        popPadding = easeInOut(0, 300, height, 0, 2.2)
        newOpacity = easeInOut(0, 300, height, 0.3, 1)
        return {
            "padding-top": "1.25em",
            "padding-bottom": popPadding,
            "opacity": newOpacity
        }
    },
    function (height) {
        newOpacity = easeInOut(600, 1000, height, 1, 0)
        return {
            "padding-top": "1.25em",
            "padding-bottom": 2.2,
            "opacity": newOpacity
        }
    }
)

const scrollBlockTwo = new ScrollBlock(0, 600, 1000,
    function (height) {
        newOpacity = easeInOut(0, 600, height, 0, 1)
        return {
            "padding-top": "1.25em",
            "opacity": newOpacity
        }
    },
    function (height) {
        newOpacity = easeInOut(600, 1000, height, 1, 0)
        return {
            "padding-top": "1.25em",
            "opacity": newOpacity
        }
    }
)

function frontPageTitleObject(startH, endH) {
    return new ScrollBlock(startH, endH-400, endH,
        function (height) {
            popPadding = easeInOut(startH, startH+300, height, 0, 1.8)
            newOpacity = easeInOut(startH, startH+300, height, 0, 1)
            return {
                "padding-bottom": popPadding+2,
                "opacity": newOpacity
            }
        },
        function (height) {
            newOpacity = easeInOut(endH-400, endH, height, 1, 0)
            return {
                "padding-bottom": 1.8+2,
                "opacity": newOpacity
            }
        }
    )
}

const scrollBlockThree = frontPageTitleObject(900, 3000)

/* 앱 */

function frontPageAppTitleObject(startH, offset) {
    return new ScrollBlock(startH, startH+600, startH+1000,
        function (height) {
            newOpacity = easeInOut(startH, startH+300, height, 0, 1)
            ret =  {
                "padding-bottom": 2,
                "opacity": newOpacity
            }
            if (offset) {
                ret["padding-top"] = offset+"em"
            }
            return ret
        },
        function (height) {
            newOpacity = easeInOut(startH+600, startH+1000, height, 1, 0)
            ret = {
                "padding-bottom": 2,
                "opacity": newOpacity
            }
            if (offset) {
                ret["padding-top"] = offset+"em"
            }
            return ret
        }
    )
}

function frontPageAppIconObject(startH) {
    return new ScrollBlock(startH, startH+600, startH+1000,
        function (height) {
            newOpacity = easeInOut(startH, startH+600, height, 0, 1)
            return {
                "padding-top": "15vw",
                "opacity": newOpacity
            }
        },
        function (height) {
            newOpacity = easeInOut(startH+600, startH+1000, height, 1, 0)
            return {
                "padding-top": "15vw",
                "opacity": newOpacity
            }
        }
    )
}

/* 앱 소개 */
const scrollBlockFour = frontPageAppTitleObject(1000)
const scrollBlockFive = frontPageAppIconObject(1000)
const scrollBlock6 = frontPageAppTitleObject(2000)
const scrollBlock7 = frontPageAppIconObject(2000)
/* 프론트엔드 */
const scrollBlock8 = frontPageTitleObject(2900, 3900)
const scrollBlock9 = frontPageAppTitleObject(3000, 2)
/* 마무리 */
const scrollBlock10 = frontPageAppTitleObject(3900, 2)

const scrollBlocks = [scrollBlockOne, scrollBlockTwo, scrollBlockThree, scrollBlockFour, scrollBlockFive, scrollBlock6, scrollBlock7, scrollBlock8, scrollBlock9, scrollBlock10]

function update() {
    let height = Math.max(0, document.documentElement.scrollTop);
    for (let i = 0; i < scrollBlocks.length; i++) {
        const element = scrollBlocks[i];
        if (element.startH <= height && height <= element.endH) {
            target = $(".front-page__object:nth-child(" + (i + 1) + ")")
            target.css({
                "display": "inline-block"
            })
            element.animation(height, $(".front-page__object:nth-child(" + (i + 1) + ")"))
        } else {
            $(".front-page__object:nth-child(" + (i + 1) + ")").css({
                "display": "none"
            })
        }
    }
}

$(update)
document.addEventListener('scroll', function () {
    update()
});