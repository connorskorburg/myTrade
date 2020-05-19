let symbol = document.getElementById('symbol').value; 

createChart(symbol)
async function createChart(symbol){
    const data = await getData()
    console.log(data);
    if(data.datesArr.length == 0 || data.smaArr.length ==0){
        document.getElementById('chart').style.display = "none";
        document.getElementById('latest-table').style.display = "block";
    }
    else{
        const ctx = document.getElementById('chart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.datesArr,
                datasets: [{
                    data: data.smaArr,
                    label: `${symbol} Simple Moving Average over 60 Periods`, 
                    fill: false,
                    backgroundColor: 
                    'rgba(255, 99, 132, 0.2)',
                    borderColor: 
                    'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
        });
    }
}


async function getData(){
    const response = await fetch(`https://alpha-vantage.p.rapidapi.com/query?datatype=json&interval=5min&series_type=close&function=SMA&symbol=${symbol}&time_period=60`, {
        "method": "GET",
        "headers": {
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
            "x-rapidapi-key": "d786c51a95msh59c1cb8b1870608p12961fjsnfefeb6091e22"
        }
    });
    const data = await response.json();
    const datesArr = []
    const smaArr = []
    techSma = data["Technical Analysis: SMA"];
    for(date in techSma){
        // console.log(date)
        // console.log(techSma[date]['SMA'])
        datesArr.unshift(date);
        smaArr.unshift(techSma[date]['SMA']);
        
    }
    return { datesArr, smaArr }
}