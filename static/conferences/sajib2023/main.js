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

    
})


