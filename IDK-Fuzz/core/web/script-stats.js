// jQuery
$(document).ready(function () {
    var prevOpen = false;
    var currOpen = true;
    $(".prev-items").slideUp(0);
    $(".prev").on("click",function(){
        $(".prev-items").slideToggle();
        if(!prevOpen){
            $(".prev").text("Previous fuzzjobs (Click to hide)");
            $(".prev").prev().attr('class', 'arrow-down');
            prevOpen = true;
        }
        else{
            $(".prev").text("Previous fuzzjobs (Click to expand)");
            $(".prev").prev().attr('class', 'arrow-right');
            prevOpen = false; 
        }
    });
    $(".curr").on("click",function(){
        $(".curr-items").slideToggle();
        if(!currOpen){
            $(".curr").text("Current fuzzjobs (Click to hide)");
            $(".curr").prev().attr('class', 'arrow-down');
            currOpen = true;
        }
        else{
            $(".curr").text("Current fuzzjobs (Click to expand)");
            $(".curr").prev().attr('class', 'arrow-right');
            currOpen = false;
        }
    });
});