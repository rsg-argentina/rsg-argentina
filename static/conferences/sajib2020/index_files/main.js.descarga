$( function() {
    

    var date = Date.now(),
    second = 1000;

    function pad(num) {
        return ('0' + num).slice(-2);
    }

    function checkTime(what = "day") {

        var dateObj;
        date += second;
        dateObj = new Date(date);

        if (what == "day"){
            
            dd = pad(dateObj.getDate()) 
            mm = pad(parseInt(dateObj.getMonth())+1).toString()
            yy = dateObj.getFullYear()
            
            //clockEl.innerHTML = [dd,mm,yy].join("-");
            return [dd,mm,yy].join("-");
        
        } else {
        
            hh = pad(dateObj.getHours())
            mm = pad(dateObj.getMinutes())
            ss = pad(dateObj.getSeconds())

            return [hh,mm,ss].join(":");

        }
    

    } 
        

    $("#fullprogram").click(function(e){
        e.preventDefault()
        $("#day-0").css("display","none")  
        $("#day-1").css("display","block")
        $("#day-2").css("display","block")
        $("#poster").css("display","none")              

    });

    $("#day-1-bt").click(function(e){
        // toggle day program
        e.preventDefault()
        $("#day-0").css("display","none")  
        $("#day-2").css("display","none")   
        $("#poster").css("display","none")      
        $("#day-1").css("display","block")              
    });

    $("#day-2-bt").click(function(e){
        // toggle day program
        e.preventDefault()
        $("#day-0").css("display","none")  
        $("#day-1").css("display","none")  
        $("#poster").css("display","none")      
        $("#day-2").css("display","block")              
    });

    $("#poster-bt").click(function(e){
        // toggle day program
        e.preventDefault()
        $("#day-0").css("display","none")  
        $("#day-1").css("display","none")  
        $("#day-2").css("display","none")              
        $("#poster").css("display","block")              
    });

    setInterval(checkTime, second*60);
    
})


