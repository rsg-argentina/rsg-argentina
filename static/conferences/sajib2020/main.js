$( function() {
    

    var date = Date.now(),
    second = 1000;

    function pad(num) {
        return ('0' + num).slice(-2);
    }

    function checkDay() {
    var dateObj;
    date += second;
    dateObj = new Date(date);
    
    dd = pad(dateObj.getDate()) 
    mm = pad(parseInt(dateObj.getMonth())+1).toString()
    yy = dateObj.getFullYear()
    
        //clockEl.innerHTML = [dd,mm,yy].join("-");
        return [dd,mm,yy].join("-");
    }        

    $("#fullprogram").click(function(e){
        e.preventDefault()
        $("#day-1").css("display","block")
        $("#day-2").css("display","block")        

    });

    $("#day-1-bt").click(function(e){
        // toggle day program
        e.preventDefault()
        $("#day-2").css("display","none")   
        $("#day-1").css("display","block")              
    });

    $("#day-2-bt").click(function(e){
        // toggle day program
        e.preventDefault()
        $("#day-1").css("display","none")  
        $("#day-2").css("display","block")              
    });

    $("#live").click(function(e){
        e.preventDefault()
        $("#day-1").css("display","none")  
        $("#day-2").css("display","none")  
        $("#day-0").css("display","none")    
        
        if(checkDay() == $("#day-1").attr("day") ){
      
            $("#day-1").css("display","block")

        } else if (checkDay() == $("#day-2").attr("day")){
   
            $("#day-2").css("display","block")        

        } else {
            $("#day-0").css("display","block")  
        }           

    })

    setInterval(checkDay, second*60);
    
})


