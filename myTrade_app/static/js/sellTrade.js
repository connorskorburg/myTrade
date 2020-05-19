function showTotal(){
    document.getElementById('show-total').style.display = "block";
    shares = document.getElementById('shares').value;
    shares = parseFloat(shares)
    hiddenShares = document.getElementById('hidden_shares').value;
    hiddenShares = parseFloat(hiddenShares);
    
        
    currentPrice = document.getElementById('current_price').innerText;

    function parseNumber(val, locale = 'en-US') {
        let format = Intl.NumberFormat(locale).format('1.1');
        let newPattern = new RegExp(`[^-+0-9${ format.charAt( 1 ) }]`, 'g');
        let pattern = val.replace(newPattern, '');
        let newPrice = pattern.replace(format.charAt(1), '.');
      
        return parseFloat(newPrice);
      }
    
    currentPrice = parseNumber(currentPrice);
    if(isNaN(shares) == true){
        shares = "Enter a Number";
        totalPrice = 0.00.toFixed(2);
    }
    else{
        totalPrice = currentPrice * shares;
        totalPrice = totalPrice.toFixed(2);
    }

    
    if(shares > hiddenShares){
        document.getElementById('sell_btn').style.display = "none";
    }
    else if(shares <= hiddenShares){
        document.getElementById('sell_btn').style.display = "block"
    }

    document.getElementById('total_price').innerText = totalPrice;
    document.getElementById('total_shares').innerText = shares;
    document.getElementById('post_shares').value = shares;
    document.getElementById('price_per_share').innerText = currentPrice.toFixed(2);
    document.getElementById('input_share').value = shares;
}
