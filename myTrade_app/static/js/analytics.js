let symbol = document.getElementById('symbol').value; 

createChart(symbol)
async function createChart(symbol){
    const data = await getData()
    const ctx = document.getElementById('chart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.datesArr,
            datasets: [{
                data: data.priceArr,
                label: `${symbol} Close Price Adjusted Each Day`, 
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

async function getData(){
    const response = await fetch(`https://alpha-vantage.p.rapidapi.com/query?symbol=${symbol}&function=TIME_SERIES_DAILY_ADJUSTED`, {
        "method": "GET",
        "headers": {
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
            "x-rapidapi-key": "d786c51a95msh59c1cb8b1870608p12961fjsnfefeb6091e22"
        }
    });
    const data = await response.json();
    const datesArr = []
    const priceArr = []
    tsDaily = data["Time Series (Daily)"];
    for(date in tsDaily){
        // console.log(date)
        // console.log(tsDaily[date]['4. close'])
        datesArr.unshift(date);
        priceArr.unshift(tsDaily[date]['4. close']);
        
    }
    return { datesArr, priceArr }
}